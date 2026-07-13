import flet as ft


def card_titulo(titulo: str):
    return ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Text(
                titulo,
                size=24,
                weight=ft.FontWeight.BOLD,
            ),
        )
    )