import flet as ft


class DashboardCard(ft.Card):
    """Card reutilizável para indicadores do Dashboard."""

    def __init__(
        self,
        titulo: str,
        valor: str,
        icone: str,
        cor: str = ft.Colors.BLUE,
    ):
        super().__init__(
            elevation=2,
            content=ft.Container(
                padding=20,
                border_radius=12,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Icon(
                            icone,
                            size=36,
                            color=cor,
                        ),
                        ft.Text(
                            titulo,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            valor,
                            size=28,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
            ),
        )