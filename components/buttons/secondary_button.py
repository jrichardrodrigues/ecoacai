import flet as ft

from components.theme import Colors, Radius, Spacing


class SecondaryButton(ft.OutlinedButton):
    """Botão secundário do Design System EcoAçaí."""

    def __init__(
        self,
        label: str,
        on_click=None,
        icon=None,
        width: int | None = None,
        expand: bool = False,
        disabled: bool = False,
    ):
        super().__init__(
            content=label,
            icon=icon,
            on_click=on_click,
            width=width,
            height=Spacing.BUTTON_HEIGHT,
            expand=expand,
            disabled=disabled,
            style=ft.ButtonStyle(
                color=Colors.PRIMARY,
                side=ft.BorderSide(
                    width=1.5,
                    color=Colors.PRIMARY,
                ),
                padding=ft.Padding.symmetric(
                    horizontal=Spacing.LG,
                    vertical=Spacing.SM,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=Radius.BUTTON,
                ),
            ),
        )