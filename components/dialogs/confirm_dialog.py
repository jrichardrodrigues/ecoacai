import flet as ft


def confirmar_exclusao(page: ft.Page, on_confirmar):
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar exclusão"),
        content=ft.Text("Deseja realmente excluir este cadastro?"),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: fechar_dialogo(page, dialog),
            ),
            ft.TextButton(
                "Excluir",
                on_click=on_confirmar,
            ),
        ],
    )

    page.dialog = dialog
    dialog.open = True
    page.update()


def fechar_dialogo(page: ft.Page, dialog: ft.AlertDialog):
    dialog.open = False
    page.update()