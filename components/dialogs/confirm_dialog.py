import flet as ft


class ConfirmDialog(ft.AlertDialog):
    """Diálogo reutilizável para confirmação."""

    def __init__(
        self,
        page: ft.Page,
        titulo: str,
        mensagem: str,
        on_confirm,
    ):
        self._page = page
        self.on_confirm = on_confirm

        super().__init__(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Text(mensagem),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=self.cancelar,
                ),
                ft.FilledButton(
                    "Excluir",
                    on_click=self.confirmar,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def cancelar(self, e):
        self.open = False
        self._page.update()

    def confirmar(self, e):
        self.open = False
        self._page.update()

        if self.on_confirm:
            self.on_confirm()