import flet as ft

def main(page: ft.Page):
    page.title = "Qaydnoma App"
    page.padding = 15

    notes = []
    notes_list = ft.ListView(expand=True, spacing=10)
    input_field = ft.TextField(label="Qaydnoma kiriting...", expand=True)

    def render():
        notes_list.controls.clear()
        for idx, text in enumerate(notes):
            def delete_click(e, i=idx):
                notes.pop(i)
                render()
                page.update()

            notes_list.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(text),
                        trailing=ft.IconButton(
                            icon="delete",
                            icon_color="red",
                            on_click=delete_click
                        )
                    )
                )
            )

    def add_click(e):
        if input_field.value.strip():
            notes.append(input_field.value.strip())
            input_field.value = ""
            render()
            page.update()

    page.add(
        ft.Row([
            input_field,
            ft.FloatingActionButton(icon="add", on_click=add_click)
        ]),
        ft.Divider(),
        ft.Text("Qaydlar ro'yxati:", weight="bold"),
        notes_list
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
