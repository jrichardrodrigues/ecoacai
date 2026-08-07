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

    Mantém identidade visual, espaçamentos e comportamento
    consistente entre as telas da aplicação.

    Em janelas menores, a página permite rolagem vertical
    automática sem comprimir o conteúdo.
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

        # O card cresce naturalmente conforme o conteúdo.
        card = ft.Container(
            width=max_width,
            border_radius=Radius.LG,
            shadow=Shadows.CARD,
            bgcolor=Colors.Background.SURFACE,
            padding=Spacing.XL,
            content=ft.Column(
                controls=body_controls,
                spacing=Spacing.LG,
            ),
        )

        # A rolagem pertence à página, e não ao conteúdo interno do card.
        page_content = ft.Column(
            controls=[
                ft.Row(
                    controls=[card],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            scroll=scroll,
            expand=True,
        )

        super().__init__(
            expand=expand,
            bgcolor=bgcolor or Colors.Background.DEFAULT,
            padding=Spacing.PAGE_PADDING,
            content=page_content,
        )