from __future__ import annotations

import flet as ft


class ResponsiveTable(ft.Container):
    """
    Contêiner responsivo para tabelas do sistema.

    Mantém a tabela com uma largura mínima estável e oferece
    rolagem horizontal automaticamente quando a largura
    disponível não for suficiente.
    """

    def __init__(
            self,
            *,
            content: ft.Control,
            min_width: int = 1300,
            border: ft.Border | None = None,
            border_radius: int = 8,
            padding: int = 0,
    ) -> None:
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=content,
                        width=min_width,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS,
            ),
            border=border,
            border_radius=border_radius,
            padding=padding,
            expand=True,
        )