import flet as ft

from components.buttons import PrimaryButton
from components.cards import FormCard
from components.theme import Colors


def main(page: ft.Page):
    page.title = "Teste PrimaryButton"
    page.bgcolor = Colors.BACKGROUND

    mensagem = ft.Text("Aguardando clique...")

    def ao_clicar(e):
        mensagem.value = "Botão principal funcionando!"
        page.update()

    card = FormCard(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Teste do PrimaryButton",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=Colors.TEXT,
                ),
                mensagem,
                PrimaryButton(
                    label="CONFIRMAR",
                    icon=ft.Icons.CHECK,
                    on_click=ao_clicar,
                ),
            ],
            spacing=16,
        ),
    )

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=card,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)