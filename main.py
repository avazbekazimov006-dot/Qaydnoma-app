import flet as ft

class Note:
    def __init__(self, title="", items=None, is_pinned=False, is_archived=False, color=None, reminder=None):
        self.title = title
        self.items = items if items is not None else []
        self.is_pinned = is_pinned
        self.is_archived = is_archived
        self.color = color if color else "#1E1E2C"
        self.reminder = reminder

def main(page: ft.Page):
    page.title = "Qaydnomalar"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 12

    # Boshlang'ich qaydnomalar
    notes = [
        Note(
            title="azimiy",
            items=[{"text": "ggg", "checked": False}, {"text": "ggg", "checked": False}],
            color="#252836"
        )
    ]

    # --- YON MENYU (DRAWER) ---
    def close_drawer(e=None):
        drawer.open = False
        page.update()

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=20),
            ft.ListTile(leading=ft.Icon(ft.icons.LIGHTBULB_OUTLINE), title=ft.Text("Qaydnomalar"), on_click=close_drawer),
            ft.ListTile(leading=ft.Icon(ft.icons.ARCHIVE_OUTLINED), title=ft.Text("Arxiv"), on_click=close_drawer),
            ft.ListTile(leading=ft.Icon(ft.icons.DELETE_OUTLINE), title=ft.Text("Savat"), on_click=close_drawer),
        ]
    )
    page.drawer = drawer

    # Crash bergan show_drawer e=None bilan to'g'rilandi
    def show_drawer(e=None):
        drawer.open = True
        page.update()

    # --- ESLATGICH MODAL OYNASI (Google Keep uslubida) ---
    selected_date_text = ft.Text("14-avgust", size=14)
    selected_time_text = ft.Text("23:30", size=14)
    
    repeat_dropdown = ft.Dropdown(
        value="Takrorlanmaydi",
        options=[
            ft.dropdown.Option("Takrorlanmaydi"),
            ft.dropdown.Option("Har kuni"),
            ft.dropdown.Option("Har xafta"),
        ],
        border_color=ft.colors.WHITE24,
        text_size=14
    )

    active_note_holder = [None]

    def close_reminder_dialog(e=None):
        reminder_dialog.open = False
        page.update()

    def save_reminder(e=None):
        if active_note_holder[0]:
            active_note_holder[0].reminder = f"{selected_date_text.value}, {selected_time_text.value}"
        reminder_dialog.open = False
        render_notes()

    reminder_dialog = ft.AlertDialog(
        title=ft.Text("Qachon eslatilsin?", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            controls=[
                ft.ListTile(
                    title=ft.Text("Sana", size=11, color=ft.colors.GREY_400),
                    subtitle=selected_date_text,
                    trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN),
                ),
                ft.ListTile(
                    title=ft.Text("Vaqt", size=11, color=ft.colors.GREY_400),
                    subtitle=selected_time_text,
                    trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN),
                ),
                repeat_dropdown
            ],
            tight=True,
            spacing=5
        ),
        actions=[
            ft.TextButton("Bekor qilish", on_click=close_reminder_dialog),
            ft.ElevatedButton("Saqlash", on_click=save_reminder, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_reminder_dialog(note, e=None):
        active_note_holder[0] = note
        page.dialog = reminder_dialog
        reminder_dialog.open = True
        page.update()

    # --- RANG VA MAVZU PALITRASI ---
    def open_color_sheet(note, e=None):
        def apply_color(color_code):
            note.color = color_code
            color_bs.open = False
            render_notes()

        palette_colors = ["#1E1E2C", "#4A1525", "#4A2800", "#3E4A00", "#004A38", "#12304A"]
        
        color_bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("Rangni tanlang", weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.LENS,
                            icon_color=c,
                            icon_size=32,
                            on_click=lambda e, col=c: apply_color(col)
                        ) for c in palette_colors
                    ])
                ], tight=True)
            )
        )
        page.overlay.append(color_bs)
        color_bs.open = True
        page.update()

    # --- QADASH VA ARXIVLASH ---
    def toggle_pin(note, e=None):
        note.is_pinned = not note.is_pinned
        render_notes()

    def toggle_archive(note, e=None):
        note.is_archived = not note.is_archived
        render_notes()

    # --- EKRANDA CHIQARISH ---
    pinned_container = ft.Column(spacing=10)
    other_container = ft.Column(spacing=10)

    def render_notes():
        pinned_container.controls.clear()
        other_container.controls.clear()

        for note in notes:
            if note.is_archived:
                continue

            card_content = ft.Column(spacing=5)
            if note.title:
                card_content.controls.append(ft.Text(note.title, weight=ft.FontWeight.BOLD, size=16))

            for item in note.items:
                card_content.controls.append(
                    ft.Checkbox(label=item["text"], value=item["checked"])
                )

            if note.reminder:
                card_content.controls.append(
                    ft.Chip(
                        label=ft.Text(note.reminder, size=11),
                        leading=ft.Icon(ft.icons.ALARM, size=14)
                    )
                )

            card = ft.Card(
                color=note.color,
                content=ft.Container(
                    padding=12,
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.PUSHPIN if note.is_pinned else ft.icons.PUSHPIN_OUTLINED,
                                on_click=lambda e, n=note: toggle_pin(n)
                            ),
                            ft.IconButton(
                                icon=ft.icons.NOTIFICATIONS_NONE,
                                on_click=lambda e, n=note: open_reminder_dialog(n)
                            ),
                            ft.IconButton(
                                icon=ft.icons.ARCHIVE_OUTLINED,
                                on_click=lambda e, n=note: toggle_archive(n)
                            ),
                            ft.IconButton(
                                icon=ft.icons.PALETTE_OUTLINED,
                                on_click=lambda e, n=note: open_color_sheet(n)
                            )
                        ], alignment=ft.MainAxisAlignment.END),
                        card_content
                    ])
                )
            )

            if note.is_pinned:
                pinned_container.controls.append(card)
            else:
                other_container.controls.append(card)

        page.update()

    # Appbar
    page.app_bar = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU, on_click=show_drawer),
        title=ft.Text("Qaydnomalar"),
        bgcolor=ft.colors.SURFACE_VARIANT
    )

    # Asosiy joylashuv
    main_layout = ft.Column([
        ft.Text("Qadanganlar", size=12, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
        pinned_container,
        ft.Divider(),
        ft.Text("Boshqa qaydnomalar", size=12, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
        other_container
    ], scroll=ft.ScrollMode.AUTO)

    page.add(
        main_layout,
        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=lambda e: print("Yangi qaydnoma"))
    )

    render_notes()

# Ilovaga assets va Splash Screen ulandi
ft.app(
    target=main,
    assets_dir="assets",
    splash=ft.SplashScreen(
        content=ft.Container(
            content=ft.Image(src="assets/icon.png", width=200),
            alignment=ft.alignment.center,
            bgcolor="#1E1E2C"
        )
    )
)
