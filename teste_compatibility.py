import flet as ft

from components.compatibility import abrir_snackbar
from components.buttons import LinkButton
from components.theme import Colors


def main(page: ft.Page):
    page.title = "Teste de compatibilidade"

    def mostrar_mensagem(e):
        abrir_snackbar(
            page,
            "Camada de compatibilidade funcionando!",
            bgcolor=Colors.SUCCESS,
        )

    page.add(
        LinkButton(
            label="Testar compatibilidade",
            icon=ft.Icons.CHECK,
            on_click=mostrar_mensagem,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)