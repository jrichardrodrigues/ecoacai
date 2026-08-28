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
                ft.DataColumn(
                    ft.Text("Nome", size=17, weight=ft.FontWeight.W_600)
                ),
                ft.DataColumn(
                    ft.Text("CPF", size=17, weight=ft.FontWeight.W_600)
                ),
                ft.DataColumn(
                    ft.Text("Celular", size=17, weight=ft.FontWeight.W_600)
                ),
                ft.DataColumn(
                    ft.Text("Bairro", size=17, weight=ft.FontWeight.W_600)
                ),
                ft.DataColumn(
                    ft.Text("Setor", size=17, weight=ft.FontWeight.W_600)
                ),
                ft.DataColumn(
                    ft.Text("Situação", size=17, weight=ft.FontWeight.W_600)
                ),
                ft.DataColumn(
                    ft.Text("Ações", size=17, weight=ft.FontWeight.W_600)
                ),
            ],
        )

        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_collect = on_collect

    @staticmethod
    def _formatar_cpf(cpf: str) -> str:
        """Formata o CPF para exibição."""

        digitos = "".join(
            caractere
            for caractere in str(cpf or "")
            if caractere.isdigit()
        )

        if len(digitos) != 11:
            return str(cpf or "")

        return (
            f"{digitos[:3]}."
            f"{digitos[3:6]}."
            f"{digitos[6:9]}-"
            f"{digitos[9:]}"
        )

    @staticmethod
    def _formatar_celular(celular: str) -> str:
        """Formata o celular para exibição."""

        digitos = "".join(
            caractere
            for caractere in str(celular or "")
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

        return str(celular or "")

    def carregar(self, estabelecimentos):

        rows = []

        for estabelecimento in estabelecimentos:

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(estabelecimento.nome, size=16)
                        ),
                        ft.DataCell(
                            ft.Text(
                                self._formatar_cpf(
                                    estabelecimento.cpf
                                ),
                                size=16,
                                no_wrap=True,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                self._formatar_celular(
                                    estabelecimento.celular
                                ),
                                size=16,
                                no_wrap=True,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(estabelecimento.bairro, size=16)
                        ),
                        ft.DataCell(
                            ft.Text(estabelecimento.setor, size=16)
                        ),
                        ft.DataCell(
                            ft.Text(
                                "Ativo"
                                if estabelecimento.ativo
                                else "Inativo",
                                size=16,
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