import flet as ft


def criar_app_bar():
    return ft.AppBar(
        title=ft.Text(
            "Controle de Recolhimento de Caroço do Açaí",
            weight=ft.FontWeight.BOLD,
        ),
        center_title=False,
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
    )