from collections.abc import Callable

import flet as ft


class ConfirmDialog(ft.AlertDialog):
    """Diálogo reutilizável para confirmação de ações."""

    def __init__(
        self,
        page: ft.Page,
        titulo: str,
        mensagem: str,
        on_confirm: Callable[[], None],
        texto_confirmar: str = "Confirmar",
        texto_cancelar: str = "Cancelar",
        cor_confirmar: str = ft.Colors.RED_700,
        icone: str | None = ft.Icons.WARNING_AMBER_ROUNDED,
    ) -> None:
        self._page = page
        self._on_confirm = on_confirm

        super().__init__(
            modal=True,
            title=self._criar_titulo(
                titulo=titulo,
                icone=icone,
                cor=cor_confirmar,
            ),
            content=ft.Container(
                width=430,
                content=ft.Text(
                    mensagem,
                    size=15,
                    color=ft.Colors.GREY_800,
                ),
            ),
            actions=[
                ft.TextButton(
                    texto_cancelar,
                    on_click=self._ao_cancelar,
                ),
                ft.FilledButton(
                    texto_confirmar,
                    bgcolor=cor_confirmar,
                    color=ft.Colors.WHITE,
                    on_click=self._ao_confirmar,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    @staticmethod
    def _criar_titulo(
        titulo: str,
        icone: str | None,
        cor: str,
    ) -> ft.Control:
        """Cria o título visual do diálogo."""

        controles: list[ft.Control] = []

        if icone:
            controles.append(
                ft.Icon(
                    icone,
                    color=cor,
                    size=28,
                )
            )

        controles.append(
            ft.Text(
                titulo,
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREY_900,
            )
        )

        return ft.Row(
            controls=controles,
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def abrir(self) -> None:
        """Adiciona o diálogo à página e o abre."""

        if self not in self._page.overlay:
            self._page.overlay.append(self)

        self.open = True
        self._page.update()

    def fechar(self) -> None:
        """Fecha o diálogo sem removê-lo durante o evento."""

        self.open = False
        self._page.update()

    def _ao_cancelar(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Fecha o diálogo sem executar a ação."""

        self.fechar()

    def _ao_confirmar(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Fecha o diálogo e executa a ação confirmada."""

        self.fechar()

        if callable(self._on_confirm):
            self._on_confirm()