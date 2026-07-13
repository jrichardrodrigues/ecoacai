from collections.abc import Callable

import flet as ft


def criar_text_button(
    label: str,
    on_click: Callable | None = None,
    icon=None,
    **kwargs,
) -> ft.TextButton:
    return ft.TextButton(
        content=label,
        icon=icon,
        on_click=on_click,
        **kwargs,
    )


def criar_elevated_button(
    label: str,
    on_click: Callable | None = None,
    icon=None,
    **kwargs,
) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        content=label,
        icon=icon,
        on_click=on_click,
        **kwargs,
    )


def criar_outlined_button(
    label: str,
    on_click: Callable | None = None,
    icon=None,
    **kwargs,
) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        content=label,
        icon=icon,
        on_click=on_click,
        **kwargs,
    )