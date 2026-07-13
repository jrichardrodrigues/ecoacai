import flet as ft


def campo_texto(label: str):
    return ft.TextField(
        label=label,
        expand=True,
        border_radius=10,
    )