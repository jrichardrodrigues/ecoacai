import flet as ft


def abrir_snackbar(
    page: ft.Page,
    mensagem: str,
    bgcolor=None,
) -> ft.SnackBar:
    snackbar = ft.SnackBar(
        content=ft.Text(mensagem),
        bgcolor=bgcolor,
    )

    if hasattr(page, "open") and callable(page.open):
        page.open(snackbar)
    else:
        snackbar.open = True
        page.overlay.append(snackbar)
        page.update()

    return snackbar


def abrir_dialogo(
    page: ft.Page,
    dialogo: ft.AlertDialog,
):
    if hasattr(page, "open") and callable(page.open):
        page.open(dialogo)
    else:
        page.dialog = dialogo
        dialogo.open = True
        page.update()


def fechar_dialogo(
    page: ft.Page,
    dialogo: ft.AlertDialog,
):
    dialogo.open = False
    page.update()