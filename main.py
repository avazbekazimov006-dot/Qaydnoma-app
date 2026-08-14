import flet as ft
import os

def main(page: ft.Page):
    # --- ILOVA SOZLAMALARI ---
    page.title = "Qaydnoma App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO

    # --- IKONKA VA RESURSLARNI XAVFSIZ TEKSHIRISH ---
    icon_path = "assets/icon.png"
    if not os.path.exists(icon_path):
        icon_path = None  # Fayl topilmasa ilova crash bermaydi

    # --- YUKLANISH (LOADING) EKRANI (SplashScreen o'rniga barqaror usul) ---
    loading_ring = ft.ProgressRing(width=30, height=30, stroke_width=3)
    loading_text = ft.Text("Yuklanmoqda...", size=14, color=ft.colors.GREY)
    
    loading_container = ft.Container(
        content=ft.Column(
            [loading_ring, loading_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    
    page.add(loading_container)
    page.update()

    # --- MALUMOTLAR BAZASI / QAYDNOMALAR RO'YXATI ---
    notes = []

    # UI elementlari
    notes_list_view = ft.ListView(expand=True, spacing=10)
    note_input = ft.TextField(
        label="Yangi qaydnoma yozing...", 
        multiline=True, 
        expand=True
    )

    # --- FUNKSIYALAR ---
    def add_note(e):
        if note_input.value.strip():
            notes.append(note_input.value.strip())
            note_input.value = ""
            render_notes()
            page.update()

    def delete_note(index):
        def _delete(e):
            notes.pop(index)
            render_notes()
            page.update()
        return _delete

    def render_notes():
        notes_list_view.controls.clear()
        for idx, note in enumerate(notes):
            notes_list_view.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.NOTE_ALT_OUTLINED, color=ft.colors.GREEN),
                        title=ft.Text(note),
                        trailing=ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color=ft.colors.RED_400,
                            on_click=delete_note(idx)
                        )
                    )
                )
            )

    # --- DRAWER (YON MENYU) SOZLAMALARI ---
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                icon=ft.icons.TEXT_SNIPPETS_OUTLINED,
                selected_icon=ft.icons.TEXT_SNIPPETS,
                label="Barcha qaydlar",
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon=ft.icons.INFO_OUTLINE,
                label="Dastur haqida",
            ),
        ]
    )

    # --- YUKLANISH TUGAGACH ASOSIY INTERFEYSNI CHIQARISH ---
    page.clean()  # Loading kontainerini olib tashlaymiz

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.icons.MENU, 
            on_click=lambda e: page.show_drawer(page.drawer)
        ),
        title=ft.Text("Qaydnoma App"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        note_input,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, 
                            on_click=add_note,
                            bgcolor=ft.colors.GREEN_600,
                            content_color=ft.colors.WHITE
                        )
                    ],
                    alignment=ft.MainAxisAlignment.BETWEEN
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Mening qaydlarim:", size=16, weight=ft.FontWeight.BOLD),
                notes_list_view
            ],
            expand=True
        )
    )
    
    render_notes()
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
