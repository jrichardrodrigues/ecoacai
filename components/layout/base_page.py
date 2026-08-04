from __future__ import annotations

import flet as ft

from components.layout.page_header import PageHeader
from components.theme import (
    Colors,
    Radius,
    Shadows,
    Spacing,
)


class BasePage(ft.Container):
    """
    Página base da Plataforma ZELURBIS.

    Todas as telas da aplicação deverão herdar desta classe
    para manter identidade visual, espaçamentos e comportamento
    consistentes.
    """

    def __init__(
        self,
        *,
        title: str,
        subtitle: str | None = None,
        content: ft.Control | None = None,
        actions: list[ft.Control] | None = None,
        expand: bool = True,
        scroll: ft.ScrollMode = ft.ScrollMode.AUTO,
        max_width: int = 1200,
        bgcolor: str | None = None,
    ) -> None:

        actions = actions or []

        body_controls: list[ft.Control] = [
            PageHeader(
                title=title,
                subtitle=subtitle,
            )
        ]

        if content is not None:
            body_controls.append(content)

        if actions:
            body_controls.append(
                ft.Row(
                    controls=actions,
                    alignment=ft.MainAxisAlignment.END,
                    spacing=Spacing.MD,
                )
            )

        body = ft.Column(
            controls=body_controls,
            spacing=Spacing.LG,
            expand=True,
            scroll=scroll,
        )

        super().__init__(
            expand=expand,
            bgcolor=bgcolor or Colors.Background.DEFAULT,
            padding=Spacing.PAGE_PADDING,
            alignment=ft.alignment.top_center,
            content=ft.Container(
                width=max_width,
                border_radius=Radius.LG,
                shadow=Shadows.SM,
                bgcolor=Colors.Background.SURFACE,
                padding=Spacing.XL,
                content=body,
            ),
        )