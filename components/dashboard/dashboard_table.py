import flet as ft


class DashboardTable(ft.Card):
    """Tabela das últimas solicitações."""

    def __init__(
        self,
        solicitacoes: list[dict],
    ) -> None:
        linhas: list[ft.DataRow] = []

        for solicitacao in solicitacoes:
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                str(
                                    solicitacao.get(
                                        "codigo",
                                        "",
                                    )
                                ),
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(
                                    solicitacao.get(
                                        "estabelecimento",
                                        "",
                                    )
                                )
                            )
                        ),
                        ft.DataCell(
                            self._status_chip(
                                str(
                                    solicitacao.get(
                                        "status",
                                        "",
                                    )
                                )
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(
                                    solicitacao.get(
                                        "quantidade_sacas",
                                        0,
                                    )
                                )
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                self._formatar_peso(
                                    solicitacao.get(
                                        "quantidade_kg",
                                        0,
                                    )
                                )
                            )
                        ),
                    ]
                )
            )

        conteudo_tabela: ft.Control

        if linhas:
            conteudo_tabela = ft.DataTable(
                columns=[
                    ft.DataColumn(
                        ft.Text(
                            "Número",
                            weight=ft.FontWeight.BOLD,
                        )
                    ),
                    ft.DataColumn(
                        ft.Text(
                            "Estabelecimento",
                            weight=ft.FontWeight.BOLD,
                        )
                    ),
                    ft.DataColumn(
                        ft.Text(
                            "Status",
                            weight=ft.FontWeight.BOLD,
                        )
                    ),
                    ft.DataColumn(
                        ft.Text(
                            "Sacas",
                            weight=ft.FontWeight.BOLD,
                        ),
                        numeric=True,
                    ),
                    ft.DataColumn(
                        ft.Text(
                            "Kg",
                            weight=ft.FontWeight.BOLD,
                        ),
                        numeric=True,
                    ),
                ],
                rows=linhas,
            )
        else:
            conteudo_tabela = ft.Container(
                content=ft.Text(
                    "Nenhuma solicitação cadastrada.",
                    italic=True,
                    color=ft.Colors.GREY_600,
                ),
                padding=10,
            )

        super().__init__(
            elevation=2,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.ASSIGNMENT_OUTLINED,
                                    size=20,
                                ),
                                ft.Text(
                                    "Últimas solicitações",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Divider(),
                        conteudo_tabela,
                    ],
                    spacing=10,
                ),
            ),
        )

    @staticmethod
    def _status_chip(status: str) -> ft.Container:
        """Retorna um badge colorido para o status."""

        cores = {
            "PENDENTE": ft.Colors.AMBER_100,
            "AGENDADA": ft.Colors.BLUE_100,
            "EM_COLETA": ft.Colors.ORANGE_100,
            "CONCLUIDA": ft.Colors.GREEN_100,
        }

        return ft.Container(
            content=ft.Text(
                status.replace("_", " "),
                size=12,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=cores.get(
                status,
                ft.Colors.GREY_200,
            ),
            border_radius=20,
            padding=ft.Padding(
                left=10,
                top=5,
                right=10,
                bottom=5,
            ),
        )

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