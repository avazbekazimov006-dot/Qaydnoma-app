import flet as ft
import os

def main(page: ft.Page):
    # --- ILOVA SOZLAMALARI ---
    page.title = "Qaydnoma App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO

    # --- YUKLANISH (LOADING) EKRANI ---
    loading_ring = ft.ProgressRing(width=30, height=30, stroke_width=3)
    loading_text = ft.Text("Yuklanmoqda...", size=14, color="grey")
    
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
                        leading=ft.Icon("note_alt_outlined", color="green"),
                        title=ft.Text(note),
                        trailing=ft.IconButton(
                            icon="delete_outline",
                            icon_color="red",
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
                icon="text_snippets_outlined",
                selected_icon="text_snippets",
                label="Barcha qaydlar",
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon="info_outline",
                label="Dastur haqida",
            ),
        ]
    )

    # --- YUKLANISH TUGAGACH ASOSIY INTERFEYSNI CHIQARISH ---
    page.clean()

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon="menu", 
            on_click=lambda e: page.show_drawer(page.drawer)
        ),
        title=ft.Text("Qaydnoma App"),
        center_title=True,
        bgcolor="#E0E0E0"
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        note_input,
                        ft.FloatingActionButton(
                            icon="add", 
                            on_click=add_note,
                            bgcolor="#2E7D32",
                            content_color="white"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.BETWEEN
                ),
                ft.Divider(height=10, color="transparent"),
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
