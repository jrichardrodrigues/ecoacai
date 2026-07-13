import flet as ft


def mostrar_mensagem(page: ft.Page, texto: str, cor=ft.Colors.BLUE):
    page.overlay.append(
        ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=cor,
            open=True,
        )
    )
    page.update()


def mostrar_sucesso(page: ft.Page, texto: str):
    mostrar_mensagem(page, texto, ft.Colors.GREEN)


def mostrar_erro(page: ft.Page, texto: str):
    mostrar_mensagem(page, texto, ft.Colors.RED)