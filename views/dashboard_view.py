import flet as ft

from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)


class DashboardView:
    """Dashboard com indicadores das solicitações."""

    def __init__(
        self,
        page: ft.Page,
    ) -> None:
        self.page = page
        self.controller = SolicitacaoColetaController()

        self.estatisticas = (
            self.controller.obter_estatisticas()
        )

    @staticmethod
    def _formatar_numero(
        valor: int | float | None,
    ) -> str:
        if valor is None:
            return "0"

        if isinstance(valor, float):
            return (
                f"{valor:,.1f}"
                .replace(",", "_")
                .replace(".", ",")
                .replace("_", ".")
            )

        return (
            f"{valor:,}"
            .replace(",", ".")
        )

    @staticmethod
    def _criar_card(
        titulo: str,
        valor: str,
        icone: str,
        cor: str,
    ) -> ft.Control:
        return ft.Card(
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

    def build(self) -> ft.Control:
        total = self.estatisticas.get(
            "total",
            0,
        )

        pendentes = self.estatisticas.get(
            "pendentes",
            0,
        )

        agendadas = self.estatisticas.get(
            "agendadas",
            0,
        )

        em_coleta = self.estatisticas.get(
            "em_coleta",
            0,
        )

        concluidas = self.estatisticas.get(
            "concluidas",
            0,
        )

        total_sacas = self.estatisticas.get(
            "total_sacas",
            0,
        )

        total_kg = self.estatisticas.get(
            "total_kg",
            0,
        )

        cards_status = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 4,
                    },
                    content=self._criar_card(
                        titulo="Total de solicitações",
                        valor=self._formatar_numero(total),
                        icone=ft.Icons.ASSIGNMENT,
                        cor=ft.Colors.BLUE_700,
                    ),
                ),
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 4,
                    },
                    content=self._criar_card(
                        titulo="Pendentes",
                        valor=self._formatar_numero(
                            pendentes
                        ),
                        icone=ft.Icons.SCHEDULE,
                        cor=ft.Colors.AMBER_700,
                    ),
                ),
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 4,
                    },
                    content=self._criar_card(
                        titulo="Agendadas",
                        valor=self._formatar_numero(
                            agendadas
                        ),
                        icone=ft.Icons.EVENT,
                        cor=ft.Colors.BLUE,
                    ),
                ),
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 4,
                    },
                    content=self._criar_card(
                        titulo="Em coleta",
                        valor=self._formatar_numero(
                            em_coleta
                        ),
                        icone=ft.Icons.LOCAL_SHIPPING,
                        cor=ft.Colors.ORANGE_700,
                    ),
                ),
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 4,
                    },
                    content=self._criar_card(
                        titulo="Concluídas",
                        valor=self._formatar_numero(
                            concluidas
                        ),
                        icone=ft.Icons.CHECK_CIRCLE,
                        cor=ft.Colors.GREEN_700,
                    ),
                ),
            ],
            spacing=12,
            run_spacing=12,
        )

        cards_totais = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                    },
                    content=self._criar_card(
                        titulo="Total de sacas",
                        valor=(
                            f"{self._formatar_numero(total_sacas)} "
                            "sacas"
                        ),
                        icone=ft.Icons.INVENTORY_2,
                        cor=ft.Colors.BROWN_600,
                    ),
                ),
                ft.Container(
                    col={
                        "sm": 12,
                        "md": 6,
                    },
                    content=self._criar_card(
                        titulo="Peso total",
                        valor=(
                            f"{self._formatar_numero(total_kg)} kg"
                        ),
                        icone=ft.Icons.SCALE,
                        cor=ft.Colors.PURPLE_600,
                    ),
                ),
            ],
            spacing=12,
            run_spacing=12,
        )

        return ft.Column(
            controls=[
                ft.Text(
                    "Dashboard",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Visão geral das solicitações de coleta.",
                    size=15,
                    color=ft.Colors.GREY_700,
                ),
                ft.Divider(),
                ft.Text(
                    "Solicitações",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                cards_status,
                ft.Divider(),
                ft.Text(
                    "Volumes registrados",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                cards_totais,
            ],
            spacing=15,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )