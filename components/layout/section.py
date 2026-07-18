import flet as ft

from components.layout import SectionHeader
from components.theme import Spacing


class Section(ft.Column):
    """Seção padronizada da interface."""

    def __init__(
        self,
        title: str,
        content: ft.Control,
        show_divider: bool = True,
    ):
        controls = [
            SectionHeader(title),
            content,
        ]

        if show_divider:
            controls.append(ft.Divider())

        super().__init__(
            controls=controls,
            spacing=Spacing.MD,
        )