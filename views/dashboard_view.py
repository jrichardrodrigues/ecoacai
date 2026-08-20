from datetime import date, datetime

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

    def __init__(
            self,
            page: ft.Page,
            on_abrir_solicitacoes=None,
            on_abrir_agendadas=None,
            on_abrir_em_coleta=None,
            on_abrir_concluidas=None,
            on_abrir_canceladas=None,
            on_abrir_para_hoje=None,
            on_abrir_todas_solicitacoes=None,
            on_abrir_solicitantes=None,
    ) -> None:
        self.page = page
        self.on_abrir_solicitacoes = on_abrir_solicitacoes
        self.on_abrir_agendadas = on_abrir_agendadas
        self.on_abrir_em_coleta = on_abrir_em_coleta
        self.on_abrir_concluidas = on_abrir_concluidas
        self.on_abrir_canceladas = on_abrir_canceladas
        self.on_abrir_para_hoje = on_abrir_para_hoje
        self.on_abrir_todas_solicitacoes = on_abrir_todas_solicitacoes
        self.on_abrir_solicitantes = on_abrir_solicitantes


        self.controller = DashboardController()

        self.data_inicial: str | None = None
        self.data_final: str | None = None

        self.campo_data_inicial = ft.TextField(
            label="Data inicial",
            hint_text="dd/mm/aaaa",
            width=180,
            dense=True,
            read_only=True,
            on_click=self._abrir_data_inicial,
        )

        self.campo_data_final = ft.TextField(
            label="Data final",
            hint_text="dd/mm/aaaa",
            width=180,
            dense=True,
            read_only=True,
            on_click=self._abrir_data_final,
        )

        self.estatisticas = self.controller.obter_estatisticas(
            data_inicial=self.data_inicial,
            data_final=self.data_final,
        )

        self.conteudo_dashboard = ft.Column(
            spacing=Spacing.LG,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )

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
    def _formatar_duracao(
        minutos: int | float | None,
    ) -> str:
        """Formata uma duração em minutos para leitura amigável."""

        if minutos is None or minutos <= 0:
            return "0 min"

        total_minutos = int(round(minutos))

        dias, restante = divmod(
            total_minutos,
            1440,
        )

        horas, minutos_restantes = divmod(
            restante,
            60,
        )

        partes: list[str] = []

        if dias > 0:
            partes.append(
                f"{dias}d"
            )

        if horas > 0:
            partes.append(
                f"{horas}h"
            )

        if minutos_restantes > 0 or not partes:
            partes.append(
                f"{minutos_restantes}min"
            )

        return " ".join(partes)

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
            height: int = 200,
            on_click=None,
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
                height=height,
            ),
            on_click=on_click,
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
            canceladas: int,
            recusadas: int,
    ) -> ft.Control:
        """Cria o painel executivo de distribuição por status."""

        pendentes = pendentes or 0
        agendadas = agendadas or 0
        em_coleta = em_coleta or 0
        concluidas = concluidas or 0
        canceladas = canceladas or 0
        recusadas = recusadas or 0

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
            (
                "Canceladas",
                canceladas,
                ft.Icons.CANCEL,
                ft.Colors.GREY_700,
                ft.Colors.GREY_100,
            ),
            (
                "Recusadas",
                recusadas,
                ft.Icons.BLOCK,
                ft.Colors.PURPLE_700,
                ft.Colors.PURPLE_50,
            ),
        ]

        total = sum(
            valor
            for _, valor, _, _, _ in dados
        )

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
                    radius=108,
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
                center_space_radius=68,
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
                    self._criar_card_status_grafico(
                        titulo=dados[5][0],
                        valor=dados[5][1],
                        total=total,
                        icone=dados[5][2],
                        cor=dados[5][3],
                        cor_fundo=dados[5][4],
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
                    self._criar_card_status_grafico(
                        titulo=dados[4][0],
                        valor=dados[4][1],
                        total=total,
                        icone=dados[4][2],
                        cor=dados[4][3],
                        cor_fundo=dados[4][4],
                    ),
                ],
            )

            area_grafico = ft.Container(
                width=500,
                height=380,
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
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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

    def _criar_grafico_evolucao(
            self,
            dados: list[dict],
    ) -> ft.Control:
        """Cria o gráfico de evolução das solicitações."""

        if not dados:
            return ft.Container(
                height=300,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    "Não há dados para o período selecionado.",
                ),
            )

        pontos_solicitacoes: list[fch.LineChartDataPoint] = []
        pontos_concluidas: list[fch.LineChartDataPoint] = []

        for indice, item in enumerate(dados):
            pontos_solicitacoes.append(
                fch.LineChartDataPoint(
                    indice,
                    item.get("solicitacoes", 0),
                )
            )

            pontos_concluidas.append(
                fch.LineChartDataPoint(
                    indice,
                    item.get("concluidas", 0),
                )
            )

        maior_valor = max(
            max(
                item.get("solicitacoes", 0),
                item.get("concluidas", 0),
            )
            for item in dados
        )

        max_y = max(
            maior_valor + 1,
            5,
        )

        series = [
            fch.LineChartData(
                points=pontos_solicitacoes,
                color=ft.Colors.BLUE_600,
                stroke_width=3,
                curved=False,
                point=True,
            ),
            fch.LineChartData(
                points=pontos_concluidas,
                color=ft.Colors.GREEN_600,
                stroke_width=3,
                curved=False,
                point=True,
            ),
        ]

        labels_datas = []

        quantidade_dias = len(dados)

        if quantidade_dias <= 15:
            passo_rotulo = 1
        elif quantidade_dias <= 31:
            passo_rotulo = 2
        elif quantidade_dias <= 62:
            passo_rotulo = 5
        else:
            passo_rotulo = 7

        for indice, item in enumerate(dados):

            # Reduz apenas os rótulos visíveis no eixo X.
            # Todos os pontos continuam sendo desenhados no gráfico.
            exibir_rotulo = (
                    indice % passo_rotulo == 0
                    or indice == quantidade_dias - 1
            )

            if not exibir_rotulo:
                continue

            data = item.get("data", "")

            if data:
                partes = data.split("-")

                if len(partes) == 3:
                    data_formatada = (
                        f"{partes[2]}/{partes[1]}"
                    )
                else:
                    data_formatada = data
            else:
                data_formatada = ""

            labels_datas.append(
                fch.ChartAxisLabel(
                    value=indice,
                    label=ft.Text(
                        data_formatada,
                        size=11,
                        color=ft.Colors.GREY_700,
                    ),
                )
            )

        labels_y = [
            fch.ChartAxisLabel(
                value=valor,
                label=ft.Text(
                    str(valor),
                    size=11,
                    color=ft.Colors.GREY_700,
                ),
            )
            for valor in range(
                0,
                int(max_y) + 1,
            )
        ]

        grafico = fch.LineChart(
            data_series=series,
            bottom_axis=fch.ChartAxis(
                labels=labels_datas,
                label_size=32,
                show_min=True,
                show_max=True,
            ),
            left_axis=fch.ChartAxis(
                labels=labels_y,
                label_size=32,
                show_min=True,
                show_max=True,
            ),
            min_x=0,
            max_x=max(
                len(dados) - 1,
                1,
            ),
            min_y=0,
            max_y=max_y,
            interactive=True,
            expand=True,
        )

        return ft.Container(
            padding=20,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_200,
            ),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Evolução das solicitações",
                                size=16,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CIRCLE,
                                        size=10,
                                        color=ft.Colors.BLUE_600,
                                    ),
                                    ft.Text(
                                        "Solicitações",
                                        size=12,
                                        color=ft.Colors.GREY_700,
                                    ),
                                    ft.Icon(
                                        ft.Icons.CIRCLE,
                                        size=10,
                                        color=ft.Colors.GREEN_600,
                                    ),
                                    ft.Text(
                                        "Concluídas",
                                        size=12,
                                        color=ft.Colors.GREY_700,
                                    ),
                                ],
                                spacing=6,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(
                        height=280,
                        content=grafico,
                    ),
                ],
                spacing=16,
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
            total_canceladas: int,
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
                "on_click": self.on_abrir_todas_solicitacoes,
            },
            {
                "titulo": "Solicitantes",
                "valor": self._formatar_numero(total_estabelecimentos),
                "icone": ft.Icons.STORE,
                "cor": ft.Colors.CYAN_700,
                "cor_fundo": ft.Colors.CYAN_50,
                "subtitulo": "Total cadastrados",
                "col": {"sm": 12, "md": 6, "lg": 3},
                "on_click": self.on_abrir_solicitantes,
            },
            {
                "titulo": "Pendentes",
                "valor": self._formatar_numero(total_pendentes),
                "icone": ft.Icons.PENDING_ACTIONS,
                "cor": ft.Colors.AMBER_800,
                "cor_fundo": ft.Colors.AMBER_50,
                "subtitulo": "Aguardando atendimento",
                "col": {"sm": 12, "md": 6, "lg": 3},
                "on_click": self.on_abrir_solicitacoes,
            },
            {
                "titulo": "Agendadas",
                "valor": self._formatar_numero(total_agendadas),
                "icone": ft.Icons.EVENT_AVAILABLE,
                "cor": ft.Colors.PURPLE_700,
                "cor_fundo": ft.Colors.PURPLE_50,
                "subtitulo": "Coletas programadas",
                "col": {"sm": 12, "md": 6, "lg": 3},
                "on_click": self.on_abrir_agendadas,
            },
            {
                "titulo": "Para hoje",
                "valor": self._formatar_numero(total_hoje),
                "icone": ft.Icons.TODAY,
                "cor": ft.Colors.INDIGO_700,
                "cor_fundo": ft.Colors.INDIGO_50,
                "subtitulo": "Coletas previstas hoje",
                "col": {"sm": 12, "md": 6, "lg": 3},
                "on_click": self.on_abrir_para_hoje,
            },
            {
                "titulo": "Em coleta",
                "valor": self._formatar_numero(total_em_coleta),
                "icone": ft.Icons.LOCAL_SHIPPING,
                "cor": ft.Colors.DEEP_ORANGE_700,
                "cor_fundo": ft.Colors.DEEP_ORANGE_50,
                "subtitulo": "Coletas em andamento",
                "col": {"sm": 12, "md": 6, "lg": 3},
                "on_click": self.on_abrir_em_coleta,
            },
            {
                "titulo": "Concluídas",
                "valor": self._formatar_numero(total_concluidas),
                "icone": ft.Icons.CHECK_CIRCLE,
                "cor": ft.Colors.GREEN_700,
                "cor_fundo": ft.Colors.GREEN_50,
                "subtitulo": "Coletas finalizadas",
                "col": {"sm": 12, "md": 6, "lg": 3},
                "on_click": self.on_abrir_concluidas,
            },
            {
                "titulo": "Canceladas",
                "valor": self._formatar_numero(total_canceladas),
                "icone": ft.Icons.CANCEL,
                "cor": ft.Colors.RED_700,
                "cor_fundo": ft.Colors.RED_50,
                "subtitulo": "Solicitações canceladas",
                "col": {"sm": 12, "md": 6, "lg": 3},
                "on_click": self.on_abrir_canceladas,
            },
        ]

    def _obter_cards_totais(
            self,
            total_sacas: int,
            total_bags: int,
            total_kg: int | float,
    ) -> list[dict]:
        """Retorna os dados dos cards de volumes."""
        return [
            {
                "titulo": "Sacas coletadas",
                "valor": f"{self._formatar_numero(total_sacas)} sacas",
                "icone": ft.Icons.INVENTORY_2,
                "cor": Colors.Dashboard.SACKS,
                "cor_fundo": Colors.Dashboard.SACKS_BG,
                "subtitulo": "Volumes coletados em sacas",
                "col": {"sm": 12, "md": 4},
            },
            {
                "titulo": "Bags coletados",
                "valor": f"{self._formatar_numero(total_bags)} bags",
                "icone": ft.Icons.INVENTORY,
                "cor": ft.Colors.TEAL_700,
                "cor_fundo": ft.Colors.TEAL_50,
                "subtitulo": "Volumes coletados em bags",
                "col": {"sm": 12, "md": 4},
            },
            {
                "titulo": "Peso coletado",
                "valor": f"{self._formatar_numero(total_kg)} kg",
                "icone": ft.Icons.SCALE,
                "cor": Colors.Dashboard.WEIGHT,
                "cor_fundo": Colors.Dashboard.WEIGHT_BG,
                "subtitulo": "Peso efetivamente coletado",
                "col": {"sm": 12, "md": 4},
            },
        ]

    @staticmethod
    def _converter_data_filtro(valor: str) -> str | None:
        """Converte dd/mm/aaaa para aaaa-mm-dd."""

        texto = str(valor or "").strip()

        if not texto:
            return None

        try:
            data = datetime.strptime(
                texto,
                "%d/%m/%Y",
            )
        except ValueError as erro:
            raise ValueError(
                "Informe a data no formato dd/mm/aaaa."
            ) from erro

        return data.strftime("%Y-%m-%d")

    def _aplicar_filtro(
            self,
            _evento: ft.Event,
    ) -> None:
        """Aplica o período informado ao Dashboard."""

        try:
            self.data_inicial = self._converter_data_filtro(
                self.campo_data_inicial.value
            )

            self.data_final = self._converter_data_filtro(
                self.campo_data_final.value
            )

            if (
                    self.data_inicial
                    and self.data_final
                    and self.data_inicial > self.data_final
            ):
                raise ValueError(
                    "A data inicial não pode ser maior que a data final."
                )

            self.estatisticas = (
                self.controller.obter_estatisticas(
                    data_inicial=self.data_inicial,
                    data_final=self.data_final,
                )
            )

            self.conteudo_dashboard.controls = (
                self._montar_conteudo_dashboard()
            )

            self.page.update()

        except ValueError as erro:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    str(erro)
                )
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _limpar_filtro(
        self,
        _evento: ft.Event,
    ) -> None:
        """Remove o período e restaura o Dashboard completo."""

        self.data_inicial = None
        self.data_final = None

        self.campo_data_inicial.value = ""
        self.campo_data_final.value = ""

        self.estatisticas = (
            self.controller.obter_estatisticas(
                data_inicial=None,
                data_final=None,
            )
        )

        self.conteudo_dashboard.controls = (
            self._montar_conteudo_dashboard()
        )

        self.page.update()

    def _abrir_data_inicial(
            self,
            _evento: ft.Event,
    ) -> None:
        """Abre o calendário para selecionar a data inicial."""

        hoje = date.today()

        data_selecionada = hoje

        if self.campo_data_inicial.value:
            try:
                data_selecionada = datetime.strptime(
                    self.campo_data_inicial.value,
                    "%d/%m/%Y",
                ).date()
            except ValueError:
                data_selecionada = hoje

        seletor = ft.DatePicker(
            value=data_selecionada,
            first_date=date(2020, 1, 1),
            last_date=date(
                hoje.year + 2,
                12,
                31,
            ),
            on_change=self._selecionar_data_inicial,
        )

        self.page.show_dialog(seletor)

    def _selecionar_data_inicial(
        self,
        evento: ft.Event,
    ) -> None:
        """Atualiza o campo de data inicial."""

        valor = evento.control.value

        if valor is None:
            return

        self.campo_data_inicial.value = (
            valor.strftime("%d/%m/%Y")
        )

        self.page.update()

    def _abrir_data_final(
            self,
            _evento: ft.Event,
    ) -> None:
        """Abre o calendário para selecionar a data final."""

        hoje = date.today()

        data_selecionada = hoje

        if self.campo_data_final.value:
            try:
                data_selecionada = datetime.strptime(
                    self.campo_data_final.value,
                    "%d/%m/%Y",
                ).date()
            except ValueError:
                data_selecionada = hoje

        seletor = ft.DatePicker(
            value=data_selecionada,
            first_date=date(2020, 1, 1),
            last_date=date(
                hoje.year + 2,
                12,
                31,
            ),
            on_change=self._selecionar_data_final,
        )

        self.page.show_dialog(seletor)

    def _selecionar_data_final(
        self,
        evento: ft.Event,
    ) -> None:
        """Atualiza o campo de data final."""

        valor = evento.control.value

        if valor is None:
            return

        self.campo_data_final.value = (
            valor.strftime("%d/%m/%Y")
        )

        self.page.update()

    def _montar_conteudo_dashboard(
            self,
    ) -> list[ft.Control]:
        """Monta os controles internos do Dashboard."""
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

        tempo_medio_atendimento = self.estatisticas.get(
            "tempo_medio_atendimento",
            0,
        )

        tempo_medio_coleta = self.estatisticas.get(
            "tempo_medio_coleta",
            0,
        )

        tempo_medio_espera = self.estatisticas.get(
            "tempo_medio_espera",
            0,
        )

        taxa_cumprimento_agendamento = self.estatisticas.get(
            "taxa_cumprimento_agendamento",
            0,
        )

        eficiencia_volume_coletado = self.estatisticas.get(
            "eficiencia_volume_coletado",
            0,
        )

        evolucao_solicitacoes = self.estatisticas.get(
            "evolucao_solicitacoes",
            [],
        )

        taxa_conclusao = (
            (concluidas / total) * 100
            if total > 0
            else 0
        )

        total_sacas = self.estatisticas.get(
            "sacas_coletadas",
            0,
        )

        total_bags = self.estatisticas.get(
            "bags_coletados",
            0,
        )

        total_kg = self.estatisticas.get(
            "kg_coletados",
            0,
        )

        canceladas = self.estatisticas.get(
            "canceladas",
            0,
        )

        recusadas = self.estatisticas.get(
            "recusadas",
            0,
        )

        ultimas_solicitacoes = self.controller.listar_ultimas(
            limite=5,
            data_inicial=self.data_inicial,
            data_final=self.data_final,
        )

        cards_status_data = self._obter_cards_status(
            total_solicitacoes=total,
            total_estabelecimentos=total_estabelecimentos,
            total_pendentes=pendentes,
            total_agendadas=agendadas,
            total_hoje=coletas_hoje,
            total_em_coleta=em_coleta,
            total_concluidas=concluidas,
            total_canceladas=canceladas,
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
            total_bags=total_bags,
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

        cards_desempenho = ft.ResponsiveRow(
            spacing=Spacing.MD,
            run_spacing=Spacing.MD,
            controls=[
                self._criar_container_card(
                    titulo="Tempo médio de atendimento",
                    valor=self._formatar_duracao(
                        tempo_medio_atendimento
                    ),
                    icone=ft.Icons.SCHEDULE,
                    cor=ft.Colors.INDIGO_700,
                    cor_fundo=ft.Colors.INDIGO_50,
                    subtitulo="Da solicitação até a conclusão da coleta",
                    height=220,
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 2,
                    },
                ),
                self._criar_container_card(
                    titulo="Tempo médio de espera",
                    valor=self._formatar_duracao(
                        tempo_medio_espera
                    ),
                    icone=ft.Icons.HOURGLASS_EMPTY,
                    cor=ft.Colors.AMBER_800,
                    cor_fundo=ft.Colors.AMBER_50,
                    subtitulo="Da solicitação até a chegada ao local da coleta",
                    height=220,
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 2,
                    },
                ),
                self._criar_container_card(
                    titulo="Tempo médio de coleta",
                    valor=self._formatar_duracao(
                        tempo_medio_coleta
                    ),
                    icone=ft.Icons.TIMER_OUTLINED,
                    cor=ft.Colors.BLUE_700,
                    cor_fundo=ft.Colors.BLUE_50,
                    subtitulo="Da chegada ao local da coleta até a conclusão",
                    height=220,
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 2,
                    },
                ),
                self._criar_container_card(
                    titulo="Taxa de conclusão",
                    valor=(
                        f"{taxa_conclusao:.1f}%"
                        .replace(".", ",")
                    ),
                    icone=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    cor=ft.Colors.GREEN_700,
                    cor_fundo=ft.Colors.GREEN_50,
                    subtitulo="Percentual das solicitações concluídas",
                    height=220,
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 2,
                    },
                ),
                self._criar_container_card(
                    titulo="Cumprimento do agendamento",
                    valor=(
                        f"{taxa_cumprimento_agendamento:.1f}%"
                        .replace(".", ",")
                    ),
                    icone=ft.Icons.EVENT_AVAILABLE,
                    cor=ft.Colors.TEAL_700,
                    cor_fundo=ft.Colors.TEAL_50,
                    subtitulo="Chegada até 15 min após o agendado",
                    height=220,
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 2,
                    },
                ),
                self._criar_container_card(
                    titulo="Eficiência do volume coletado",
                    valor=(
                        f"{eficiencia_volume_coletado:.1f}%"
                        .replace(".", ",")
                    ),
                    icone=ft.Icons.SCALE,
                    cor=ft.Colors.PURPLE_700,
                    cor_fundo=ft.Colors.PURPLE_50,
                    subtitulo="Peso coletado em relação ao previsto",
                    height=220,
                    col={
                        "sm": 12,
                        "md": 6,
                        "lg": 2,
                    },
                ),
            ],
        )

        painel_evolucao = self._criar_grafico_evolucao(
            evolucao_solicitacoes,
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
            canceladas=canceladas,
            recusadas=recusadas,
        )

        filtro_periodo = ft.Container(
            padding=16,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            border_radius=Radius.LG,
            bgcolor=ft.Colors.WHITE,
            content=ft.Row(
                controls=[
                    self.campo_data_inicial,
                    self.campo_data_final,
                    ft.FilledButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.FILTER_ALT,
                                    size=18,
                                ),
                                ft.Text("Aplicar"),
                            ],
                            spacing=8,
                            tight=True,
                        ),
                        on_click=self._aplicar_filtro,
                    ),
                    ft.OutlinedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.CLEAR,
                                    size=18,
                                ),
                                ft.Text("Limpar"),
                            ],
                            spacing=8,
                            tight=True,
                        ),
                        on_click=self._limpar_filtro,
                    ),
                ],
                spacing=12,
                wrap=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        return [
            cabecalho_executivo,
            filtro_periodo,
            Section(
                title="Solicitações",
                content=cards_status,
            ),
            Section(
                title="Volumes registrados",
                content=cards_totais,
            ),
            Section(
                title="Desempenho operacional",
                content=cards_desempenho,
            ),
            painel_evolucao,
            painel_distribuicao,
            DashboardTable(
                solicitacoes=ultimas_solicitacoes,
            ),
        ]

    def build(self) -> ft.Control:
        """Constrói e retorna o Dashboard."""

        self.conteudo_dashboard.controls = (
            self._montar_conteudo_dashboard()
        )

        return ft.Column(
            controls=[
                self.conteudo_dashboard,
            ],
            spacing=Spacing.LG,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )