import flet as ft

from components.buttons import SecondaryButton
from components.cards import FormCard
from components.theme import Colors


def main(page: ft.Page):
    page.title = "Teste SecondaryButton"
    page.bgcolor = Colors.BACKGROUND

    mensagem = ft.Text("Aguardando clique...")

    def ao_clicar(e):
        mensagem.value = "Botão secundário funcionando!"
        page.update()

    card = FormCard(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Teste do SecondaryButton",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=Colors.TEXT,
                ),
                mensagem,
                SecondaryButton(
                    label="VOLTAR",
                    icon=ft.Icons.ARROW_BACK,
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