from datetime import datetime

import flet as ft


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

        self.padding = 24
        self.border_radius = 16
        self.bgcolor = ft.Colors.GREEN_800
        self.content = ft.Column(
            spacing=18,
            controls=[
                self._criar_linha_superior(
                    titulo=titulo,
                    descricao=descricao,
                ),
                self._criar_resumo(
                    total_estabelecimentos=(
                        total_estabelecimentos
                    ),
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
            padding=ft.Padding.symmetric(
                horizontal=14,
                vertical=10,
            ),
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(
                0.12,
                ft.Colors.WHITE,
            ),
            content=ft.Row(
                tight=True,
                spacing=9,
                controls=[
                    ft.Icon(
                        icone,
                        color=cor,
                        size=22,
                    ),
                    ft.Column(
                        tight=True,
                        spacing=1,
                        controls=[
                            ft.Text(
                                titulo,
                                size=11,
                                color=ft.Colors.WHITE70,
                            ),
                            ft.Text(
                                valor,
                                size=17,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
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
                        spacing=4,
                        controls=[
                            ft.Text(
                                titulo,
                                size=27,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                descricao,
                                size=14,
                                color=ft.Colors.WHITE70,
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
                        spacing=8,
                        controls=[
                            ft.Icon(
                                ft.Icons.CALENDAR_MONTH,
                                color=ft.Colors.WHITE70,
                                size=18,
                            ),
                            ft.Text(
                                data_hora,
                                size=13,
                                color=ft.Colors.WHITE70,
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
                ft.Colors.CYAN_100,
            ),
            (
                "Solicitações",
                total_solicitacoes,
                ft.Icons.ASSIGNMENT,
                ft.Colors.BLUE_100,
            ),
            (
                "Sacas",
                total_sacas,
                ft.Icons.INVENTORY_2,
                ft.Colors.AMBER_100,
            ),
            (
                "Peso registrado",
                f"{total_kg} kg",
                ft.Icons.SCALE,
                ft.Colors.GREEN_100,
            ),
        ]

        return ft.ResponsiveRow(
            spacing=10,
            run_spacing=10,
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