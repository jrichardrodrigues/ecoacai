import flet as ft

from components.theme import Colors, Radius


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
            content=ft.Text(label),
            icon=icon,
            on_click=on_click,
            width=width,
            height=48,
            expand=expand,
            disabled=disabled,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: Colors.PRIMARY,
                    ft.ControlState.DISABLED: ft.Colors.GREY_500,
                },
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(
                        width=1,
                        color=Colors.PRIMARY,
                    ),
                    ft.ControlState.DISABLED: ft.BorderSide(
                        width=1,
                        color=ft.Colors.GREY_300,
                    ),
                },
                padding=ft.Padding(
                    left=16,
                    top=10,
                    right=16,
                    bottom=10,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=Radius.MD,
                ),
            ),
        )