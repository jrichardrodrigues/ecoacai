from collections.abc import Callable

import flet as ft

from config import COR_ECOACAI

def criar_app_bar(
    on_voltar_zelurbis: Callable[[], None] | None = None,
) -> ft.AppBar:
    """Cria a barra institucional do módulo ECOAÇAÍ."""

    actions: list[ft.Control] = []

    if on_voltar_zelurbis is not None:
        actions.append(
            ft.TextButton(
                content="ZELURBIS",
                icon=ft.Icons.ARROW_BACK_ROUNDED,
                on_click=lambda _e: on_voltar_zelurbis(),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                ),
            )
        )

    return ft.AppBar(
        automatically_imply_leading=False,
        toolbar_height=72,
        bgcolor=COR_ECOACAI,
        title_spacing=20,
        title=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.ECO_ROUNDED,
                    color=ft.Colors.WHITE,
                    size=38,
                ),
                ft.Text(
                    "ECOAÇAÍ",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(
                    width=1,
                    height=32,
                    bgcolor=ft.Colors.with_opacity(
                        0.40,
                        ft.Colors.WHITE,
                    ),
                ),
                ft.Text(
                    "GESTÃO INTELIGENTE DE RESÍDUO DO AÇAÍ",
                    size=17,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                ),
            ],
        ),
        actions=actions,
    )