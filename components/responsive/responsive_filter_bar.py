from __future__ import annotations

from typing import Iterable

import flet as ft


class ResponsiveFilterBar(ft.Row):
    """
    Barra responsiva para campos de filtro e botões de ação.

    Por padrão, os controles permanecem na mesma linha.
    O comportamento de quebra pode ser habilitado pela tela
    quando necessário.
    """

    def __init__(
            self,
            *,
            controls: Iterable[ft.Control],
            spacing: int = 12,
            run_spacing: int = 12,
            wrap: bool = False,
    ) -> None:
        super().__init__(
            controls=list(controls),
            spacing=spacing,
            run_spacing=run_spacing,
            wrap=wrap,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )