import flet as ft
import flet_charts as fch

from components.dashboard import (
    DashboardTable,
    ExecutiveCard,
    ExecutiveHeader,
)
from components.layout import Section
from components.theme import (
    Colors,
    Typography,
    Spacing,
    Radius,
    Shadows,
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
    def _formatar_percentual(valor: int, total: int) -> str:
        """Formata um percentual no padrão brasileiro."""
        percentual = (valor / total * 100) if total > 0 else 0
        return f"{percentual:.1f}%".replace(".", ",")

    @staticmethod
    def _criar_item_legenda(
        texto: str,
        valor: int,
        cor: str,
    ) -> ft.Control:
        """Cria um item da legenda do gráfico."""
        return ft.Row(
            tight=True,
            spacing=Spacing.SM,
            controls=[
                ft.Container(
                    width=11,
                    height=11,
                    border_radius=Radius.SM,
                    bgcolor=cor,
                ),
                ft.Text(
                    f"{texto} ({valor})",
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
            col=col
            or {
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

    def _criar_card_status_grafico(
        self,
        titulo: str,
        valor: int,
        total: int,
        icone: str,
        cor: str,
        cor_fundo: str,
    ) -> ft.Control:
        """Cria um indicador lateral do painel de distribuição."""
        return ft.Container(
            width=180,
            height=140,
            padding=ft.Padding(
                left=14,
                top=10,
                right=14,
                bottom=10,
            ),
            border_radius=Radius.XL,
            bgcolor=cor_fundo,
            border=ft.Border.all(
                1,
                ft.Colors.with_opacity(0.18, cor),
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                controls=[
                    ft.Container(
                        width=40,
                        height=40,
                        border_radius=20,
                        bgcolor=ft.Colors.with_opacity(0.12, cor),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            icone,
                            size=22,
                            color=cor,
                        ),
                    ),
                    ft.Text(
                        str(valor),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=cor,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        titulo,
                        size=Typography.SMALL,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREY_800,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        self._formatar_percentual(valor, total),
                        size=Typography.SMALL,
                        weight=ft.FontWeight.BOLD,
                        color=cor,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    def _criar_grafico_status(
        self,
        pendentes: int,
        agendadas: int,
        em_coleta: int,
        concluidas: int,
    ) -> ft.Control:
        """Cria o painel executivo de distribuição por status."""
        dados = [
            (
                "Pendentes",
                pendentes,
                ft.Icons.SCHEDULE,
                ft.Colors.ORANGE_600,
                ft.Colors.ORANGE_50,
            ),
            (
                "Agendadas",
                agendadas,
                ft.Icons.EVENT_AVAILABLE,
                ft.Colors.BLUE_600,
                ft.Colors.BLUE_50,
            ),
            (
                "Em coleta",
                em_coleta,
                ft.Icons.LOCAL_SHIPPING,
                ft.Colors.RED_500,
                ft.Colors.RED_50,
            ),
            (
                "Concluídas",
                concluidas,
                ft.Icons.CHECK_CIRCLE,
                ft.Colors.GREEN_600,
                ft.Colors.GREEN_50,
            ),
        ]

        total = sum(valor for _, valor, _, _, _ in dados)

        if total == 0:
            conteudo_principal: ft.Control = ft.Container(
                height=320,
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
        else:
            secoes = [
                fch.PieChartSection(
                    value=valor,
                    title=(
                        f"{valor}\n"
                        f"({self._formatar_percentual(valor, total)})"
                    ),
                    color=cor,
                    radius=92,
                    title_style=ft.TextStyle(
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                )
                for _, valor, _, cor, _ in dados
                if valor > 0
            ]

            grafico = fch.PieChart(
                sections=secoes,
                sections_space=2,
                center_space_radius=58,
                center_space_color=ft.Colors.WHITE,
                expand=True,
            )

            legenda = ft.Container(
                alignment=ft.Alignment.CENTER,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    wrap=True,
                    spacing=28,
                    run_spacing=12,
                    controls=[
                        self._criar_item_legenda(
                            texto,
                            valor,
                            cor,
                        )
                        for texto, valor, _, cor, _ in dados
                    ],
                ),
            )

            coluna_esquerda = ft.Column(
                spacing=14,
                controls=[
                    self._criar_card_status_grafico(
                        titulo=dados[0][0],
                        valor=dados[0][1],
                        total=total,
                        icone=dados[0][2],
                        cor=dados[0][3],
                        cor_fundo=dados[0][4],
                    ),
                    self._criar_card_status_grafico(
                        titulo=dados[1][0],
                        valor=dados[1][1],
                        total=total,
                        icone=dados[1][2],
                        cor=dados[1][3],
                        cor_fundo=dados[1][4],
                    ),
                ],
            )

            coluna_direita = ft.Column(
                spacing=14,
                controls=[
                    self._criar_card_status_grafico(
                        titulo=dados[2][0],
                        valor=dados[2][1],
                        total=total,
                        icone=dados[2][2],
                        cor=dados[2][3],
                        cor_fundo=dados[2][4],
                    ),
                    self._criar_card_status_grafico(
                        titulo=dados[3][0],
                        valor=dados[3][1],
                        total=total,
                        icone=dados[3][2],
                        cor=dados[3][3],
                        cor_fundo=dados[3][4],
                    ),
                ],
            )

            area_grafico = ft.Container(
                width=420,
                height=320,
                padding=ft.Padding(
                    left=8,
                    top=0,
                    right=8,
                    bottom=4,
                ),
                alignment=ft.Alignment.CENTER,
                content=grafico,
            )

            conteudo_principal = ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=28,
                        controls=[
                            coluna_esquerda,
                            area_grafico,
                            coluna_direita,
                        ],
                    ),
                    legenda,
                ],
            )

        return ft.Container(
            padding=ft.Padding(
                left=24,
                top=20,
                right=24,
                bottom=20,
            ),
            border_radius=Radius.XL,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_200,
            ),
            shadow=Shadows.CARD,
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Row(
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=44,
                                height=44,
                                border_radius=Radius.LG,
                                bgcolor=ft.Colors.INDIGO_50,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(
                                    ft.Icons.PIE_CHART_OUTLINE,
                                    size=24,
                                    color=ft.Colors.INDIGO_700,
                                ),
                            ),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        "Distribuição das solicitações",
                                        size=Typography.H3,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_900,
                                    ),
                                    ft.Text(
                                        "Visão geral do status das solicitações",
                                        size=Typography.SMALL,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Divider(
                        height=1,
                        color=ft.Colors.GREY_200,
                    ),
                    conteudo_principal,
                ],
            ),
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
        """Retorna os dados dos cards de status."""
        return [
            {
                "titulo": "Solicitações",
                "valor": self._formatar_numero(total_solicitacoes),
                "icone": ft.Icons.ASSIGNMENT,
                "cor": ft.Colors.BLUE_700,
                "cor_fundo": ft.Colors.BLUE_50,
                "subtitulo": "Total de solicitações",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Estabelecimentos",
                "valor": self._formatar_numero(total_estabelecimentos),
                "icone": ft.Icons.STORE,
                "cor": ft.Colors.CYAN_700,
                "cor_fundo": ft.Colors.CYAN_50,
                "subtitulo": "Total cadastrados",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Pendentes",
                "valor": self._formatar_numero(total_pendentes),
                "icone": ft.Icons.PENDING_ACTIONS,
                "cor": ft.Colors.AMBER_800,
                "cor_fundo": ft.Colors.AMBER_50,
                "subtitulo": "Aguardando atendimento",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Agendadas",
                "valor": self._formatar_numero(total_agendadas),
                "icone": ft.Icons.EVENT_AVAILABLE,
                "cor": ft.Colors.PURPLE_700,
                "cor_fundo": ft.Colors.PURPLE_50,
                "subtitulo": "Coletas programadas",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Para hoje",
                "valor": self._formatar_numero(total_hoje),
                "icone": ft.Icons.TODAY,
                "cor": ft.Colors.INDIGO_700,
                "cor_fundo": ft.Colors.INDIGO_50,
                "subtitulo": "Coletas previstas hoje",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Em coleta",
                "valor": self._formatar_numero(total_em_coleta),
                "icone": ft.Icons.LOCAL_SHIPPING,
                "cor": ft.Colors.DEEP_ORANGE_700,
                "cor_fundo": ft.Colors.DEEP_ORANGE_50,
                "subtitulo": "Coletas em andamento",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
            {
                "titulo": "Concluídas",
                "valor": self._formatar_numero(total_concluidas),
                "icone": ft.Icons.CHECK_CIRCLE,
                "cor": ft.Colors.GREEN_700,
                "cor_fundo": ft.Colors.GREEN_50,
                "subtitulo": "Coletas finalizadas",
                "col": {"sm": 12, "md": 6, "lg": 3},
            },
        ]

    def _obter_cards_totais(
        self,
        total_sacas: int,
        total_kg: int | float,
    ) -> list[dict]:
        """Retorna os dados dos cards de volumes."""
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
            "total_estabelecimentos",
            0,
        )
        pendentes = self.estatisticas.get("pendentes", 0)
        agendadas = self.estatisticas.get("agendadas", 0)
        coletas_hoje = self.estatisticas.get("coletas_hoje", 0)
        em_coleta = self.estatisticas.get("em_coleta", 0)
        concluidas = self.estatisticas.get("concluidas", 0)
        total_sacas = self.estatisticas.get("total_sacas", 0)
        total_kg = self.estatisticas.get("total_kg", 0)

        ultimas_solicitacoes = self.controller.listar_ultimas(
            limite=5,
        )

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

        painel_distribuicao = self._criar_grafico_status(
            pendentes=pendentes,
            agendadas=agendadas,
            em_coleta=em_coleta,
            concluidas=concluidas,
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
                painel_distribuicao,
                DashboardTable(
                    solicitacoes=ultimas_solicitacoes,
                ),
            ],
            spacing=Spacing.LG,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )