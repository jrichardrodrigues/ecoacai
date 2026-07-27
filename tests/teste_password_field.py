import flet as ft

from components.cards import FormCard
from components.fields import PasswordField
from components.headers import PageHeader
from components.theme import Colors


def main(page: ft.Page):
    page.title = "Teste PasswordField"
    page.bgcolor = Colors.BACKGROUND

    senha = PasswordField()

    card = FormCard(
        content=ft.Column(
            controls=[
                PageHeader(
                    title="Teste de senha",
                    subtitle=(
                        "Digite uma senha para acompanhar "
                        "a validação em tempo real."
                    ),
                    icon=ft.Icons.LOCK_OUTLINE,
                ),
                senha.container,
            ],
            spacing=24,
        ),
    )

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            padding=20,
            content=card,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)