from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.ui import theme


class AuthFields(ft.Column):
    def __init__(self, controls: Sequence[ft.Control]) -> None:
        super().__init__(
            controls=list(controls),
            spacing=theme.SPACE_MD,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
