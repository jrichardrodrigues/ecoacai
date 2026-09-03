from __future__ import annotations

from typing import Any

import flet as ft

from components.buttons import PrimaryButton


class ResponsiveHeader(ft.ResponsiveRow):
    """Cabeçalho responsivo padrão das telas do sistema."""

    def __init__(
            self,
            *,
            title: str,
            subtitle: str | None = None,
            action_label: str | None = None,
            action_icon: Any | None = None,
            on_action=None,
    ) -> None:

        title_controls: list[ft.Control] = [
            ft.Text(
                title,
                size=26,
                weight=ft.FontWeight.BOLD,
            ),
        ]

        if subtitle:
            title_controls.append(
                ft.Text(
                    subtitle,
                    size=14,
                )
            )

        title_block = ft.Column(
            controls=title_controls,
            spacing=3,
        )

        controls: list[ft.Control] = [
            ft.Container(
                content=title_block,
                col={
                    "xs": 12,
                    "sm": 12,
                    "md": 8,
                    "lg": 9,
                },
            ),
        ]

        if action_label:
            action_button = PrimaryButton(
                label=action_label,
                icon=action_icon or ft.Icons.ADD,
                on_click=on_action,
            )

            controls.append(
                ft.Container(
                    content=action_button,
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 3,
                    },
                    alignment=ft.Alignment.CENTER_RIGHT,
                )
            )

        super().__init__(
            controls=controls,
            columns=12,
            spacing=12,
            run_spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )