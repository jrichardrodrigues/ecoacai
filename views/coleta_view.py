import flet as ft

from controllers import SolicitacaoColetaController


class ColetasView:
    """Tela de Coletas Ativas."""

    def __init__(self, page: ft.Page):
        self.page = page

        self.txt_pesquisa = ft.TextField(
            hint_text="Pesquisar estabelecimento...",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
        )

        self.controller = SolicitacaoColetaController()

        self.tabela = ft.DataTable(
            expand=True,
            columns=[
                ft.DataColumn(ft.Text("Estabelecimento")),
                ft.DataColumn(ft.Text("Data")),
                ft.DataColumn(ft.Text("Quantidade")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Nenhum registro encontrado")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text("-")),
                    ]
                )
            ],
        )

        self.btn_nova = ft.ElevatedButton(
            text="Nova Coleta",
            icon=ft.Icons.ADD,
            width=180,
        )

    def build(self):
        self.carregar_dados()
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                spacing=20,
                controls=[
                    ft.Text(
                        "Coletas Ativas",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),

                    self.txt_pesquisa,

                    ft.Container(
                        expand=True,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        padding=10,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                self.tabela,
                            ],
                        ),
                    ),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            self.btn_nova,
                        ],
                    ),
                ],
            ),
        )

    def carregar_dados(self):
        """Carrega as solicitações do banco e preenche a tabela."""

        self.tabela.rows.clear()

        solicitacoes = self.controller.listar_com_estabelecimento()

        if not solicitacoes:
            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Nenhum registro encontrado")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text("-")),
                    ]
                )
            )
            return

        for solicitacao in solicitacoes:

            if solicitacao.quantidade_kg > 0:
                quantidade = f"{solicitacao.quantidade_kg:.1f} kg"
            else:
                quantidade = f"{solicitacao.quantidade_sacas} sacas"

            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(str(solicitacao.estabelecimento_id))
                        ),
                        ft.DataCell(
                            ft.Text(solicitacao.data_solicitacao or "")
                        ),
                        ft.DataCell(
                            ft.Text(quantidade)
                        ),
                        ft.DataCell(
                            ft.Text(solicitacao.status)
                        ),
                        ft.DataCell(
                            ft.Row(
                                spacing=0,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar",
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.CHECK_CIRCLE,
                                        tooltip="Alterar Status",
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Excluir",
                                    ),
                                ],
                            )
                        ),
                    ]
                )
            )