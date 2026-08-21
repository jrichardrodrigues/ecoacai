from datetime import datetime

import flet as ft

from components.theme import Colors, Typography, Spacing, Radius


class ExecutiveHeader(ft.Container):
    """Cabeçalho executivo reutilizável do Dashboard."""

    def __init__(
        self,
        titulo: str = "Dashboard Executivo",
        descricao: str = (
            "Visão estratégica das operações do EcoAçaí."
        ),
        on_calendario_click=None,
    ) -> None:
        super().__init__()

        self.padding = Spacing.XL
        self.border_radius = Radius.XL
        self.bgcolor = Colors.Brand.PRIMARY

        self.content = self._criar_linha_superior(
            titulo=titulo,
            descricao=descricao,
            on_calendario_click=on_calendario_click,
        )

    @staticmethod
    def _criar_linha_superior(
            titulo: str,
            descricao: str,
            on_calendario_click=None,
    ) -> ft.Control:
        data_hora = datetime.now().strftime(
            "%d/%m/%Y às %H:%M"
        )

        consulta_calendario = ft.Container(
            padding=ft.Padding(
                left=10,
                top=8,
                right=10,
                bottom=8,
            ),
            border_radius=Radius.LG,
            tooltip="Consultar Dashboard por data",
            on_click=on_calendario_click,
            content=ft.Row(
                tight=True,
                spacing=Spacing.SM,
                controls=[
                    ft.Icon(
                        ft.Icons.CALENDAR_MONTH,
                        color=ft.Colors.with_opacity(
                            0.75,
                            Colors.Text.ON_PRIMARY,
                        ),
                        size=18,
                    ),
                    ft.Text(
                        data_hora,
                        size=Typography.SMALL,
                        color=ft.Colors.with_opacity(
                            0.75,
                            Colors.Text.ON_PRIMARY,
                        ),
                    ),
                ],
            ),
        )

        return ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 8,
                    },
                    content=ft.Column(
                        spacing=Spacing.XS,
                        controls=[
                            ft.Text(
                                titulo,
                                size=Typography.H1,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.Text.ON_PRIMARY,
                            ),
                            ft.Text(
                                descricao,
                                size=Typography.BODY_SMALL,
                                color=ft.Colors.with_opacity(
                                    0.70,
                                    Colors.Text.ON_PRIMARY,
                                ),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 4,
                    },
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=consulta_calendario,
                ),
            ],
        )