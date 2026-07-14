import flet as ft

from .search_field import SearchField


class Toolbar(ft.Row):
    """Barra superior das telas de listagem."""

    def __init__(
        self,
        titulo: str,
        on_search=None,
        on_add=None,
    ):
        self.search = SearchField(
            on_change=on_search,
        )

        botao = ft.ElevatedButton(
            "Novo",
            icon=ft.Icons.ADD,
            on_click=on_add,
        )

        super().__init__(
            controls=[
                ft.Text(
                    titulo,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                self.search,
                botao,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )