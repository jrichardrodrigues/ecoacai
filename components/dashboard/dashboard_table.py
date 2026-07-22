import flet as ft

from components.theme import (
    Typography,
    Spacing,
    Radius,
    Shadows,
)


class DashboardTable(ft.Container):
    """Painel profissional das últimas solicitações."""

    def __init__(
        self,
        solicitacoes: list[dict],
        on_ver_todas=None,
        on_visualizar=None,
        on_editar=None,
        on_excluir=None,
    ) -> None:
        super().__init__()

        self.solicitacoes = solicitacoes
        self.on_ver_todas = on_ver_todas
        self.on_visualizar = on_visualizar
        self.on_editar = on_editar
        self.on_excluir = on_excluir

        self.expand = True
        self.padding = ft.Padding(
            left=20,
            top=24,
            right=20,
            bottom=20,
        )
        self.border_radius = Radius.XL
        self.bgcolor = ft.Colors.WHITE
        self.border = ft.Border.all(
            1,
            ft.Colors.GREY_200,
        )
        self.shadow = Shadows.CARD

        linhas = self._criar_linhas()

        conteudo = (
            self._criar_tabela(linhas)
            if linhas
            else self._criar_estado_vazio()
        )

        self.content = ft.Column(
            spacing=18,
            controls=[
                self._criar_cabecalho(),
                ft.Divider(
                    height=1,
                    color=ft.Colors.GREY_200,
                ),
                conteudo,
                ft.Divider(
                    height=1,
                    color=ft.Colors.GREY_200,
                ),
                self._criar_rodape(),
            ],
        )

    def _criar_cabecalho(self) -> ft.Control:
        """Cria o cabeçalho executivo do painel."""

        botao_ver_todas = ft.Container(
            height=40,
            padding=ft.Padding(
                left=14,
                top=0,
                right=10,
                bottom=0,
            ),
            border_radius=Radius.LG,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            alignment=ft.Alignment.CENTER,
            ink=True,
            on_click=self.on_ver_todas,
            content=ft.Row(
                tight=True,
                spacing=10,
                controls=[
                    ft.Text(
                        "Ver todas",
                        size=Typography.SMALL,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREY_800,
                    ),
                    ft.Icon(
                        ft.Icons.CHEVRON_RIGHT,
                        size=19,
                        color=ft.Colors.GREY_700,
                    ),
                ],
            ),
        )

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=46,
                            height=46,
                            border_radius=Radius.LG,
                            bgcolor=ft.Colors.INDIGO_50,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ft.Icons.ASSIGNMENT_OUTLINED,
                                size=24,
                                color=ft.Colors.INDIGO_700,
                            ),
                        ),
                        ft.Column(
                            spacing=3,
                            controls=[
                                ft.Text(
                                    "Últimas solicitações",
                                    size=Typography.H3,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_900,
                                ),
                                ft.Text(
                                    (
                                        "As solicitações mais recentes "
                                        "cadastradas no sistema"
                                    ),
                                    size=Typography.SMALL,
                                    color=ft.Colors.GREY_600,
                                ),
                            ],
                        ),
                    ],
                ),
                botao_ver_todas,
            ],
        )

    def _criar_linhas(self) -> list[ft.DataRow]:
        """Cria as linhas da tabela."""

        linhas: list[ft.DataRow] = []

        for solicitacao in self.solicitacoes:
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Container(
                                width=125,
                                alignment=ft.Alignment.CENTER_LEFT,
                                content=ft.Container(
                                    padding=ft.Padding(
                                        left=10,
                                        top=5,
                                        right=10,
                                        bottom=5,
                                    ),
                                    border_radius=Radius.MD,
                                    bgcolor=ft.Colors.GREY_100,
                                    border=ft.Border.all(
                                        1,
                                        ft.Colors.GREY_200,
                                    ),
                                    content=ft.Text(
                                        str(
                                            solicitacao.get(
                                                "codigo",
                                                "",
                                            )
                                        ),
                                        size=Typography.SMALL,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_900,
                                    ),
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                width=300,
                                alignment=ft.Alignment.CENTER_LEFT,
                                content=ft.Text(
                                    str(
                                        solicitacao.get(
                                            "estabelecimento",
                                            "",
                                        )
                                    ),
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.GREY_900,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                width=165,
                                alignment=ft.Alignment.CENTER,
                                content=self._status_chip(
                                    str(
                                        solicitacao.get(
                                            "status",
                                            "",
                                        )
                                    )
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                width=75,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text(
                                    str(
                                        solicitacao.get(
                                            "quantidade_sacas",
                                            0,
                                        )
                                    ),
                                    color=ft.Colors.GREY_800,
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                width=90,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text(
                                    self._formatar_peso(
                                        solicitacao.get(
                                            "quantidade_kg",
                                            0,
                                        )
                                    ),
                                    color=ft.Colors.GREY_800,
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                width=205,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text(
                                    self._obter_data(solicitacao),
                                    color=ft.Colors.GREY_700,
                                    size=Typography.SMALL,
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                width=165,
                                alignment=ft.Alignment.CENTER,
                                content=self._criar_acoes(
                                    solicitacao
                                ),
                            )
                        ),
                    ],
                )
            )

        return linhas

    def _criar_tabela(
        self,
        linhas: list[ft.DataRow],
    ) -> ft.Control:
        """Cria a tabela com layout amplo e rolagem horizontal."""

        tabela = ft.DataTable(
            column_spacing=16,
            horizontal_margin=14,
            divider_thickness=0.7,
            heading_row_height=58,
            data_row_min_height=68,
            data_row_max_height=72,
            heading_row_color=ft.Colors.GREY_50,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_200,
            ),
            border_radius=Radius.LG,
            columns=[
                self._coluna("Número", 125),
                self._coluna("Estabelecimento", 300),
                self._coluna("Status", 165, centralizar=True),
                self._coluna("Sacas", 75, centralizar=True),
                self._coluna("Kg", 90, centralizar=True),
                self._coluna(
                    "Data da solicitação",
                    205,
                    centralizar=True,
                ),
                self._coluna("Ações", 165, centralizar=True),
            ],
            rows=linhas,
        )

        return ft.Container(
            width=float("inf"),
            border_radius=Radius.LG,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                controls=[tabela],
            ),
        )

    @staticmethod
    def _coluna(
        titulo: str,
        largura: int,
        centralizar: bool = False,
    ) -> ft.DataColumn:
        """Cria uma coluna com largura e alinhamento definidos."""

        return ft.DataColumn(
            ft.Container(
                width=largura,
                alignment=(
                    ft.Alignment.CENTER
                    if centralizar
                    else ft.Alignment.CENTER_LEFT
                ),
                content=ft.Text(
                    titulo,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_800,
                    size=Typography.SMALL,
                    text_align=(
                        ft.TextAlign.CENTER
                        if centralizar
                        else ft.TextAlign.LEFT
                    ),
                ),
            )
        )

    def _criar_acoes(
        self,
        solicitacao: dict,
    ) -> ft.Control:
        """Cria os botões de ação de uma solicitação."""

        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
            spacing=10,
            controls=[
                self._botao_acao(
                    icone=ft.Icons.VISIBILITY_OUTLINED,
                    cor=ft.Colors.BLUE_600,
                    cor_fundo=ft.Colors.BLUE_50,
                    tooltip="Visualizar",
                    on_click=self._adaptar_evento(
                        self.on_visualizar,
                        solicitacao,
                    ),
                ),
                self._botao_acao(
                    icone=ft.Icons.EDIT_OUTLINED,
                    cor=ft.Colors.GREEN_600,
                    cor_fundo=ft.Colors.GREEN_50,
                    tooltip="Editar",
                    on_click=self._adaptar_evento(
                        self.on_editar,
                        solicitacao,
                    ),
                ),
                self._botao_acao(
                    icone=ft.Icons.DELETE_OUTLINE,
                    cor=ft.Colors.RED_600,
                    cor_fundo=ft.Colors.RED_50,
                    tooltip="Excluir",
                    on_click=self._adaptar_evento(
                        self.on_excluir,
                        solicitacao,
                    ),
                ),
            ],
        )

    @staticmethod
    def _adaptar_evento(callback, solicitacao: dict):
        """Adapta um callback para receber a solicitação."""

        if callback is None:
            return None

        return lambda evento: callback(solicitacao)

    @staticmethod
    def _botao_acao(
        icone: str,
        cor: str,
        cor_fundo: str,
        tooltip: str,
        on_click=None,
    ) -> ft.Control:
        """Cria um botão compacto de ação."""

        return ft.Container(
            width=40,
            height=40,
            border_radius=Radius.MD,
            bgcolor=cor_fundo,
            border=ft.Border.all(
                1,
                ft.Colors.with_opacity(0.35, cor),
            ),
            alignment=ft.Alignment.CENTER,
            tooltip=tooltip,
            ink=True,
            on_click=on_click,
            content=ft.Icon(
                icone,
                size=19,
                color=cor,
            ),
        )

    def _criar_rodape(self) -> ft.Control:
        """Cria o rodapé com resumo e paginação visual."""

        quantidade = len(self.solicitacoes)

        if quantidade == 0:
            resumo = "Nenhum registro"
        elif quantidade == 1:
            resumo = "Exibindo 1 registro"
        else:
            resumo = f"Exibindo {quantidade} registros"

        paginacao = ft.Row(
            tight=True,
            spacing=10,
            controls=[
                self._botao_pagina(
                    ft.Icons.FIRST_PAGE,
                    ativo=False,
                ),
                self._botao_pagina(
                    ft.Icons.CHEVRON_LEFT,
                    ativo=False,
                ),
                ft.Container(
                    width=44,
                    height=42,
                    border_radius=Radius.MD,
                    bgcolor=ft.Colors.INDIGO_600,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "1",
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                self._botao_pagina(
                    ft.Icons.CHEVRON_RIGHT,
                    ativo=False,
                ),
                self._botao_pagina(
                    ft.Icons.LAST_PAGE,
                    ativo=False,
                ),
            ],
        )

        seletor_pagina = ft.Container(
            height=42,
            padding=ft.Padding(
                left=16,
                top=0,
                right=12,
                bottom=0,
            ),
            border_radius=Radius.MD,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            alignment=ft.Alignment.CENTER,
            content=ft.Row(
                tight=True,
                spacing=10,
                controls=[
                    ft.Text(
                        "10 por página",
                        size=Typography.SMALL,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Icon(
                        ft.Icons.KEYBOARD_ARROW_DOWN,
                        size=18,
                        color=ft.Colors.GREY_600,
                    ),
                ],
            ),
        )

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=260,
                    content=ft.Text(
                        resumo,
                        size=Typography.SMALL,
                        color=ft.Colors.GREY_600,
                    ),
                ),
                paginacao,
                ft.Container(
                    width=260,
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=seletor_pagina,
                ),
            ],
        )

    @staticmethod
    def _botao_pagina(
        icone: str,
        ativo: bool,
    ) -> ft.Control:
        """Cria um botão visual de paginação."""

        cor = (
            ft.Colors.INDIGO_600
            if ativo
            else ft.Colors.GREY_500
        )

        return ft.Container(
            width=44,
            height=42,
            border_radius=Radius.MD,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                icone,
                size=19,
                color=cor,
            ),
        )

    @staticmethod
    def _criar_estado_vazio() -> ft.Control:
        """Cria o estado exibido quando não há solicitações."""

        return ft.Container(
            height=190,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.SM,
                controls=[
                    ft.Container(
                        width=58,
                        height=58,
                        border_radius=29,
                        bgcolor=ft.Colors.GREY_100,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.INBOX_OUTLINED,
                            size=30,
                            color=ft.Colors.GREY_500,
                        ),
                    ),
                    ft.Text(
                        "Nenhuma solicitação cadastrada",
                        size=Typography.BODY,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Text(
                        (
                            "As solicitações mais recentes "
                            "aparecerão aqui."
                        ),
                        size=Typography.SMALL,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    @staticmethod
    def _status_chip(status: str) -> ft.Container:
        """Retorna um badge colorido para o status."""

        status_normalizado = status.upper().strip()

        configuracoes = {
            "PENDENTE": (
                ft.Colors.AMBER_100,
                ft.Colors.AMBER_900,
                ft.Icons.SCHEDULE,
            ),
            "AGENDADA": (
                ft.Colors.BLUE_100,
                ft.Colors.BLUE_900,
                ft.Icons.EVENT_AVAILABLE,
            ),
            "EM_COLETA": (
                ft.Colors.ORANGE_100,
                ft.Colors.ORANGE_900,
                ft.Icons.LOCAL_SHIPPING,
            ),
            "CONCLUIDA": (
                ft.Colors.GREEN_100,
                ft.Colors.GREEN_900,
                ft.Icons.CHECK_CIRCLE_OUTLINE,
            ),
            "CONCLUÍDA": (
                ft.Colors.GREEN_100,
                ft.Colors.GREEN_900,
                ft.Icons.CHECK_CIRCLE_OUTLINE,
            ),
        }

        cor_fundo, cor_texto, icone = configuracoes.get(
            status_normalizado,
            (
                ft.Colors.GREY_200,
                ft.Colors.GREY_800,
                ft.Icons.INFO_OUTLINE,
            ),
        )

        return ft.Container(
            padding=ft.Padding(
                left=12,
                top=6,
                right=12,
                bottom=6,
            ),
            bgcolor=cor_fundo,
            border_radius=Radius.LG,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                tight=True,
                spacing=6,
                controls=[
                    ft.Icon(
                        icone,
                        size=15,
                        color=cor_texto,
                    ),
                    ft.Text(
                        status_normalizado.replace("_", " "),
                        size=Typography.SMALL,
                        weight=ft.FontWeight.BOLD,
                        color=cor_texto,
                    ),
                ],
            ),
        )

    @staticmethod
    def _obter_data(solicitacao: dict) -> str:
        """Obtém uma data disponível na solicitação."""

        chaves = (
            "data_solicitacao",
            "data_criacao",
            "criado_em",
            "data",
        )

        for chave in chaves:
            valor = solicitacao.get(chave)

            if valor:
                return str(valor)

        return "—"

    @staticmethod
    def _formatar_peso(
        valor: int | float | None,
    ) -> str:
        """Formata o peso no padrão brasileiro."""

        try:
            numero = float(valor or 0)
        except (TypeError, ValueError):
            numero = 0

        return (
            f"{numero:,.1f}"
            .replace(",", "_")
            .replace(".", ",")
            .replace("_", ".")
        )