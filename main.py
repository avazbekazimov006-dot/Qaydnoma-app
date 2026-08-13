import flet as ft
import sqlite3

def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    conn.commit()
    conn.close()

def main(page: ft.Page):
    page.title = "Qaydnomalar"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    init_db()

    current_status = ["active"]

    title_input = ft.TextField(
        hint_text="Sarlavha", 
        border=ft.InputBorder.NONE
    )
    content_input = ft.TextField(
        hint_text="Qayd matni...", 
        border=ft.InputBorder.NONE, 
        multiline=True, 
        expand=True
    )

    notes_grid = ft.GridView(
        expand=True,
        runs_count=2,
        max_extent=200,
        child_aspect_ratio=0.8,
        spacing=10,
        run_spacing=10,
        padding=10
    )

    def load_notes():
        notes_grid.controls.clear()
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content FROM notes WHERE status = ? ORDER BY id DESC", 
            (current_status[0],)
        )
        rows = cursor.fetchall()
        conn.close()

        for note_id, title, content in rows:
            lines = content.split("\n") if content else []
            items = [ft.Checkbox(label=line.strip(), value=False) for line in lines if line.strip()]
            display_title = title if title else (lines[0] if lines else "Sarlavhasiz")

            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column(
                        controls=[
                            ft.Text(display_title, size=16, weight=ft.FontWeight.BOLD),
                            *items,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ),
            )
            notes_grid.controls.append(card)
        page.update()

    def save_and_go_back(e=None):
        title = title_input.value.strip() if title_input.value else ""
        content = content_input.value.strip() if content_input.value else ""

        if title or content:
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO notes (title, content, status) VALUES (?, ?, ?)", 
                (title, content, current_status[0])
            )
            conn.commit()
            conn.close()
            
        title_input.value = ""
        content_input.value = ""
        page.go("/")

    def change_view(e):
        index = e.control.selected_index
        status_map = {0: "active", 1: "active", 2: "archive", 3: "trash"}
        current_status[0] = status_map.get(index, "active")
        
        titles = {0: "Qaydnomalar", 1: "Eslatmalar", 2: "Arxiv", 3: "Chiqitdon"}
        main_appbar.title.value = titles.get(index, "Qaydnomalar")
        
        drawer.open = False
        load_notes()

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.Text("   Google Keep", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.LIGHTBULB, 
                label="Qaydnomalar"
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.NOTIFICATIONS, 
                label="Eslatmalar"
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ARCHIVE, 
                label="Arxiv"
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.DELETE, 
                label="Chiqitdon"
            ),
        ],
        on_change=change_view
    )

    main_appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=lambda _: page.show_drawer(drawer)),
        title=ft.Text("Qaydnomalar"),
    )

    def route_change(e=None):
        page.views.clear()
        
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    main_appbar,
                    notes_grid,
                ],
                floating_action_button=ft.FloatingActionButton(
                    icon=ft.Icons.ADD, 
                    on_click=lambda _: page.go("/create"),
                )
            )
        )
        
        if page.route == "/create":
            page.views.append(
                ft.View(
                    route="/create",
                    controls=[
                        ft.AppBar(
                            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=save_and_go_back),
                            title=ft.Text("Yangi qaydnoma"),
                        ),
                        ft.Container(
                            padding=15,
                            expand=True,
                            content=ft.Column(
                                controls=[
                                    title_input,
                                    ft.Divider(),
                                    content_input
                                ],
                                expand=True
                            )
                        )
                    ]
                )
            )
        page.update()
        load_notes()

    def view_pop(e):
        save_and_go_back()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()

ft.app(target=main)
