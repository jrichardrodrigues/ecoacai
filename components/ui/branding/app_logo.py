"""
AppLogo
=======

Componente oficial de identidade visual da ZELURBIS.

Pode exibir:

- ícone padrão;
- nome da plataforma;
- slogan;
- logotipo em imagem;
- disposição vertical ou horizontal.

Projeto : ZELURBIS
Versão  : UI 1.0
"""

from __future__ import annotations

import flet as ft

from components.ui import theme


class AppLogo(ft.Container):
    """Exibe a identidade visual da plataforma ZELURBIS."""

    APP_NAME = "ZELURBIS"

    APP_SLOGAN = (
        "Tecnologia a serviço da sustentabilidade."
    )

    def __init__(
        self,
        *,
        size: int = 72,
        show_icon: bool = True,
        show_name: bool = True,
        show_slogan: bool = False,
        horizontal: bool = False,
        logo_path: str | None = None,
        name_color: str = theme.PRIMARY,
        slogan_color: str = theme.TEXT_SECONDARY,
    ) -> None:
        self.logo_size = max(24, int(size))
        self.show_icon = show_icon
        self.show_name = show_name
        self.show_slogan = show_slogan
        self.horizontal = horizontal
        self.logo_path = logo_path
        self.name_color = name_color
        self.slogan_color = slogan_color

        super().__init__(
            content=self._construir(),
        )

    def _criar_marca_visual(self) -> ft.Control | None:
        """Cria a imagem oficial ou o ícone de fallback."""

        if not self.show_icon:
            return None

        if self.logo_path:
            return ft.Image(
                src=self.logo_path,
                width=self.logo_size,
                height=self.logo_size,
                fit=ft.BoxFit.CONTAIN,
            )

        return ft.Container(
            width=self.logo_size,
            height=self.logo_size,
            border_radius=self.logo_size,
            bgcolor=theme.PRIMARY,
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.ECO,
                color=theme.SURFACE,
                size=self.logo_size * 0.55,
            ),
        )

    def _criar_textos(self) -> ft.Control | None:
        """Cria o nome e o slogan da plataforma."""

        controles: list[ft.Control] = []

        if self.show_name:
            controles.append(
                ft.Text(
                    self.APP_NAME,
                    size=max(
                        18,
                        int(self.logo_size * 0.36),
                    ),
                    weight=ft.FontWeight.BOLD,
                    color=self.name_color,
                    text_align=ft.TextAlign.CENTER,
                )
            )

        if self.show_slogan:
            controles.append(
                ft.Text(
                    self.APP_SLOGAN,
                    size=max(
                        12,
                        int(self.logo_size * 0.18),
                    ),
                    color=self.slogan_color,
                    text_align=ft.TextAlign.CENTER,
                )
            )

        if not controles:
            return None

        return ft.Column(
            controls=controles,
            spacing=theme.SPACE_XS,
            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
        )

    def _construir(self) -> ft.Control:
        """Monta o componente conforme a orientação escolhida."""

        marca = self._criar_marca_visual()
        textos = self._criar_textos()

        controles = [
            controle
            for controle in (
                marca,
                textos,
            )
            if controle is not None
        ]

        if self.horizontal:
            return ft.Row(
                controls=controles,
                spacing=theme.SPACE_MD,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
            )

        return ft.Column(
            controls=controles,
            spacing=theme.SPACE_SM,
            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
        )