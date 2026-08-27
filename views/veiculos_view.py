from __future__ import annotations

import math
from collections.abc import Callable

import flet as ft

from components.chips import StatusChip
from components.layout import PageHeader
from components.dialogs import ConfirmDialog
from components.buttons import PrimaryButton, SecondaryButton

from controllers.veiculo_controller import VeiculoController
from models import Veiculo
from views.veiculo_form_view import VeiculoFormView


class VeiculosView:
    """Tela de listagem e gerenciamento de veículos."""

    ITENS_POR_PAGINA = 10

    def __init__(
        self,
        page: ft.Page,
        controller: VeiculoController | None = None,
        ao_voltar: Callable[[], None] | None = None,
    ) -> None:
        self.page = page
        self.controller = controller or VeiculoController()
        self.ao_voltar = ao_voltar

        self.pagina_atual = 1
        self.total_paginas = 1
        self.veiculos: list[Veiculo] = []

        self.pesquisa_field = ft.TextField(
            label="Pesquisar veículo",
            hint_text="Placa, marca, modelo ou tipo",
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self._ao_pesquisar,
            expand=True,
        )

        self.filtro_dropdown = ft.Dropdown(
            label="Situação",
            value="ATIVOS",
            width=190,
            options=[
                ft.DropdownOption(
                    key="ATIVOS",
                    text="Somente ativos",
                ),
                ft.DropdownOption(
                    key="INATIVOS",
                    text="Somente inativos",
                ),
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                ),
            ],
            on_select=self._ao_alterar_filtro,
        )

        self.novo_button = PrimaryButton(
            label="Novo Veículo",
            icon=ft.Icons.ADD,
            on_click=self._abrir_cadastro,
        )

        self.botao_pesquisar = PrimaryButton(
            label="Pesquisar",
            icon=ft.Icons.SEARCH,
            on_click=self._ao_pesquisar,
        )

        self.botao_limpar = SecondaryButton(
            label="Limpar",
            icon=ft.Icons.CLEAR,
            on_click=self._limpar_pesquisa,
        )

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(
                    label=ft.Text(
                        "Placa",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Veículo",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Ano",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Tipo",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Capacidade",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Status",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Situação",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Ações",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
            ],
            rows=[],
            column_spacing=24,
            horizontal_lines=ft.BorderSide(
                width=1,
                color=ft.Colors.OUTLINE_VARIANT,
            ),
        )

        self.tabela_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=self.tabela,
                        width=1300,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            border=ft.Border.all(
                width=1,
                color=ft.Colors.OUTLINE_VARIANT,
            ),
            border_radius=8,
            padding=8,
        )

        self.estado_vazio = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.LOCAL_SHIPPING_OUTLINED,
                        size=64,
                        color=ft.Colors.OUTLINE,
                    ),
                    ft.Text(
                        "Nenhum veículo encontrado.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        "Cadastre um veículo ou altere os filtros da pesquisa.",
                        color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            alignment=ft.Alignment.CENTER,
            padding=40,
            visible=False,
        )

        self.anterior_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            tooltip="Página anterior",
            on_click=self._pagina_anterior,
        )

        self.proxima_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            tooltip="Próxima página",
            on_click=self._proxima_pagina,
        )

        self.paginacao_text = ft.Text(
            "Página 1 de 1",
            weight=ft.FontWeight.W_500,
        )

        self.quantidade_text = ft.Text(
            "0 veículo(s)",
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        self.container = ft.Container(
            expand=True,
            padding=24,
            content=ft.Column(
                controls=[
                    self._construir_cabecalho(),
                    ft.Divider(),
                    self._construir_filtros(),
                    self.quantidade_text,
                    self.tabela_container,
                    self.estado_vazio,
                    self._construir_paginacao(),
                ],
                spacing=18,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self._carregar_veiculos()

    # ==========================================================
    # CONSTRUÇÃO
    # ==========================================================

    def build(self) -> ft.Control:
        return self.container

    def _construir_cabecalho(self) -> ft.Control:
        return ft.Row(
            controls=[
                ft.Container(
                    content=PageHeader(
                        title="Veículos",
                        subtitle="Cadastro e gerenciamento da frota.",
                        show_divider=False,
                    ),
                    expand=True,
                ),
                self.novo_button,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _construir_filtros(self) -> ft.Control:
        return ft.Row(
            controls=[
                self.pesquisa_field,
                self.filtro_dropdown,
                self.botao_pesquisar,
                self.botao_limpar,
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _construir_paginacao(self) -> ft.Control:
        return ft.Row(
            controls=[
                self.anterior_button,
                self.paginacao_text,
                self.proxima_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ==========================================================
    # CARREGAMENTO
    # ==========================================================

    def _carregar_veiculos(self) -> None:
        try:
            pesquisa = str(
                self.pesquisa_field.value or ""
            ).strip()

            somente_ativos = self._obter_filtro_ativos()

            todos_veiculos = self.controller.listar(
                pesquisa=pesquisa,
                somente_ativos=somente_ativos,
                limite=None,
                pagina=None,
            )

            todos_veiculos = list(
                todos_veiculos or []
            )

            # Garante o filtro mesmo que o repository não trate
            # explicitamente somente_ativos=False.
            if somente_ativos is True:
                todos_veiculos = [
                    veiculo
                    for veiculo in todos_veiculos
                    if veiculo.ativo
                ]

            elif somente_ativos is False:
                todos_veiculos = [
                    veiculo
                    for veiculo in todos_veiculos
                    if not veiculo.ativo
                ]

            total_registros = len(todos_veiculos)

            self.total_paginas = max(
                1,
                math.ceil(
                    total_registros
                    / self.ITENS_POR_PAGINA
                ),
            )

            if self.pagina_atual > self.total_paginas:
                self.pagina_atual = self.total_paginas

            inicio = (
                self.pagina_atual - 1
            ) * self.ITENS_POR_PAGINA

            fim = inicio + self.ITENS_POR_PAGINA

            self.veiculos = todos_veiculos[
                inicio:fim
            ]

            self._preencher_tabela()
            self._atualizar_paginacao(
                total_registros
            )

        except Exception as erro:
            self.veiculos = []
            self.tabela.rows = []
            self.tabela_container.visible = False
            self.estado_vazio.visible = True

            self._mostrar_mensagem(
                f"Não foi possível carregar os veículos: {erro}",
                erro=True,
            )

            self._atualizar_pagina()

    def _preencher_tabela(self) -> None:
        linhas: list[ft.DataRow] = []

        for veiculo in self.veiculos:
            linhas.append(
                self._criar_linha(
                    veiculo
                )
            )

        self.tabela.rows = linhas

        possui_registros = bool(
            self.veiculos
        )

        self.tabela_container.visible = (
            possui_registros
        )

        self.estado_vazio.visible = (
            not possui_registros
        )

        self._atualizar_pagina()

    def _criar_linha(
        self,
        veiculo: Veiculo,
    ) -> ft.DataRow:
        return ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(
                        veiculo.placa or "-",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    )
                ),
                ft.DataCell(
                    ft.Column(
                        controls=[
                            ft.Text(
                                self._descricao_veiculo(
                                    veiculo
                                ),
                                size=16,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                veiculo.marca or "",
                                size=14,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                        spacing=1,
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        str(veiculo.ano)
                        if veiculo.ano is not None
                        else "-",
                        size=16,
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        veiculo.tipo or "-",
                        size=16,
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        self._formatar_capacidade(
                            veiculo.capacidade
                        ),
                        size=16,
                    )
                ),
                ft.DataCell(
                    self._criar_status(
                        veiculo.status
                    )
                ),
                ft.DataCell(
                    self._criar_situacao(
                        veiculo.ativo
                    )
                ),
                ft.DataCell(
                    self._criar_acoes(
                        veiculo
                    )
                ),
            ],
        )

    # ==========================================================
    # COMPONENTES DA TABELA
    # ==========================================================

    def _criar_status(
            self,
            status: str,
    ) -> ft.Control:
        return StatusChip(
            texto=status or "DISPONIVEL",
            contexto="veiculo",
        )

    def _criar_situacao(
            self,
            ativo: bool,
    ) -> ft.Control:
        return StatusChip(
            texto="ATIVO" if ativo else "INATIVO",
            contexto="situacao",
        )

    def _criar_acoes(
        self,
        veiculo: Veiculo,
    ) -> ft.Control:
        editar_button = ft.IconButton(
            icon=ft.Icons.EDIT_OUTLINED,
            tooltip="Editar veículo",
            disabled=not veiculo.ativo,
            on_click=lambda event, item=veiculo: (
                self._abrir_edicao(item)
            ),
        )

        if veiculo.ativo:
            situacao_button = ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.CLICK,
                on_tap=lambda e, item=veiculo: (
                    self._confirmar_desativacao(item)
                ),
                content=ft.Container(
                    content=ft.Image(
                        src="icons/veiculo_desativar.png",
                        width=55,
                        height=55,
                    ),
                    tooltip="Desativar veículo",
                    padding=4,
                ),
            )
        else:
            situacao_button = ft.IconButton(
                icon=ft.Icons.RESTORE,
                tooltip="Reativar veículo",
                on_click=lambda event, item=veiculo: (
                    self._confirmar_reativacao(item)
                ),
            )

        return ft.Row(
            controls=[
                editar_button,
                situacao_button,
            ],
            spacing=0,
        )

    # ==========================================================
    # PESQUISA E FILTROS
    # ==========================================================

    def _ao_pesquisar(
        self,
        event: ft.Event[ft.TextField] | None = None,
    ) -> None:
        self.pagina_atual = 1
        self._carregar_veiculos()

    def _limpar_pesquisa(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        self.pesquisa_field.value = ""
        self.filtro_dropdown.value = "ATIVOS"
        self.pagina_atual = 1

        self._carregar_veiculos()

    def _ao_alterar_filtro(
        self,
        event: ft.Event[ft.Dropdown] | None = None,
    ) -> None:
        self.pagina_atual = 1
        self._carregar_veiculos()

    def _obter_filtro_ativos(
        self,
    ) -> bool | None:
        filtro = str(
            self.filtro_dropdown.value or "ATIVOS"
        ).upper()

        if filtro == "ATIVOS":
            return True

        if filtro == "INATIVOS":
            return False

        return None

    def _atualizar_lista(
        self,
        event: ft.Event[ft.Control] | None = None,
    ) -> None:
        self._carregar_veiculos()

    # ==========================================================
    # PAGINAÇÃO
    # ==========================================================

    def _pagina_anterior(
        self,
        event: ft.Event[ft.Control] | None = None,
    ) -> None:
        if self.pagina_atual <= 1:
            return

        self.pagina_atual -= 1
        self._carregar_veiculos()

    def _proxima_pagina(
        self,
        event: ft.Event[ft.Control] | None = None,
    ) -> None:
        if self.pagina_atual >= self.total_paginas:
            return

        self.pagina_atual += 1
        self._carregar_veiculos()

    def _atualizar_paginacao(
        self,
        total_registros: int,
    ) -> None:
        self.paginacao_text.value = (
            f"Página {self.pagina_atual} "
            f"de {self.total_paginas}"
        )

        self.quantidade_text.value = (
            f"{total_registros} veículo(s) encontrado(s)"
        )

        self.anterior_button.disabled = (
            self.pagina_atual <= 1
        )

        self.proxima_button.disabled = (
            self.pagina_atual
            >= self.total_paginas
        )

        self._atualizar_pagina()

    # ==========================================================
    # CADASTRO E EDIÇÃO
    # ==========================================================

    def _abrir_cadastro(
        self,
        event: ft.Event[ft.Control] | None = None,
    ) -> None:
        formulario = VeiculoFormView(
            page=self.page,
            controller=self.controller,
            ao_salvar=self._ao_salvar_formulario,
            ao_cancelar=self._fechar_formulario,
        )

        self._mostrar_formulario(
            formulario
        )

    def _abrir_edicao(
        self,
        veiculo: Veiculo,
    ) -> None:
        formulario = VeiculoFormView(
            page=self.page,
            veiculo=veiculo,
            controller=self.controller,
            ao_salvar=self._ao_salvar_formulario,
            ao_cancelar=self._fechar_formulario,
        )

        self._mostrar_formulario(
            formulario
        )

    def _mostrar_formulario(
        self,
        formulario: VeiculoFormView,
    ) -> None:
        self.container.content = (
            formulario.build()
        )

        self._atualizar_pagina()

    def _ao_salvar_formulario(
        self,
        veiculo: Veiculo,
    ) -> None:
        self._fechar_formulario()
        self._carregar_veiculos()

    def _fechar_formulario(
        self,
    ) -> None:
        self.container.content = ft.Column(
            controls=[
                self._construir_cabecalho(),
                ft.Divider(),
                self._construir_filtros(),
                self.quantidade_text,
                self.tabela_container,
                self.estado_vazio,
                self._construir_paginacao(),
            ],
            spacing=18,
            scroll=ft.ScrollMode.AUTO,
        )

        self._carregar_veiculos()

    # ==========================================================
    # DESATIVAÇÃO E REATIVAÇÃO
    # ==========================================================

    def _confirmar_desativacao(
            self,
            veiculo: Veiculo,
    ) -> None:
        ConfirmDialog(
            page=self.page,
            titulo="Desativar veículo",
            mensagem=(
                f"Deseja realmente desativar o veículo "
                f"{veiculo.placa}?"
            ),
            texto_confirmar="Desativar",
            cor_confirmar=ft.Colors.RED_700,
            on_confirm=lambda: self._desativar(veiculo),
        ).abrir()

    def _desativar(
            self,
            veiculo: Veiculo,
    ) -> None:
        try:
            if veiculo.id is None:
                raise ValueError(
                    "Veículo sem identificador."
                )

            sucesso = self.controller.desativar(
                veiculo.id
            )

            if not sucesso:
                raise ValueError(
                    "O veículo não foi desativado."
                )

            self._mostrar_mensagem(
                "Veículo desativado com sucesso."
            )

            self._carregar_veiculos()

        except Exception as erro:
            self._mostrar_mensagem(
                str(erro),
                erro=True,
            )

    def _confirmar_reativacao(
            self,
            veiculo: Veiculo,
    ) -> None:
        ConfirmDialog(
            page=self.page,
            titulo="Reativar veículo",
            mensagem=(
                f"Deseja realmente reativar o veículo "
                f"{veiculo.placa}?"
            ),
            texto_confirmar="Reativar",
            cor_confirmar=ft.Colors.GREEN_700,
            on_confirm=lambda: self._reativar(veiculo),
        ).abrir()

    def _reativar(
    self,
    veiculo: Veiculo,
) -> None:
        try:
            if veiculo.id is None:
                raise ValueError(
                    "Veículo sem identificador."
                )

            sucesso = self.controller.reativar(
                veiculo.id
            )

            if not sucesso:
                raise ValueError(
                    "O veículo não foi reativado."
                )
            self._mostrar_mensagem(
                "Veículo reativado com sucesso."
            )

            self._carregar_veiculos()

        except Exception as erro:
            self._mostrar_mensagem(
                str(erro),
                erro=True,
            )

    # ==========================================================
    # NAVEGAÇÃO
    # ==========================================================

    def _voltar(
        self,
        event: ft.Event[ft.Control] | None = None,
    ) -> None:
        if self.ao_voltar is not None:
            self.ao_voltar()

    # ==========================================================
    # UTILITÁRIOS
    # ==========================================================

    @staticmethod
    def _descricao_veiculo(
        veiculo: Veiculo,
    ) -> str:
        descricao = " ".join(
            parte
            for parte in [
                str(veiculo.marca or "").strip(),
                str(veiculo.modelo or "").strip(),
            ]
            if parte
        )

        return descricao or "-"

    @staticmethod
    def _formatar_capacidade(
            capacidade: float | None,
    ) -> str:
        if capacidade is None:
            return "-"

        valor = float(
            capacidade
        )

        if valor.is_integer():
            texto = f"{int(valor):,}".replace(
                ",",
                ".",
            )
        else:
            texto = (
                f"{valor:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        return f"{texto} t"

    def _mostrar_mensagem(
        self,
        mensagem: str,
        erro: bool = False,
    ) -> None:
        snackbar = ft.SnackBar(
            content=ft.Text(
                mensagem
            ),
            bgcolor=(
                ft.Colors.ERROR_CONTAINER
                if erro
                else ft.Colors.PRIMARY_CONTAINER
            ),
        )

        self.page.show_dialog(
            snackbar
        )

    def _atualizar_pagina(self) -> None:
        try:
            self.page.update()
        except RuntimeError:
            # O controle pode ainda não estar anexado à página.
            pass