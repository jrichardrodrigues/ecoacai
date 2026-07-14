import flet as ft

from components.tables import (
    ActionButtons,
    DataTable,
    Toolbar,
)
from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from utils.messages import mostrar_erro, mostrar_sucesso


class EstabelecimentosView:
    """Tela de listagem e gerenciamento de estabelecimentos."""

    def __init__(
            self,
            page: ft.Page,
            on_novo=None,
    ) -> None:
        self.page = page
        self.on_novo = on_novo

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

        self.tabela = DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("CPF")),
                ft.DataColumn(ft.Text("Celular")),
                ft.DataColumn(ft.Text("Bairro")),
                ft.DataColumn(ft.Text("Setor")),
                ft.DataColumn(ft.Text("Situação")),
                ft.DataColumn(ft.Text("Ações")),
            ],
        )

        self.atualizar_tabela()

    def atualizar_tabela(
        self,
        pesquisa: str = "",
    ) -> None:
        """Carrega os registros e atualiza a tabela."""

        estabelecimentos = (
            self.controller.listar_estabelecimentos(
                pesquisa=pesquisa,
            )
        )

        self.total.value = (
            f"Total de estabelecimentos: "
            f"{len(estabelecimentos)}"
        )

        linhas: list[ft.DataRow] = []

        for estabelecimento in estabelecimentos:
            estabelecimento_id = estabelecimento.id

            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(estabelecimento.nome),
                        ),
                        ft.DataCell(
                            ft.Text(estabelecimento.cpf),
                        ),
                        ft.DataCell(
                            ft.Text(estabelecimento.celular),
                        ),
                        ft.DataCell(
                            ft.Text(estabelecimento.bairro),
                        ),
                        ft.DataCell(
                            ft.Text(estabelecimento.setor),
                        ),
                        ft.DataCell(
                            ft.Text(
                                "Ativo"
                                if estabelecimento.ativo
                                else "Inativo",
                            ),
                        ),
                        ft.DataCell(
                            ActionButtons(
                                on_edit=(
                                    lambda e,
                                    item_id=estabelecimento_id:
                                    self.editar(item_id)
                                ),
                                on_delete=(
                                    lambda e,
                                    item_id=estabelecimento_id:
                                    self.excluir(item_id)
                                ),
                                on_collect=(
                                    lambda e,
                                    item_id=estabelecimento_id:
                                    self.solicitar_coleta(item_id)
                                ),
                            ),
                        ),
                    ],
                ),
            )

        self.tabela.atualizar(linhas)

        tem_registros = bool(linhas)

        self.tabela.visible = tem_registros
        self.sem_registros.visible = not tem_registros

    def pesquisar(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Filtra a listagem conforme o texto informado."""

        self.atualizar_tabela(
            pesquisa=e.control.value or "",
        )

        self.page.update()

    def novo(self, e):

        if self.on_novo:
            self.on_novo()

    def editar(
        self,
        estabelecimento_id: int | None,
    ) -> None:
        """Ação temporária de edição."""

        if estabelecimento_id is None:
            mostrar_erro(
                self.page,
                "Estabelecimento sem identificador.",
            )
            return

        mostrar_erro(
            self.page,
            f"A edição do estabelecimento "
            f"{estabelecimento_id} será implementada "
            f"na próxima etapa.",
        )

    def excluir(
        self,
        estabelecimento_id: int | None,
    ) -> None:
        """Realiza a exclusão lógica do registro."""

        if estabelecimento_id is None:
            mostrar_erro(
                self.page,
                "Estabelecimento sem identificador.",
            )
            return

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

    def solicitar_coleta(
        self,
        estabelecimento_id: int | None,
    ) -> None:
        """Ação temporária para solicitação de coleta."""

        if estabelecimento_id is None:
            mostrar_erro(
                self.page,
                "Estabelecimento sem identificador.",
            )
            return

        mostrar_erro(
            self.page,
            f"A solicitação de coleta do estabelecimento "
            f"{estabelecimento_id} será implementada "
            f"na próxima etapa.",
        )

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