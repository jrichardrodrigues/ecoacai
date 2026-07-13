import flet as ft

from components.fields import EmailField
from services import UsuarioService


def main(page: ft.Page):
    page.title = "Teste EmailField"

    usuario_service = UsuarioService()

    email = EmailField(
        usuario_service=usuario_service,
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Teste do EmailField",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                email.container,
            ],
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)