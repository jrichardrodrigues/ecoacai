from __future__ import annotations

import flet as ft

from components.ui import theme


class AuthFooter(ft.Column):
    def __init__(self, version: str = "0.9.1") -> None:
        texto = f"Versão {version} • ZELURBIS" if version else "ZELURBIS"

        super().__init__(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.LOCK_OUTLINE,
                            size=theme.ICON_SM,
                            color=theme.SUCCESS,
                        ),
                        ft.Text(
                            "Acesso protegido e seguro",
                            size=theme.CAPTION,
                            color=theme.TEXT_SECONDARY,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=theme.SPACE_XS,
                ),
                ft.Text(
                    texto,
                    size=theme.CAPTION,
                    color=theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=theme.SPACE_XS,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
