import flet as ft
import flet_charts as fch

from components.dashboard import (
    DashboardTable,
    ExecutiveCard,
    ExecutiveHeader,
)
from controllers import DashboardController
from components.theme import (
    Colors,
    Typography,
    Spacing,
    Radius,
    Shadows,
)
from components.layout import Section, SectionHeader

class DashboardView:
    """Dashboard com indicadores e gráficos das solicitações."""

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.controller = DashboardController()
        self.estatisticas = self.controller.obter_estatisticas()

    @staticmethod
    def _formatar_numero(valor: int | float | None) -> str:
        """Formata números no padrão brasileiro."""
        if valor is None:
            return "0"

        if isinstance(valor, float):
            return (
                f"{valor:,.1f}"
                .replace(",", "_")
                .replace(".", ",")
                .replace("_", ".")
            )

        return f"{valor:,}".replace(",", ".")

    @staticmethod
    def _criar_item_legenda(texto: str, valor: int, cor: str) -> ft.Control:
        """Cria um item da legenda do gráfico."""
        return ft.Row(
            tight=True,
            spacing=Spacing.SM,
            controls=[
                ft.Container(
                    width=12,
                    height=12,
                    border_radius=Radius.SM,
                    bgcolor=cor,
                ),
                ft.Text(
                    f"{texto}: {valor}",
                    size=Typography.SMALL,
                    color=Colors.Text.SECONDARY,
                ),
            ],
        )

    @staticmethod
    def _criar_container_card(
        titulo: str,
        valor: str,
        icone: str,
        cor: str,
        cor_fundo: str,
        subtitulo: str = "",
        col: dict | None = None,
    ) -> ft.Control:
        """Cria um card executivo dentro da grade responsiva."""
        return ft.Container(
            col=col or {
                "sm": 12,
                "md": 6,
                "lg": 4,
            },
            content=ExecutiveCard(
                titulo=titulo,
                valor=valor,
                icone=icone,
                cor=cor,
                cor_fundo=cor_fundo,
                subtitulo=subtitulo,
            ),
        )

    def _criar_grafico_status(
        self,
        pendentes: int,
        agendadas: int,
        em_coleta: int,
        concluidas: int,
    ) -> ft.Control:
        """Cria o gráfico de distribuição por status."""
        dados = [
            ("Pendentes", pendentes, ft.Colors.ORANGE_500),
            ("Agendadas", agendadas, ft.Colors.BLUE_500),
            ("Em coleta", em_coleta, ft.Colors.DEEP_ORANGE_500),
            ("Concluídas", concluidas, ft.Colors.GREEN_600),
        ]

        total = sum(valor for _, valor, _ in dados)

        if total == 0:
            return ft.Container(
                height=Spacing.DASHBOARD_CARD_HEIGHT,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.Icon(
                            ft.Icons.PIE_CHART_OUTLINE,
                            size=52,
                            color=ft.Colors.GREY_500,
                        ),
                        ft.Text(
                            "Ainda não existem dados para o gráfico.",
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),
            )

        secoes = [
            fch.PieChartSection(
                value=valor,
                title=str(valor),
                color=cor,
                radius=72,
                title_style=ft.TextStyle(
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            )
            for _, valor, cor in dados
            if valor > 0
        ]

        grafico = fch.PieChart(
            sections=secoes,
            sections_space=3,
            center_space_radius=48,
            center_space_color=ft.Colors.WHITE,
            expand=True,
        )

        legenda = ft.ResponsiveRow(
            spacing=12,
            run_spacing=10,
            controls=[
                ft.Container(
                    col={"sm": 12, "md": 6, "lg": 3},
                    content=self._criar_item_legenda(texto, valor, cor),
                )
                for texto, valor, cor in dados
            ],
        )

        return ft.Column(
            spacing=Spacing.LG,
            controls=[
                ft.Container(height=Spacing.DASHBOARD_CARD_HEIGHT, content=grafico),
                legenda,
            ],
        )

    def _obter_cards_status(
            self,
            total_solicitacoes: int,
            total_estabelecimentos: int,
            total_pendentes: int,
            total_agendadas: int,
            total_hoje: int,
            total_em_coleta: int,
            total_concluidas: int,
    ) -> list[dict]:
        return [
            {
                "titulo": "Solicitações",
                "valor": self._formatar_numero(total_solicitacoes),
                "icone": ft.Icons.ASSIGNMENT,
                "cor": Colors.Dashboard.REQUESTS,
                "cor_fundo": Colors.Dashboard.REQUESTS_BG,
                "subtitulo": "Total de solicitações",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Estabelecimentos",
                "valor": self._formatar_numero(total_estabelecimentos),
                "icone": ft.Icons.STORE,
                "cor": Colors.Dashboard.ESTABLISHMENTS,
                "cor_fundo": Colors.Dashboard.ESTABLISHMENTS_BG,
                "subtitulo": "Total cadastrados",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Pendentes",
                "valor": self._formatar_numero(total_pendentes),
                "icone": ft.Icons.PENDING_ACTIONS,
                "cor": Colors.Dashboard.PENDING,
                "cor_fundo": Colors.Dashboard.PENDING_BG,
                "subtitulo": "Aguardando atendimento",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Agendadas",
                "valor": self._formatar_numero(total_agendadas),
                "icone": ft.Icons.EVENT_AVAILABLE,
                "cor": Colors.Dashboard.SCHEDULED,
                "cor_fundo": Colors.Dashboard.SCHEDULED_BG,
                "subtitulo": "Coletas programadas",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Para hoje",
                "valor": self._formatar_numero(total_hoje),
                "icone": ft.Icons.TODAY,
                "cor": Colors.Dashboard.TODAY,
                "cor_fundo": Colors.Dashboard.TODAY_BG,
                "subtitulo": "Coletas previstas hoje",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Em coleta",
                "valor": self._formatar_numero(total_em_coleta),
                "icone": ft.Icons.LOCAL_SHIPPING,
                "cor": Colors.Dashboard.COLLECTING,
                "cor_fundo": Colors.Dashboard.COLLECTING_BG,
                "subtitulo": "Coletas em andamento",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Concluídas",
                "valor": self._formatar_numero(total_concluidas),
                "icone": ft.Icons.CHECK_CIRCLE,
                "cor": Colors.Dashboard.COMPLETED,
                "cor_fundo": Colors.Dashboard.COMPLETED_BG,
                "subtitulo": "Coletas finalizadas",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
        ]

    def _obter_cards_totais(
            self,
            total_sacas: int,
            total_kg: int,
    ) -> list[dict]:
        return [
            {
                "titulo": "Total de sacas",
                "valor": f"{self._formatar_numero(total_sacas)} sacas",
                "icone": ft.Icons.INVENTORY_2,
                "cor": Colors.Dashboard.SACKS,
                "cor_fundo": Colors.Dashboard.SACKS_BG,
                "subtitulo": "Volume total registrado",
                "col": {"sm": 12, "md": 6},
            },
            {
                "titulo": "Peso coletado",
                "valor": f"{self._formatar_numero(total_kg)} kg",
                "icone": ft.Icons.SCALE,
                "cor": Colors.Dashboard.WEIGHT,
                "cor_fundo": Colors.Dashboard.WEIGHT_BG,
                "subtitulo": "Peso acumulado das solicitações",
                "col": {"sm": 12, "md": 6},
            },
        ]

    def build(self) -> ft.Control:
        """Constrói e retorna o Dashboard."""
        total = self.estatisticas.get("total", 0)
        total_estabelecimentos = self.estatisticas.get(
            "total_estabelecimentos", 0
        )
        pendentes = self.estatisticas.get("pendentes", 0)
        agendadas = self.estatisticas.get("agendadas", 0)
        coletas_hoje = self.estatisticas.get("coletas_hoje", 0)
        em_coleta = self.estatisticas.get("em_coleta", 0)
        concluidas = self.estatisticas.get("concluidas", 0)
        total_sacas = self.estatisticas.get("total_sacas", 0)
        total_kg = self.estatisticas.get("total_kg", 0)

        ultimas_solicitacoes = self.controller.listar_ultimas(limite=5)

        cards_status_data = self._obter_cards_status(
            total_solicitacoes=total,
            total_estabelecimentos=total_estabelecimentos,
            total_pendentes=pendentes,
            total_agendadas=agendadas,
            total_hoje=coletas_hoje,
            total_em_coleta=em_coleta,
            total_concluidas=concluidas,
        )

        cards_status = ft.ResponsiveRow(
            spacing=Spacing.MD,
            run_spacing=Spacing.MD,
            controls=[
                self._criar_container_card(**card)
                for card in cards_status_data
            ],
        )

        cards_totais_data = self._obter_cards_totais(
            total_sacas=total_sacas,
            total_kg=total_kg,
        )

        cards_totais = ft.ResponsiveRow(
            spacing=Spacing.MD,
            run_spacing=Spacing.MD,
            controls=[
                self._criar_container_card(**card)
                for card in cards_totais_data
            ],
        )

        cabecalho_executivo = ExecutiveHeader(
            total_estabelecimentos=self._formatar_numero(
                total_estabelecimentos
            ),
            total_solicitacoes=self._formatar_numero(total),
            total_sacas=self._formatar_numero(total_sacas),
            total_kg=self._formatar_numero(total_kg),
        )

        grafico_status = ft.Container(
            padding=Spacing.CARD_PADDING,
            border_radius=Radius.CARD,
            bgcolor=Colors.Dashboard.CHART_BACKGROUND,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            content=self._criar_grafico_status(
                pendentes=pendentes,
                agendadas=agendadas,
                em_coleta=em_coleta,
                concluidas=concluidas,
            ),
        )

        return ft.Column(
            controls=[
                cabecalho_executivo,

                Section(
                    title="Solicitações",
                    content=cards_status,
                ),

                Section(
                    title="Volumes registrados",
                    content=cards_totais,
                ),

                Section(
                    title="Distribuição das solicitações",
                    content=grafico_status,
                ),

                DashboardTable(solicitacoes=ultimas_solicitacoes),
            ],
            spacing=Spacing.LG,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )