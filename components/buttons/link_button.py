import flet as ft

from components.compatibility import criar_text_button
from components.theme import Colors


def LinkButton(
    label: str,
    on_click=None,
    icon=None,
):
    """Cria um botão de link com o padrão visual da aplicação."""

    return criar_text_button(
        label=label,
        icon=icon,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=Colors.PRIMARY,
        ),
    )