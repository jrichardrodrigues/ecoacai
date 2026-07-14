import flet as ft

from .action_buttons import ActionButtons
from .data_table import DataTable


class EstabelecimentoTable(DataTable):

    def __init__(
        self,
        on_edit=None,
        on_delete=None,
        on_collect=None,
    ):
        super().__init__(
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

        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_collect = on_collect

    def carregar(self, estabelecimentos):

        rows = []

        for estabelecimento in estabelecimentos:

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(estabelecimento.nome)),
                        ft.DataCell(ft.Text(estabelecimento.cpf)),
                        ft.DataCell(ft.Text(estabelecimento.celular)),
                        ft.DataCell(ft.Text(estabelecimento.bairro)),
                        ft.DataCell(ft.Text(estabelecimento.setor)),
                        ft.DataCell(
                            ft.Text(
                                "Ativo"
                                if estabelecimento.ativo
                                else "Inativo"
                            )
                        ),
                        ft.DataCell(
                            ActionButtons(
                                on_edit=lambda e, id=estabelecimento.id: self.on_edit(id),
                                on_delete=lambda e, id=estabelecimento.id: self.on_delete(id),
                                on_collect=lambda e, id=estabelecimento.id: self.on_collect(id),
                            )
                        ),
                    ]
                )
            )

        self.atualizar(rows)