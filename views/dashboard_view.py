import flet as ft
import flet_charts as fch

from components.dashboard import (
    DashboardTable,
    ExecutiveCard,
    ExecutiveHeader,
)
from controllers import DashboardController


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
            spacing=8,
            controls=[
                ft.Container(
                    width=12,
                    height=12,
                    border_radius=6,
                    bgcolor=cor,
                ),
                ft.Text(
                    f"{texto}: {valor}",
                    size=13,
                    color=ft.Colors.GREY_700,
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
                height=280,
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
            spacing=18,
            controls=[
                ft.Container(height=280, content=grafico),
                legenda,
            ],
        )

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

        cards_status = ft.ResponsiveRow(
            spacing=12,
            run_spacing=12,
            controls=[
                self._criar_container_card(
                    "Total de solicitações",
                    self._formatar_numero(total),
                    ft.Icons.ASSIGNMENT,
                    ft.Colors.BLUE_700,
                    ft.Colors.BLUE_50,
                    "Visão geral das solicitações",
                ),
                self._criar_container_card(
                    "Estabelecimentos ativos",
                    self._formatar_numero(total_estabelecimentos),
                    ft.Icons.STORE,
                    ft.Colors.TEAL_700,
                    ft.Colors.TEAL_50,
                    "Estabelecimentos cadastrados",
                ),
                self._criar_container_card(
                    "Pendentes",
                    self._formatar_numero(pendentes),
                    ft.Icons.SCHEDULE,
                    ft.Colors.AMBER_700,
                    ft.Colors.AMBER_50,
                    "Aguardando agendamento",
                ),
                self._criar_container_card(
                    "Agendadas",
                    self._formatar_numero(agendadas),
                    ft.Icons.EVENT,
                    ft.Colors.BLUE,
                    ft.Colors.LIGHT_BLUE_50,
                    "Coletas com data definida",
                ),
                self._criar_container_card(
                    "Coletas de hoje",
                    self._formatar_numero(coletas_hoje),
                    ft.Icons.TODAY,
                    ft.Colors.INDIGO_600,
                    ft.Colors.INDIGO_50,
                    "Programadas para hoje",
                ),
                self._criar_container_card(
                    "Em coleta",
                    self._formatar_numero(em_coleta),
                    ft.Icons.LOCAL_SHIPPING,
                    ft.Colors.ORANGE_700,
                    ft.Colors.ORANGE_50,
                    "Operações em andamento",
                ),
                self._criar_container_card(
                    "Concluídas",
                    self._formatar_numero(concluidas),
                    ft.Icons.CHECK_CIRCLE,
                    ft.Colors.GREEN_700,
                    ft.Colors.GREEN_50,
                    "Coletas finalizadas",
                ),
            ],
        )

        cards_totais = ft.ResponsiveRow(
            spacing=12,
            run_spacing=12,
            controls=[
                self._criar_container_card(
                    "Total de sacas",
                    f"{self._formatar_numero(total_sacas)} sacas",
                    ft.Icons.INVENTORY_2,
                    ft.Colors.BROWN_600,
                    ft.Colors.BROWN_50,
                    "Volume total registrado",
                    {"sm": 12, "md": 6},
                ),
                self._criar_container_card(
                    "Peso coletado",
                    f"{self._formatar_numero(total_kg)} kg",
                    ft.Icons.SCALE,
                    ft.Colors.PURPLE_600,
                    ft.Colors.PURPLE_50,
                    "Peso acumulado das solicitações",
                    {"sm": 12, "md": 6},
                ),
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
            padding=20,
            border_radius=12,
            bgcolor=ft.Colors.BLUE_GREY_50,
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
                ft.Container(height=4),
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
                ft.Divider(),
                ft.Text(
                    "Distribuição das solicitações",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                grafico_status,
                ft.Divider(),
                DashboardTable(solicitacoes=ultimas_solicitacoes),
            ],
            spacing=15,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )