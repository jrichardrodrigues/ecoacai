import flet as ft

from components.fields import NameField


def main(page: ft.Page):
    page.title = "Teste NameField"

    nome = NameField()

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Teste do NameField",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                nome.container,
            ],
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)