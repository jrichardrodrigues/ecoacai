from __future__ import annotations

from typing import Iterable

import flet as ft


class ResponsiveFilterBar(ft.Row):
    """
    Barra responsiva para campos de filtro e botões de ação.

    Os controles permanecem na mesma linha enquanto houver
    espaço disponível.
    """

    def __init__(
            self,
            *,
            controls: Iterable[ft.Control],
            spacing: int = 12,
            run_spacing: int = 12,
    ) -> None:
        super().__init__(
            controls=list(controls),
            spacing=spacing,
            run_spacing=run_spacing,
            wrap=False,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )