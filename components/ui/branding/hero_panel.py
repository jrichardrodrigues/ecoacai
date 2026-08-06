"""
HeroPanel
=========

Painel institucional reutilizável da identidade visual ZELURBIS.

Projeto: ZELURBIS
Versão: UI 1.0
"""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.ui import theme
from components.ui.branding.app_logo import AppLogo


class HeroPanel(ft.Container):
    """Exibe o painel institucional da ZELURBIS."""

    DESTAQUES_PADRAO = (
        "Gestão inteligente de coletas",
        "Diversos tipos de resíduos",
        "Acompanhamento das solicitações",
        "Indicadores operacionais",
        "Integração entre parceiros e poder público",
    )

    def __init__(
        self,
        *,
        title: str = "Tecnologia a serviço da sustentabilidade.",
        description: str = (
            "A ZELURBIS conecta geradores, transportadores, "
            "beneficiadores e gestores públicos em uma única "
            "plataforma para tornar a gestão de resíduos mais "
            "eficiente, transparente e sustentável."
        ),
        highlights: Sequence[str] | None = None,
        image_path: str | None = None,
        width: int | float | None = None,
        min_height: int | float = 640,
        padding: int | float = theme.SPACE_XL,
        bgcolor: str = theme.SECONDARY,
    ) -> None:
        self.title = str(title or "").strip()
        self.description = str(description or "").strip()
        self.highlights = tuple(
            str(item).strip()
            for item in (
                highlights
                if highlights is not None
                else self.DESTAQUES_PADRAO
            )
            if str(item or "").strip()
        )
        self.image_path = image_path

        super().__init__(
            width=width,
            height=min_height,
            padding=padding,
            bgcolor=bgcolor,
            border_radius=theme.RADIUS_XL,
            content=self._construir(),
        )

    def _criar_destaque(self, texto: str) -> ft.Control:
        return ft.Row(
            controls=[
                ft.Container(
                    width=30,
                    height=30,
                    border_radius=15,
                    bgcolor="#FFFFFF22",
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.CHECK_ROUNDED,
                        size=18,
                        color=theme.SURFACE,
                    ),
                ),
                ft.Text(
                    texto,
                    size=theme.BODY,
                    color=theme.SURFACE,
                    weight=ft.FontWeight.W_500,
                    expand=True,
                ),
            ],
            spacing=theme.SPACE_SM,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _criar_imagem(self) -> ft.Control | None:
        if not self.image_path:
            return None

        return ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src=self.image_path,
                height=210,
                fit=ft.BoxFit.CONTAIN,
            ),
        )

    def _criar_atores(self) -> ft.Control:
        atores = (
            ("Geradores", ft.Icons.STORE_OUTLINED),
            ("Transportadores", ft.Icons.LOCAL_SHIPPING_OUTLINED),
            ("Beneficiadores", ft.Icons.FACTORY_OUTLINED),
            ("Poder Público", ft.Icons.ACCOUNT_BALANCE_OUTLINED),
        )

        controles = []

        for nome, icone in atores:
            controles.append(
                ft.Container(
                    padding=ft.Padding.symmetric(
                        horizontal=theme.SPACE_SM,
                        vertical=theme.SPACE_XS,
                    ),
                    border_radius=theme.RADIUS_MD,
                    bgcolor="#FFFFFF18",
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                icone,
                                size=18,
                                color=theme.SURFACE,
                            ),
                            ft.Text(
                                nome,
                                size=theme.CAPTION,
                                color=theme.SURFACE,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        spacing=theme.SPACE_XS,
                        tight=True,
                    ),
                )
            )

        return ft.Row(
            controls=controles,
            spacing=theme.SPACE_SM,
            run_spacing=theme.SPACE_SM,
            wrap=True,
        )

    def _construir(self) -> ft.Control:
        controles = [
            AppLogo(
                size=64,
                show_name=True,
                show_slogan=False,
                horizontal=True,
                name_color=theme.SURFACE,
            ),
            ft.Container(height=theme.SPACE_SM),
            ft.Text(
                self.title,
                size=theme.TITLE,
                weight=ft.FontWeight.BOLD,
                color=theme.SURFACE,
            ),
            ft.Text(
                self.description,
                size=theme.BODY,
                color="#FFFFFFDD",
            ),
            self._criar_atores(),
            ft.Divider(
                color="#FFFFFF33",
                height=theme.SPACE_LG,
            ),
            ft.Text(
                "O que a ZELURBIS oferece",
                size=theme.SUBTITLE,
                weight=ft.FontWeight.BOLD,
                color=theme.SURFACE,
            ),
        ]

        controles.extend(
            self._criar_destaque(item)
            for item in self.highlights
        )

        imagem = self._criar_imagem()

        if imagem is not None:
            controles.append(imagem)

        controles.extend(
            [
                ft.Container(expand=True),
                ft.Text(
                    "Mais que um software. Uma plataforma para "
                    "conectar pessoas, empresas e cidades.",
                    size=theme.CAPTION,
                    color="#FFFFFFBB",
                    italic=True,
                ),
            ]
        )

        return ft.Column(
            controls=controles,
            spacing=theme.SPACE_MD,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
