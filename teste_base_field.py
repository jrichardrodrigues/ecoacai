import flet as ft

from components.fields import BaseField


def main(page: ft.Page):
    page.title = "Teste BaseField"

    campo = BaseField(
        label="Nome do responsável",
        hint_text="Digite um nome",
    )

    def mostrar_erro(e):
        campo.mostrar_erro("Campo obrigatório.")
        page.update()

    def mostrar_sucesso(e):
        campo.mostrar_sucesso("Campo preenchido corretamente.")
        page.update()

    def limpar(e):
        campo.limpar()
        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Teste do componente BaseField",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                campo.control,
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Mostrar erro",
                            on_click=mostrar_erro,
                        ),
                        ft.ElevatedButton(
                            "Mostrar sucesso",
                            on_click=mostrar_sucesso,
                        ),
                        ft.ElevatedButton(
                            "Limpar",
                            on_click=limpar,
                        ),
                    ],
                ),
            ],
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)