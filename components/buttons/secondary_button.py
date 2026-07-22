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
                color=Colors.PRIMARY,
                side=ft.BorderSide(
                    width=1,
                    color=Colors.PRIMARY,
                ),
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