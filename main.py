import flet as ft

def main(page: ft.Page):
    # --- PAGE CONFIGURATION ---
    page.title = "Qaydnoma AI"
    page.padding = 16
    page.scroll = "auto"  # Enum o'rniga xavfsiz string

    # --- STATE MANAGEMENT ---
    notes = []

    # --- INPUT CONTROLS ---
    input_field = ft.TextField(
        label="Yangi qaydnoma kiriting...",
        multiline=True,
        min_lines=2,
        max_lines=4,
        expand=True
    )

    search_field = ft.TextField(
        label="Qaydlardan qidirish...",
        dense=True
    )

    notes_list = ft.Column(spacing=10)

    # --- CORE LOGIC ---
    def render_notes(e=None):
        notes_list.controls.clear()
        query = search_field.value.lower().strip() if search_field.value else ""
        
        filtered = [
            (idx, note) for idx, note in enumerate(notes) 
            if query in note.lower()
        ]

        if not filtered:
            notes_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Qaydlar topilmadi..." if query else "Hali hech qanday qaydnoma yo'q.",
                        color="grey",
                        size=14
                    ),
                    padding=20
                )
            )
        else:
            for idx, text in filtered:
                # Indeks xatosiga qarshi xavfsiz closure
                def make_delete_handler(index_to_delete):
                    def handle_delete(e):
                        if 0 <= index_to_delete < len(notes):
                            notes.pop(index_to_delete)
                            render_notes()
                    return handle_delete

                card_item = ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(text, size=15, weight="bold", expand=True)
                                    ],
                                    expand=True
                                ),
                                ft.OutlinedButton(
                                    content=ft.Text("O'chirish", color="red"),
                                    on_click=make_delete_handler(idx)
                                )
                            ],
                            alignment="spaceBetween",
                            vertical_alignment="center"
                        ),
                        padding=12
                    )
                )
                notes_list.controls.append(card_item)

        page.update()

    search_field.on_change = render_notes

    def add_note_click(e):
        text = input_field.value.strip() if input_field.value else ""
        if text:
            notes.append(text)
            input_field.value = ""
            render_notes()

    def clear_all_click(e):
        notes.clear()
        render_notes()

    # --- UI LAYOUT ---
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("📝 Qaydnoma App", size=24, weight="bold", color="#1A237E"),
                ft.Text("Barcha muhim fikrlaringiz bir joyda", size=13, color="grey"),
            ]
        ),
        padding=10
    )

    input_box = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    input_field,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Text("Qo'shish", size=15),
                                bgcolor="#1E88E5",
                                color="white",
                                on_click=add_note_click,
                                expand=True
                            ),
                            ft.OutlinedButton(
                                content=ft.Text("Tozalash"),
                                on_click=clear_all_click
                            )
                        ]
                    )
                ]
            ),
            padding=10
        )
    )

    search_box = ft.Container(
        content=search_field,
        padding=10
    )

    notes_header = ft.Row(
        controls=[
            ft.Text("Mening Qaydlarim", size=16, weight="bold"),
        ],
        alignment="spaceBetween"
    )

    # --- BUILD PAGE ---
    page.add(
        header,
        input_box,
        search_box,
        notes_header,
        ft.Divider(height=1),
        notes_list
    )

    render_notes()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
