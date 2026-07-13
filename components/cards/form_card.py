import flet as ft

from components.theme import (
    Colors,
    Radius,
    Spacing,
)


class FormCard(ft.Container):

    def __init__(
        self,
        content,
        width=520,
    ):
        super().__init__()

        self.width = width

        self.padding = Spacing.XL

        self.border_radius = Radius.XL

        self.bgcolor = Colors.SURFACE

        self.shadow = ft.BoxShadow(
            blur_radius=18,
            spread_radius=0,
            offset=ft.Offset(0, 4),
            color=ft.Colors.with_opacity(
                0.08,
                ft.Colors.BLACK,
            ),
        )

        self.content = content