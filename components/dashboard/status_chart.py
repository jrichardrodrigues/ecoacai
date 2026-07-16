import flet as ft


class StatusChart(ft.Card):
    """Gráfico horizontal das solicitações por status."""

    def __init__(
        self,
        pendentes: int,
        agendadas: int,
        em_coleta: int,
        concluidas: int,
    ) -> None:
        valores = {
            "Pendentes": (
                pendentes,
                ft.Colors.AMBER_700,
            ),
            "Agendadas": (
                agendadas,
                ft.Colors.BLUE,
            ),
            "Em coleta": (
                em_coleta,
                ft.Colors.ORANGE_700,
            ),
            "Concluídas": (
                concluidas,
                ft.Colors.GREEN_700,
            ),
        }

        maior_valor = max(
            pendentes,
            agendadas,
            em_coleta,
            concluidas,
            1,
        )

        linhas: list[ft.Control] = []

        for titulo, dados in valores.items():
            valor, cor = dados

            largura_barra = int(
                (valor / maior_valor) * 100
            )

            largura_restante = 100 - largura_barra

            controles_barra: list[ft.Control] = []

            if largura_barra > 0:
                controles_barra.append(
                    ft.Container(
                        height=12,
                        expand=largura_barra,
                        bgcolor=cor,
                        border_radius=6,
                    )
                )

            if largura_restante > 0:
                controles_barra.append(
                    ft.Container(
                        height=12,
                        expand=largura_restante,
                        bgcolor=ft.Colors.GREY_200,
                        border_radius=6,
                    )
                )

            linhas.append(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    titulo,
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    expand=True,
                                ),
                                ft.Text(
                                    str(valor),
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                        ft.Row(
                            controls=controles_barra,
                            spacing=0,
                        ),
                    ],
                    spacing=5,
                )
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
                                    ft.Icons.BAR_CHART,
                                    size=20,
                                ),
                                ft.Text(
                                    "Distribuição por status",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Divider(),
                        *linhas,
                    ],
                    spacing=14,
                ),
            ),
        )