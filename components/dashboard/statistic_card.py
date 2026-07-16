import flet as ft


class StatisticCard(ft.Card):
    """Card reutilizável para indicadores do Dashboard."""

    def __init__(
        self,
        titulo: str,
        valor: str,
        icone: str,
        cor: str,
    ) -> None:
        super().__init__(
            elevation=2,
            content=ft.Container(
                padding=18,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=52,
                            height=52,
                            border_radius=26,
                            bgcolor=cor,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                icone,
                                color=ft.Colors.WHITE,
                                size=28,
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    titulo,
                                    size=14,
                                    color=ft.Colors.GREY_700,
                                ),
                                ft.Text(
                                    valor,
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                    ],
                    spacing=15,
                    vertical_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),
                ),
            ),
        )