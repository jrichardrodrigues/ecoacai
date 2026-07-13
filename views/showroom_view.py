import flet as ft

from components.buttons import PrimaryButton, SecondaryButton
from components.cards import FormCard
from components.headers import PageHeader
from components.theme import Colors


class ShowroomView:

    def build(self):

        return ft.Container(

            expand=True,

            bgcolor=Colors.BACKGROUND,

            alignment=ft.Alignment.CENTER,

            content=FormCard(

                content=ft.Column(

                    controls=[

                        PageHeader(
                            title="EcoAçaí UI Kit",
                            subtitle="Biblioteca Visual",
                        ),

                        PrimaryButton(
                            label="Primary Button"
                        ),
                        SecondaryButton(
                            label="Secondary Button",
                            icon=ft.Icons.ARROW_BACK,
                        ),

                    ],

                    spacing=24,

                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),

                )

            )

        )