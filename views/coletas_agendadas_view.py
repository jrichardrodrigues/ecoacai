import flet as ft

from controllers import ColetasAgendadasController
from components.layout import criar_app_bar, criar_menu


class ColetasAgendadasView:
    """Tela de acompanhamento das coletas agendadas."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = ColetasAgendadasController()

    def build(self) -> ft.View:
        return ft.View(
            route="/coletas-agendadas",
            appbar=criar_app_bar(),
            controls=[
                ft.Row(
                    controls=[
                        criar_menu(self.page),
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            padding=20,
                            expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Coletas Agendadas",
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Acompanhe e execute as operações das coletas agendadas.",
                                        color=ft.Colors.GREY_700,
                                    ),
                                    ft.Divider(),
                                ],
                                spacing=15,
                            ),
                        ),
                    ],
                    expand=True,
                ),
            ],
        )