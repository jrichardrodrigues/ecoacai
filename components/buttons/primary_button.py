import flet as ft

from components.theme import Colors, Radius


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
            content=ft.Text(label),
            icon=icon,
            on_click=on_click,
            width=width,
            height=48,
            expand=expand,
            disabled=disabled,
            bgcolor={
                ft.ControlState.DEFAULT: Colors.PRIMARY,
                ft.ControlState.DISABLED: ft.Colors.GREY_300,
            },
            color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                ft.ControlState.DISABLED: ft.Colors.GREY_600,
            },
            style=ft.ButtonStyle(
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