from collections.abc import Callable

import flet as ft

from components.buttons import (
    PrimaryButton,
    SecondaryButton,
)
from components.responsive import (
    ResponsiveFilterBar,
    ResponsiveHeader,
)
from components.theme import (
    Colors,
    Radius,
    Spacing,
)
from controllers import MotoristaController
from models import Motorista
from utils.messages import (
    mostrar_erro,
    mostrar_sucesso,
)
from components.dialogs import ConfirmDialog


class MotoristasView:
    """Tela de consulta e gerenciamento de motoristas."""

    ITENS_POR_PAGINA = 10

    def __init__(
        self,
        page: ft.Page,
        on_novo: Callable[[], None],
        on_editar: Callable[[Motorista], None],
    ) -> None:
        self.page = page
        self.controller = MotoristaController()

        self.on_novo = on_novo
        self.on_editar = on_editar

        self.motoristas: list[Motorista] = []

        self.pagina_atual = 1
        self.total_registros = 0

        # ======================================================
        # PESQUISA
        # ======================================================

        self.campo_pesquisa = ft.TextField(
            label="Pesquisar",
            hint_text=(
                "Pesquise por nome, telefone ou CNH"
            ),
            prefix_icon=ft.Icons.SEARCH,
            border_radius=Radius.INPUT,
            expand=True,
            on_submit=self.pesquisar,
        )

        self.botao_pesquisar = PrimaryButton(
            label="Pesquisar",
            icon=ft.Icons.SEARCH,
            on_click=self.pesquisar,
        )

        self.botao_limpar_pesquisa = SecondaryButton(
            label="Limpar",
            icon=ft.Icons.CLEAR,
            on_click=self.limpar_pesquisa,
        )

        self.botao_novo_motorista = PrimaryButton(
            label="Novo Motorista",
            icon=ft.Icons.ADD,
            on_click=self.abrir_novo_motorista,
        )

        # ======================================================
        # FILTRO DE SITUAÇÃO
        # ======================================================

        self.filtro_situacao = ft.Dropdown(
            label="Situação",
            value="ATIVOS",
            width=180,
            border_radius=Radius.INPUT,
            options=[
                ft.dropdown.Option(
                    key="ATIVOS",
                    text="Ativos",
                ),
                ft.dropdown.Option(
                    key="INATIVOS",
                    text="Inativos",
                ),
                ft.dropdown.Option(
                    key="TODOS",
                    text="Todos",
                ),
            ],
            on_select=self.alterar_filtro_situacao,
        )

        # ======================================================
        # TABELA
        # ======================================================

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(
                    label=ft.Text(
                        "Nome",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Telefone",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "CNH",
                        size=17,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.DataColumn(
                    label=ft.Text(
                        "Categoria",
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
            column_spacing=Spacing.MD,
            horizontal_margin=Spacing.MD,
            heading_row_height=52,
            data_row_min_height=52,
            data_row_max_height=64,
        )

        self.container_tabela = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=self.tabela,
                        width=1300,
                    ),
                ],
                scroll=ft.ScrollMode.ALWAYS,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            border=ft.Border.all(
                width=1,
                color=Colors.BORDER,
            ),
            border_radius=Radius.CARD,
            padding=Spacing.XS,
            expand=True,
        )

        # ======================================================
        # CARREGAMENTO E ESTADO VAZIO
        # ======================================================

        self.indicador_carregamento = ft.ProgressRing(
            visible=False,
        )

        self.mensagem_lista = ft.Text(
            value="Nenhum motorista encontrado.",
            visible=False,
        )

        self.estado_lista = ft.Container(
            visible=False,
            content=ft.Column(
                controls=[
                    self.indicador_carregamento,
                    self.mensagem_lista,
                ],
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=Spacing.SM,
            ),
            alignment=ft.Alignment.CENTER,
            padding=Spacing.LG,
        )

        # ======================================================
        # PAGINAÇÃO
        # ======================================================

        self.texto_paginacao = ft.Text(
            value="Página 1 de 1",
        )

        self.botao_anterior = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            tooltip="Página anterior",
            disabled=True,
            on_click=self.pagina_anterior,
        )

        self.botao_proxima = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            tooltip="Próxima página",
            disabled=True,
            on_click=self.proxima_pagina,
        )

        self.paginacao = ft.Row(
            controls=[
                self.botao_anterior,
                self.texto_paginacao,
                self.botao_proxima,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
        )

        # ======================================================
        # CONTEÚDO PRINCIPAL
        # ======================================================

        self.container = ft.Container(
            expand=True,
            padding=24,
            content=ft.Column(
                controls=[],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self.exibir_listagem()
        self.carregar_motoristas()

    # ==========================================================
    # CONSTRUÇÃO DA INTERFACE
    # ==========================================================

    def exibir_listagem(self) -> None:
        """Configura os controles da tela de listagem."""

        self.container.content.controls = [
            ResponsiveHeader(
                title="Motoristas",
                subtitle=(
                    "Cadastre, consulte e gerencie "
                    "os motoristas da operação."
                ),
                action_label="Novo Motorista",
                action_icon=ft.Icons.ADD,
                on_action=self.abrir_novo_motorista,
            ),
            ResponsiveFilterBar(
                controls=[
                    self.campo_pesquisa,
                    self.filtro_situacao,
                    self.botao_pesquisar,
                    self.botao_limpar_pesquisa,
                ],
            ),
            self.estado_lista,
            self.container_tabela,
            self.paginacao,
        ]

    def construir(self) -> ft.Control:
        """Constrói a tela principal de motoristas."""

        return self.container

    # ==========================================================
    # NAVEGAÇÃO
    # ==========================================================

    def abrir_novo_motorista(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Solicita a abertura do formulário de cadastro."""

        self.on_novo()

    def abrir_edicao(
        self,
        motorista: Motorista,
    ) -> None:
        """Solicita a abertura do formulário de edição."""

        self.on_editar(
            motorista,
        )

    # ==========================================================
    # FILTROS
    # ==========================================================

    def obter_filtro_ativos(
        self,
    ) -> bool | None:
        """
        Converte o filtro visual para o valor do controller.

        Retorna:
        - True para ativos;
        - False para inativos;
        - None para todos.
        """

        filtro = self.filtro_situacao.value

        if filtro == "ATIVOS":
            return True

        if filtro == "INATIVOS":
            return False

        return None

    def pesquisar(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Executa uma pesquisa."""

        self.pagina_atual = 1
        self.carregar_motoristas()

    def limpar_pesquisa(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Limpa a pesquisa e restaura o filtro padrão."""

        self.campo_pesquisa.value = ""
        self.filtro_situacao.value = "ATIVOS"

        self.pagina_atual = 1
        self.carregar_motoristas()

    def alterar_filtro_situacao(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Atualiza a lista conforme a situação selecionada."""

        self.pagina_atual = 1
        self.carregar_motoristas()

    # ==========================================================
    # CARREGAMENTO
    # ==========================================================

    def carregar_motoristas(self) -> None:
        """Carrega os motoristas da página atual."""

        self._iniciar_carregamento()

        pesquisa = str(
            self.campo_pesquisa.value or "",
        ).strip()

        somente_ativos = self.obter_filtro_ativos()

        try:
            self.motoristas = self.controller.listar(
                pesquisa=pesquisa,
                somente_ativos=somente_ativos,
                limite=self.ITENS_POR_PAGINA,
                pagina=self.pagina_atual,
            )

            self.total_registros = (
                self.controller.quantidade(
                    pesquisa=pesquisa,
                    somente_ativos=somente_ativos,
                )
            )

            total_paginas = self._calcular_total_paginas()

            if self.pagina_atual > total_paginas:
                self.pagina_atual = total_paginas

                self.motoristas = self.controller.listar(
                    pesquisa=pesquisa,
                    somente_ativos=somente_ativos,
                    limite=self.ITENS_POR_PAGINA,
                    pagina=self.pagina_atual,
                )

            self.preencher_tabela()
            self._atualizar_paginacao(
                total_paginas,
            )
            self._atualizar_estado_lista()

        except Exception as erro:
            self.motoristas = []
            self.tabela.rows.clear()
            self.container_tabela.visible = False
            self.mensagem_lista.visible = True
            self.mensagem_lista.value = (
                "Não foi possível carregar os motoristas."
            )

            mostrar_erro(
                self.page,
                str(erro),
            )

        finally:
            self._finalizar_carregamento()

    def _iniciar_carregamento(self) -> None:
        """Configura a interface para o estado de carregamento."""

        self.indicador_carregamento.visible = True
        self.mensagem_lista.visible = False
        self.estado_lista.visible = True
        self.container_tabela.visible = False
        self.paginacao.visible = False

        self.page.update()

    def _finalizar_carregamento(self) -> None:
        """Finaliza o estado de carregamento."""

        self.indicador_carregamento.visible = False

        if self.motoristas:
            self.estado_lista.visible = False

        self.page.update()

    def _atualizar_estado_lista(self) -> None:
        """Atualiza a tabela e a mensagem de lista vazia."""

        possui_registros = bool(
            self.motoristas,
        )

        self.container_tabela.visible = possui_registros
        self.estado_lista.visible = not possui_registros
        self.mensagem_lista.visible = not possui_registros
        self.paginacao.visible = possui_registros

        if not possui_registros:
            self.mensagem_lista.value = (
                "Nenhum motorista encontrado."
            )

    # ==========================================================
    # PAGINAÇÃO
    # ==========================================================

    def _calcular_total_paginas(self) -> int:
        """Calcula a quantidade total de páginas."""

        return max(
            1,
            (
                self.total_registros
                + self.ITENS_POR_PAGINA
                - 1
            )
            // self.ITENS_POR_PAGINA,
        )

    def _atualizar_paginacao(
        self,
        total_paginas: int,
    ) -> None:
        """Atualiza o texto e os botões da paginação."""

        self.texto_paginacao.value = (
            f"Página {self.pagina_atual} "
            f"de {total_paginas}"
        )

        self.botao_anterior.disabled = (
            self.pagina_atual <= 1
        )

        self.botao_proxima.disabled = (
            self.pagina_atual >= total_paginas
        )

    def pagina_anterior(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Navega para a página anterior."""

        if self.pagina_atual <= 1:
            return

        self.pagina_atual -= 1
        self.carregar_motoristas()

    def proxima_pagina(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Navega para a próxima página."""

        total_paginas = self._calcular_total_paginas()

        if self.pagina_atual >= total_paginas:
            return

        self.pagina_atual += 1
        self.carregar_motoristas()

    # ==========================================================
    # TABELA
    # ==========================================================

    def preencher_tabela(self) -> None:
        """Preenche a tabela com os motoristas carregados."""

        self.tabela.rows.clear()

        for motorista in self.motoristas:
            self.tabela.rows.append(
                self._criar_linha_motorista(
                    motorista,
                )
            )

    def _criar_linha_motorista(
        self,
        motorista: Motorista,
    ) -> ft.DataRow:
        """Cria uma linha da tabela para um motorista."""

        situacao = (
            "Ativo"
            if motorista.ativo
            else "Inativo"
        )

        return ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(
                        motorista.nome,
                        size=16,
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        self._formatar_telefone(
                            motorista.telefone,
                        ),
                        size=16,
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        motorista.cnh,
                        size=16,
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        motorista.categoria_cnh,
                        size=16,
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        situacao,
                        size=16,
                        color=(
                            ft.Colors.GREEN
                            if motorista.ativo
                            else ft.Colors.RED
                        ),
                    )
                ),
                ft.DataCell(
                    self._criar_acoes_motorista(
                        motorista,
                    )
                ),
            ],
        )

    def _criar_acoes_motorista(
        self,
        motorista: Motorista,
    ) -> ft.Row:
        """Cria os botões de ação do motorista."""

        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    tooltip="Editar",
                    mouse_cursor=ft.MouseCursor.CLICK,
                    on_click=lambda e, m=motorista: self.abrir_edicao(m),
                ),
                ft.IconButton(
                    icon=ft.Icons.PERSON_OFF_OUTLINED,
                    tooltip="Desativar",
                    visible=motorista.ativo,
                    icon_color=ft.Colors.RED_500,
                    on_click=lambda e, m=motorista: self._confirmar_desativacao(m),
                ),
                ft.IconButton(
                    icon=ft.Icons.RESTORE_ROUNDED,
                    tooltip="Reativar",
                    visible=not motorista.ativo,
                    icon_color=ft.Colors.GREEN_600,
                    on_click=lambda e, m=motorista: self._confirmar_reativacao(m),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        )

    @staticmethod
    def _formatar_telefone(
        telefone: str,
    ) -> str:
        """Formata o telefone celular para exibição."""

        digitos = "".join(
            caractere
            for caractere in str(telefone or "")
            if caractere.isdigit()
        )

        if len(digitos) == 11:
            return (
                f"({digitos[:2]}) "
                f"{digitos[2:7]}-"
                f"{digitos[7:]}"
            )

        if len(digitos) == 10:
            return (
                f"({digitos[:2]}) "
                f"{digitos[2:6]}-"
                f"{digitos[6:]}"
            )

        return str(
            telefone or "",
        )

    # ==========================================================
    # EXCLUSÃO E REATIVAÇÃO
    # ==========================================================

    def excluir_motorista(
        self,
        motorista: Motorista,
    ) -> None:
        """Realiza a exclusão lógica de um motorista."""

        if motorista.id is None:
            mostrar_erro(
                self.page,
                "Motorista sem identificador.",
            )
            return

        sucesso, mensagem = self.controller.excluir(
            motorista.id,
        )

        if sucesso:
            mostrar_sucesso(
                self.page,
                mensagem,
            )
        else:
            mostrar_erro(
                self.page,
                mensagem,
            )

        self.carregar_motoristas()

    def reativar_motorista(
        self,
        motorista: Motorista,
    ) -> None:
        """Reativa um motorista desativado."""

        if motorista.id is None:
            mostrar_erro(
                self.page,
                "Motorista sem identificador.",
            )
            return

        sucesso, mensagem = self.controller.reativar(
            motorista.id,
        )

        if sucesso:
            mostrar_sucesso(
                self.page,
                mensagem,
            )
        else:
            mostrar_erro(
                self.page,
                mensagem,
            )

        self.carregar_motoristas()

    def _confirmar_reativacao(
            self,
            motorista: Motorista,
    ) -> None:
        dialogo = ConfirmDialog(
            page=self.page,
            titulo="Reativar motorista",
            mensagem=(
                "Deseja realmente reativar o motorista?\n\n"
                f"{motorista.nome}"
            ),
            texto_confirmar="Reativar",
            texto_cancelar="Cancelar",
            cor_confirmar=ft.Colors.GREEN_700,
            icone=ft.Icons.RESTORE_ROUNDED,
            on_confirm=lambda: self.reativar_motorista(
                motorista
            ),
        )

        dialogo.abrir()

    def _confirmar_desativacao(
            self,
            motorista: Motorista,
    ) -> None:
        dialogo = ConfirmDialog(
            page=self.page,
            titulo="Desativar motorista",
            mensagem=(
                "Deseja realmente desativar o motorista?\n\n"
                f"{motorista.nome}\n\n"
                "O motorista poderá ser reativado posteriormente."
            ),
            texto_confirmar="Desativar",
            texto_cancelar="Cancelar",
            cor_confirmar=ft.Colors.RED_700,
            icone=ft.Icons.PERSON_OFF_ROUNDED,
            on_confirm=lambda: self.excluir_motorista(
                motorista
            ),
        )

        dialogo.abrir()