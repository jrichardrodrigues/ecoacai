import flet as ft

from components.theme import Colors, Radius, Spacing


class PrimaryButton(ft.ElevatedButton):
    """Botão principal do Design System EcoAçaí."""

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
            bgcolor=Colors.PRIMARY,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                padding=ft.Padding.symmetric(
                    horizontal=Spacing.LG,
                    vertical=Spacing.SM,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=Radius.BUTTON,
                ),
            ),
        )