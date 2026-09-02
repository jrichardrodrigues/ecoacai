from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.dialogs import confirmar_exclusao
from components.layout.page_header import PageHeader
from components.buttons import PrimaryButton, SecondaryButton
from components.theme import Radius

from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from utils.messages import mostrar_erro, mostrar_sucesso


class SolicitacoesGestorView:
    """Fila de solicitações de coleta recebidas pelo Gestor."""

    def __init__(
        self,
        page: ft.Page,
        controller: SolicitacaoColetaController | None = None,
        on_ver_detalhes: Callable[[int, str], None] | None = None,
        on_abrir_lixeira: Callable[[], None] | None = None,
        status_inicial: str | None = None,
        data_agendada_inicial: str | None = None,
        data_solicitacao_inicial: str | None = None,
        titulo: str = "Solicitações",
        subtitulo: str = "Analise as solicitações de coleta recebidas dos Geradores.",
    ) -> None:
        self.page = page
        self.controller = (
                controller or SolicitacaoColetaController()
        )

        self.status_inicial = status_inicial
        self.data_agendada_inicial = data_agendada_inicial
        self.data_solicitacao_inicial = data_solicitacao_inicial

        self.titulo = titulo
        self.subtitulo = subtitulo

        # ==========================================================
        # FILTROS DE CONSULTA
        # ==========================================================

        self.campo_pesquisa = ft.TextField(
            label="Pesquisar",
            hint_text="Código ou solicitante",
            prefix_icon=ft.Icons.SEARCH,
            width=580,
            border_radius=Radius.INPUT,
        )

        self.filtro_status = ft.Dropdown(
            label="Status",
            width=190,
            value="TODOS",
            border_radius=Radius.INPUT,
            options=[
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                ),
                ft.DropdownOption(
                    key="EM_ANALISE",
                    text="Em análise",
                ),
                ft.DropdownOption(
                    key="AGENDADA",
                    text="Agendada",
                ),
                ft.DropdownOption(
                    key="EM_DESLOCAMENTO",
                    text="Em deslocamento",
                ),
                ft.DropdownOption(
                    key="EM_COLETA",
                    text="Em coleta",
                ),
                ft.DropdownOption(
                    key="CONCLUIDA",
                    text="Concluída",
                ),
                ft.DropdownOption(
                    key="CANCELADA",
                    text="Cancelada",
                ),
            ],
        )

        self.data_inicial_field = ft.TextField(
            label="Data inicial",
            hint_text="dd/mm/aaaa",
            width=150,
            read_only=True,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            border_radius=Radius.INPUT,
            on_click=self._abrir_data_inicial,
            always_call_on_tap=True,
        )

        self.data_final_field = ft.TextField(
            label="Data final",
            hint_text="dd/mm/aaaa",
            width=150,
            read_only=True,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            border_radius=Radius.INPUT,
            on_click=self._abrir_data_final,
            always_call_on_tap=True,
        )
        self.lista = ft.Column(
            spacing=12,
        )

        self.total = ft.Text(
            "0 solicitações",
            size=14,
            color=ft.Colors.BLUE_GREY_700,
        )

        self.on_ver_detalhes = on_ver_detalhes

        self.on_abrir_lixeira = on_abrir_lixeira

        self._carregar()

    def _abrir_data_inicial(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        picker = ft.DatePicker(
            help_text="Selecione a data inicial",
            cancel_text="Cancelar",
            confirm_text="Selecionar",
            entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY,
            on_change=self._ao_selecionar_data_inicial,
        )

        self.page.show_dialog(picker)

    def _abrir_data_final(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        picker = ft.DatePicker(
            help_text="Selecione a data final",
            cancel_text="Cancelar",
            confirm_text="Selecionar",
            entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY,
            on_change=self._ao_selecionar_data_final,
        )

        self.page.show_dialog(picker)

    def _ao_selecionar_data_inicial(
            self,
            event: ft.Event[ft.DatePicker],
    ) -> None:
        data = event.control.value

        if data is None:
            return

        self.data_inicial_field.value = data.strftime(
            "%d/%m/%Y"
        )

        self.page.update()

    def _ao_selecionar_data_final(
            self,
            event: ft.Event[ft.DatePicker],
    ) -> None:
        data = event.control.value

        if data is None:
            return

        self.data_final_field.value = data.strftime(
            "%d/%m/%Y"
        )

        self.page.update()

    # ==========================================================
    # FORMATAÇÃO
    # ==========================================================

    @staticmethod
    def _formatar_status(
        status: str,
    ) -> str:
        return (
            str(status or "")
            .replace("_", " ")
            .title()
        )

    @staticmethod
    def _criar_status_chip(
            status: str,
    ) -> ft.Container:
        """Cria o chip visual correspondente ao status da solicitação."""

        status_normalizado = str(
            status or ""
        ).strip().upper()

        estilos = {
            "SOLICITADA": (
                ft.Colors.AMBER_100,
                ft.Colors.AMBER_900,
            ),
            "EM_ANALISE": (
                ft.Colors.ORANGE_100,
                ft.Colors.ORANGE_900,
            ),
            "AGENDADA": (
                ft.Colors.BLUE_100,
                ft.Colors.BLUE_900,
            ),
            "EM_COLETA": (
                ft.Colors.ORANGE_100,
                ft.Colors.ORANGE_900,
            ),
            "CONCLUIDA": (
                ft.Colors.GREEN_100,
                ft.Colors.GREEN_900,
            ),
            "CANCELADA": (
                ft.Colors.GREY_200,
                ft.Colors.GREY_800,
            ),
        }

        cor_fundo, cor_texto = estilos.get(
            status_normalizado,
            (
                ft.Colors.BLUE_GREY_100,
                ft.Colors.BLUE_GREY_800,
            ),
        )

        return ft.Container(
            content=ft.Text(
                SolicitacoesGestorView._formatar_status(
                    status_normalizado
                ),
                size=13,
                weight=ft.FontWeight.BOLD,
                color=cor_texto,
            ),
            bgcolor=cor_fundo,
            padding=ft.Padding.symmetric(
                horizontal=12,
                vertical=5,
            ),
            border_radius=16,
        )

    @staticmethod
    def _formatar_residuo(
        tipo: str,
    ) -> str:
        tipos = {
            "CAROCO_ACAI": "Caroço de Açaí",
        }

        return tipos.get(
            tipo,
            tipo or "-",
        )

    @staticmethod
    def _formatar_quantidade(
            dados: dict,
    ) -> str:
        forma_acondicionamento = str(
            dados.get("forma_acondicionamento") or ""
        ).strip().upper()

        quantidade = int(
            dados.get("quantidade_prevista")
            or dados.get("quantidade_sacas_prevista")
            or 0
        )

        if forma_acondicionamento == "BAG":
            unidade_texto = (
                "Bag"
                if quantidade == 1
                else "Bags"
            )

            return (
                f"{quantidade} "
                f"{unidade_texto} (1 m³)"
            )

        if forma_acondicionamento == "SACA":
            unidade_texto = (
                "Saca"
                if quantidade == 1
                else "Sacas"
            )

            return (
                f"{quantidade} "
                f"{unidade_texto} (50 kg)"
            )

        return f"{quantidade} unidade(s)"

    @staticmethod
    def _converter_data_filtro(
            valor: str | None,
    ) -> str | None:
        if not valor:
            return None

        valor = valor.strip()

        if not valor:
            return None

        try:
            dia, mes, ano = valor.split("/")
            return f"{ano}-{mes}-{dia}"
        except ValueError:
            raise ValueError(
                "Informe a data no formato dd/mm/aaaa."
            )

    def _ao_pesquisar(
            self,
            _e: ft.Event[ft.Control] | None = None,
    ) -> None:
        try:
            data_inicial = self._converter_data_filtro(
                self.data_inicial_field.value
            )

            data_final = self._converter_data_filtro(
                self.data_final_field.value
            )

            if (
                    data_inicial
                    and data_final
                    and data_inicial > data_final
            ):
                raise ValueError(
                    "A data inicial não pode ser maior que a data final."
                )

            pesquisa = str(
                self.campo_pesquisa.value or ""
            ).strip()

            status = str(
                self.filtro_status.value or "TODOS"
            ).strip()

            if status == "TODOS":
                status = None

            self._carregar(
                pesquisa=pesquisa or None,
                status=status,
                data_inicial=data_inicial,
                data_final=data_final,
            )

            self.page.update()

        except ValueError as erro:
            mostrar_erro(
                self.page,
                str(erro),
            )

    def _limpar_filtros(
            self,
            _e: ft.Event[ft.Control] | None = None,
    ) -> None:
        self.campo_pesquisa.value = ""
        self.filtro_status.value = "TODOS"
        self.data_inicial_field.value = ""
        self.data_final_field.value = ""

        self._carregar()

        self.page.update()

    # ==========================================================
    # DADOS
    # ==========================================================

    def _carregar(
            self,
            *,
            pesquisa: str | None = None,
            status: str | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> None:
        solicitacoes = self.controller.listar_operacional(
            pesquisa=pesquisa,
            status=status,
            data_agendada=self.data_agendada_inicial,
            data_inicial=data_inicial,
            data_final=data_final,
        )

        self.lista.controls.clear()

        for dados in solicitacoes:
            self.lista.controls.append(
                self._criar_card(dados)
            )

        total = len(solicitacoes)

        self.total.value = (
            f"{total} "
            f"{'solicitação' if total == 1 else 'solicitações'}"
        )

        if not solicitacoes:
            self.lista.controls.append(
                self._estado_vazio()
            )

    # ==========================================================
    # CARDS
    # ==========================================================

    def _criar_card(
        self,
        dados: dict,
    ) -> ft.Control:

        solicitacao_id = int(
            dados.get("id") or 0
        )

        codigo = (
            dados.get("codigo")
            or f"COL-{solicitacao_id:06d}"
        )

        solicitante = (
            dados.get("solicitante")
            or "Solicitante não identificado"
        )

        status = str(
            dados.get("status") or ""
        ).upper()

        botoes: list[ft.Control] = []

        if status == "SOLICITADA":
            botoes.append(
                ft.FilledButton(
                    content="Analisar",
                    icon=ft.Icons.RATE_REVIEW_OUTLINED,
                    on_click=lambda _e, sid=solicitacao_id: (
                        self._analisar(sid)
                    ),
                )
            )

            botoes.append(
                ft.TextButton(
                    content="Excluir",
                    icon=ft.Icons.DELETE_OUTLINE,
                    style=ft.ButtonStyle(
                        color=ft.Colors.RED_700,
                    ),
                    on_click=lambda _e, sid=solicitacao_id: (
                        self._excluir(sid)
                    ),
                )
            )

        if self.on_ver_detalhes is not None:
            botoes.append(
                ft.TextButton(
                    content="Ver detalhes",
                    icon=ft.Icons.VISIBILITY_OUTLINED,
                    on_click=lambda _e, sid=solicitacao_id, nome=solicitante: (
                        self.on_ver_detalhes(
                            sid,
                            nome,
                        )
                    ),
                )
            )

        return ft.Card(
            content=ft.Container(
                padding=ft.Padding.symmetric(
                    horizontal=16,
                    vertical=10,
                ),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    codigo,
                                    size=17,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(
                                    expand=True,
                                ),
                                self._criar_status_chip(
                                    status
                                ),
                            ],
                        ),

                        ft.Divider(
                            height=8,
                        ),

                        ft.Text(
                            f"Solicitante: {solicitante}"
                        ),

                        ft.Text(
                            "Tipo de resíduo: "
                            + self._formatar_residuo(
                                dados.get("tipo_residuo")
                            )
                        ),

                        ft.Text(
                            "Quantidade prevista: "
                            + self._formatar_quantidade(dados)
                        ),

                        ft.Text(
                            "Peso estimado: "
                            + self._formatar_peso_estimado(dados)
                        ),

                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Solicitada em: "
                                    f"{dados.get('data_solicitacao') or '-'}"
                                ),
                                ft.Container(
                                    expand=True,
                                ),
                                *botoes,
                            ],
                            vertical_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                        ),
                    ],
                    spacing=5,
                ),
            ),
        )

    def _excluir(
            self,
            solicitacao_id: int,
    ) -> None:
        """Solicita confirmação e exclui logicamente a solicitação."""

        def confirmar() -> None:
            sucesso, mensagem = self.controller.excluir(
                solicitacao_id
            )

            if sucesso:
                mostrar_sucesso(
                    self.page,
                    mensagem,
                )
                self._carregar()
            else:
                mostrar_erro(
                    self.page,
                    mensagem,
                )

        confirmar_exclusao(
            page=self.page,
            mensagem=(
                "Deseja realmente excluir esta solicitação?"
            ),
            on_confirm=confirmar,
        )

    @staticmethod
    def _formatar_peso_estimado(
            dados: dict,
    ) -> str:
        peso = float(
            dados.get("peso_estimado_kg") or 0
        )

        if peso <= 0:
            return "Não informado"

        if peso.is_integer():
            return f"{int(peso):,}".replace(",", ".") + " kg"

        return (
                f"{peso:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " kg"
        )

    # ==========================================================
    # AÇÕES
    # ==========================================================

    def _analisar(
        self,
        solicitacao_id: int,
    ) -> None:
        sucesso, mensagem, _solicitacao = (
            self.controller.analisar(
                solicitacao_id
            )
        )

        if not sucesso:
            mostrar_erro(
                self.page,
                mensagem,
            )
            return

        mostrar_sucesso(
            self.page,
            mensagem,
        )

        self._carregar()
        self.page.update()

    # ==========================================================
    # ESTADO VAZIO
    # ==========================================================

    @staticmethod
    def _estado_vazio() -> ft.Control:
        return ft.Container(
            padding=40,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.INBOX_OUTLINED,
                        size=56,
                        color=ft.Colors.BLUE_GREY_400,
                    ),
                    ft.Text(
                        "Nenhuma solicitação nesta data.",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Não há solicitações cadastradas hoje.",
                        color=ft.Colors.BLUE_GREY_700,
                    ),
                ],
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=10,
            ),
        )

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def build(self) -> ft.Control:

        cabecalho = PageHeader(
            title=self.titulo,
            subtitle=self.subtitulo,
        )

        botao_lixeira = ft.OutlinedButton(
            content=ft.Text("Lixeira"),
            icon=ft.Icons.DELETE_OUTLINE,
            on_click=(
                lambda _e: self.on_abrir_lixeira()
                if self.on_abrir_lixeira is not None
                else None
            ),
            height=48,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.RED_700,
                    ft.ControlState.DISABLED: ft.Colors.GREY_500,
                },
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(
                        width=1,
                        color=ft.Colors.RED_700,
                    ),
                    ft.ControlState.DISABLED: ft.BorderSide(
                        width=1,
                        color=ft.Colors.GREY_300,
                    ),
                },
                padding=ft.Padding(
                    left=16,
                    top=10,
                    right=16,
                    bottom=10,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=Radius.MD,
                ),
            ),
        )

        botao_pesquisar = PrimaryButton(
            label="Pesquisar",
            icon=ft.Icons.SEARCH,
            on_click=self._ao_pesquisar,
        )

        botao_limpar = SecondaryButton(
            label="Limpar",
            icon=ft.Icons.CLEAR,
            on_click=self._limpar_filtros,
        )

        barra_botoes = ft.Row(
            controls=[
                botao_pesquisar,
                botao_limpar,
                botao_lixeira,
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        barra_filtros = ft.Row(
            controls=[
                self.campo_pesquisa,
                self.filtro_status,
                self.data_inicial_field,
                self.data_final_field,
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        barra_acoes = ft.Row(
            controls=[
                self.total,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        area_lista = ft.Container(
            content=self.lista,
            expand=True,
        )

        return ft.Column(
            controls=[
                cabecalho,

                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                barra_botoes,
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),

                        barra_filtros,
                    ],
                    spacing=8,
                ),

                barra_acoes,

                area_lista,
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )