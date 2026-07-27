import flet as ft

from components.cards import FormCard


def main(page: ft.Page):

    page.add(

        FormCard(

            ft.Column(

                [

                    ft.Text(
                        "EcoAçaí",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        "Primeiro componente reutilizável."
                    ),

                ]

            )

        )

    )


ft.app(main)