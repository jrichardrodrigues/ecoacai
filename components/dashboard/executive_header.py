from datetime import datetime

import flet as ft

from components.theme import Colors, Typography, Spacing, Radius


class ExecutiveHeader(ft.Container):
    """Cabeçalho executivo reutilizável do Dashboard."""

    def __init__(
        self,
        total_estabelecimentos: str,
        total_solicitacoes: str,
        total_sacas: str,
        total_kg: str,
        titulo: str = "Dashboard Executivo",
        descricao: str = (
            "Visão estratégica das operações do EcoAçaí."
        ),
    ) -> None:
        super().__init__()

        self.padding = Spacing.XL
        self.border_radius = Radius.XL
        self.bgcolor = Colors.Brand.PRIMARY

        self.content = ft.Column(
            spacing=Spacing.LG,
            controls=[
                self._criar_linha_superior(
                    titulo=titulo,
                    descricao=descricao,
                ),
                self._criar_resumo(
                    total_estabelecimentos=total_estabelecimentos,
                    total_solicitacoes=total_solicitacoes,
                    total_sacas=total_sacas,
                    total_kg=total_kg,
                ),
            ],
        )

    @staticmethod
    def _criar_indicador(
        titulo: str,
        valor: str,
        icone: str,
        cor: str,
    ) -> ft.Control:
        return ft.Container(
            padding=ft.Padding(
                left=16,
                top=10,
                right=16,
                bottom=10,
            ),
            border_radius=Radius.LG,
            bgcolor=ft.Colors.with_opacity(
                0.12,
                Colors.Text.ON_PRIMARY,
            ),
            content=ft.Row(
                tight=True,
                spacing=Spacing.MD,
                controls=[
                    ft.Icon(
                        icone,
                        color=cor,
                        size=22,
                    ),
                    ft.Column(
                        tight=True,
                        spacing=Spacing.XS,
                        controls=[
                            ft.Text(
                                titulo,
                                size=Typography.LABEL,
                                color=ft.Colors.with_opacity(
                                    0.70,
                                    Colors.Text.ON_PRIMARY,
                                ),
                            ),
                            ft.Text(
                                valor,
                                size=Typography.H4,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.Text.ON_PRIMARY,
                            ),
                        ],
                    ),
                ],
            ),
        )

    @staticmethod
    def _criar_linha_superior(
        titulo: str,
        descricao: str,
    ) -> ft.Control:
        data_hora = datetime.now().strftime(
            "%d/%m/%Y às %H:%M"
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
                        spacing=Spacing.SM,
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
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=Spacing.MD,
                        controls=[
                            ft.Icon(
                                ft.Icons.CALENDAR_MONTH,
                                color=ft.Colors.with_opacity(
                                    0.70,
                                    Colors.Text.ON_PRIMARY,
                                ),
                                size=18,
                            ),
                            ft.Text(
                                data_hora,
                                size=Typography.SMALL,
                                color=ft.Colors.with_opacity(
                                    0.70,
                                    Colors.Text.ON_PRIMARY,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )

    def _criar_resumo(
        self,
        total_estabelecimentos: str,
        total_solicitacoes: str,
        total_sacas: str,
        total_kg: str,
    ) -> ft.Control:
        dados = [
            (
                "Estabelecimentos",
                total_estabelecimentos,
                ft.Icons.STORE,
                Colors.Dashboard.ESTABLISHMENTS_BG,
            ),
            (
                "Solicitações",
                total_solicitacoes,
                ft.Icons.ASSIGNMENT,
                Colors.Dashboard.REQUESTS_BG,
            ),
            (
                "Sacas",
                total_sacas,
                ft.Icons.INVENTORY_2,
                Colors.Dashboard.SACKS_BG,
            ),
            (
                "Peso registrado",
                f"{total_kg} kg",
                ft.Icons.SCALE,
                Colors.Dashboard.WEIGHT_BG,
            ),
        ]

        return ft.ResponsiveRow(
            spacing=Spacing.MD,
            run_spacing=Spacing.MD,
            controls=[
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 3,
                    },
                    content=self._criar_indicador(
                        titulo=titulo,
                        valor=valor,
                        icone=icone,
                        cor=cor,
                    ),
                )
                for titulo, valor, icone, cor in dados
            ],
        )