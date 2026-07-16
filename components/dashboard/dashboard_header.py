from datetime import datetime

import flet as ft


class DashboardHeader(ft.Card):
    """Cabeçalho inteligente do Dashboard."""

    def __init__(
        self,
        pendentes: int,
        agendadas: int,
        em_coleta: int,
    ) -> None:

        agora = datetime.now()

        if agora.hour < 12:
            saudacao = "Bom dia"
        elif agora.hour < 18:
            saudacao = "Boa tarde"
        else:
            saudacao = "Boa noite"

        data = agora.strftime("%d/%m/%Y")

        mensagem = (
            f"Hoje existem "
            f"{pendentes} pendentes, "
            f"{agendadas} agendadas "
            f"e {em_coleta} em coleta."
        )

        super().__init__(
            elevation=2,
            content=ft.Container(
                padding=20,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(
                                    f"👋 {saudacao}!",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    mensagem,
                                    size=15,
                                    color=ft.Colors.GREY_700,
                                ),
                            ],
                        ),
                        ft.Text(
                            data,
                            size=15,
                            color=ft.Colors.GREY_600,
                        ),
                    ],
                ),
            ),
        )