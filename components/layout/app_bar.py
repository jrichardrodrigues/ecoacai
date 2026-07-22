import flet as ft

from config import APP_NAME, APP_SUBTITLE, COR_PRIMARIA


def criar_app_bar() -> ft.AppBar:
    """Cria a barra institucional da plataforma."""

    return ft.AppBar(
        automatically_imply_leading=False,
        toolbar_height=72,
        bgcolor=COR_PRIMARIA,
        title_spacing=20,
        title=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.ECO,
                    color=ft.Colors.WHITE,
                    size=38,
                ),
                ft.Text(
                    APP_NAME,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(
                    width=1,
                    height=32,
                    bgcolor=ft.Colors.with_opacity(0.40, ft.Colors.WHITE),
                ),
                ft.Text(
                    APP_SUBTITLE.upper(),
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                ),
            ],
        ),
    )