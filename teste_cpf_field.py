import flet as ft

from components.fields import CpfField
from services import UsuarioService


def main(page: ft.Page):
    page.title = "Teste CPF Field"

    usuario_service = UsuarioService()

    cpf = CpfField(usuario_service)

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Teste do CpfField",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                cpf.container,
            ]
        )
    )


if __name__ == "__main__":
    ft.run(main=main)