import flet as ft


class SearchField(ft.TextField):
    """Campo padrão de pesquisa do sistema."""

    def __init__(
        self,
        on_change=None,
        hint_text="Pesquisar...",
    ):
        super().__init__(
            prefix_icon=ft.Icons.SEARCH,
            hint_text=hint_text,
            border_radius=10,
            expand=True,
            on_change=on_change,
        )