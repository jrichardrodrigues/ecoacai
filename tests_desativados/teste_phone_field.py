import flet as ft

from components.fields import PhoneField
from services import UsuarioService


def main(page: ft.Page):
    page.title = "Teste PhoneField"

    usuario_service = UsuarioService()

    celular = PhoneField(
        usuario_service=usuario_service,
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Teste do PhoneField",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                celular.container,
            ],
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)