from collections.abc import Callable

import flet as ft

from components.tables import (
    EstabelecimentoTable,
    Toolbar,
)
from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from models import Estabelecimento
from utils.messages import mostrar_erro, mostrar_sucesso
from components.dialogs import confirmar_exclusao


class EstabelecimentosView:
    """Tela de listagem e gerenciamento de estabelecimentos."""

    def __init__(
            self,
            page: ft.Page,
            on_novo: Callable[[], None] | None = None,
            on_editar: Callable[[Estabelecimento], None] | None = None,
            on_solicitar_coleta: Callable[[int], None] | None = None,
    ) -> None:
        self.page = page
        self.on_novo = on_novo
        self.on_editar = on_editar
        self.on_solicitar_coleta = on_solicitar_coleta

        self.controller = EstabelecimentoController()

        self.toolbar = Toolbar(
            titulo="Estabelecimentos",
            on_search=self.pesquisar,
            on_add=self.novo,
        )

        self.total = ft.Text(
            "",
            size=14,
            color=ft.Colors.GREY_700,
        )

        self.sem_registros = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.INBOX_OUTLINED,
                        size=64,
                        color=ft.Colors.GREY_400,
                    ),
                    ft.Text(
                        "Nenhum estabelecimento cadastrado.",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Clique em 'Novo' para cadastrar "
                        "o primeiro estabelecimento.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            expand=True,
            visible=False,
        )

        self.tabela = EstabelecimentoTable(
            on_edit=self.editar,
            on_delete=self.excluir,
            on_collect=self.solicitar_coleta,
        )

        self.atualizar_tabela()

    def atualizar_tabela(
        self,
        pesquisa: str = "",
    ) -> None:
        """Consulta os dados e atualiza a tabela."""

        estabelecimentos = (
            self.controller.listar_estabelecimentos(
                pesquisa=pesquisa,
            )
        )

        quantidade = len(estabelecimentos)

        self.total.value = (
            f"Total de estabelecimentos: {quantidade}"
        )

        self.tabela.carregar(estabelecimentos)

        tem_registros = quantidade > 0

        self.tabela.visible = tem_registros
        self.sem_registros.visible = not tem_registros

    def pesquisar(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Filtra os estabelecimentos em tempo real."""

        self.atualizar_tabela(
            pesquisa=e.control.value or "",
        )

        self.page.update()

    def novo(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Abre o formulário para um novo cadastro."""

        if self.on_novo is None:
            mostrar_erro(
                self.page,
                "Não foi possível abrir o cadastro.",
            )
            return

        self.on_novo()

    def editar(
        self,
        estabelecimento_id: int | None,
    ) -> None:
        """Busca o registro e abre o formulário de edição."""

        if estabelecimento_id is None:
            mostrar_erro(
                self.page,
                "Estabelecimento sem identificador.",
            )
            return

        estabelecimento = (
            self.controller.buscar_estabelecimento_por_id(
                estabelecimento_id,
            )
        )

        if estabelecimento is None:
            mostrar_erro(
                self.page,
                "Estabelecimento não encontrado.",
            )
            return

        if self.on_editar is None:
            mostrar_erro(
                self.page,
                "Não foi possível abrir a edição.",
            )
            return

        self.on_editar(estabelecimento)

    def excluir(
            self,
            estabelecimento_id: int | None,
    ) -> None:
        """Solicita confirmação antes de excluir."""

        if estabelecimento_id is None:
            mostrar_erro(
                self.page,
                "Estabelecimento sem identificador.",
            )
            return

        def confirmar():

            sucesso, mensagem = (
                self.controller.excluir_estabelecimento(
                    estabelecimento_id,
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

            self.atualizar_tabela(
                pesquisa=self.toolbar.search.value or "",
            )

            self.page.update()

        confirmar_exclusao(
            page=self.page,
            mensagem="Deseja realmente excluir este estabelecimento?",
            on_confirm=confirmar,
        )

    def solicitar_coleta(
            self,
            estabelecimento_id: int | None,
    ) -> None:
        """Abre uma nova solicitação para o estabelecimento."""

        if estabelecimento_id is None:
            mostrar_erro(
                self.page,
                "Estabelecimento sem identificador.",
            )
            return

        if self.on_solicitar_coleta is None:
            mostrar_erro(
                self.page,
                "Não foi possível abrir a solicitação de coleta.",
            )
            return

        self.on_solicitar_coleta(estabelecimento_id)

    def build(self) -> ft.Control:
        """Constrói e retorna a tela."""

        return ft.Column(
            controls=[
                self.toolbar,
                self.total,
                ft.Stack(
                    controls=[
                        self.sem_registros,
                        self.tabela,
                    ],
                    expand=True,
                ),
            ],
            spacing=15,
            expand=True,
        )