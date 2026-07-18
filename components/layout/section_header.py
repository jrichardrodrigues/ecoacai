import flet as ft

from components.theme import Colors, Typography


class SectionHeader(ft.Text):
    """Título padronizado para seções da aplicação."""

    def __init__(self, titulo: str):
        super().__init__(
            value=titulo,
            size=Typography.H4,
            weight=ft.FontWeight.BOLD,
            color=Colors.Text.PRIMARY,
        )