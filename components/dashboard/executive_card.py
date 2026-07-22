import flet as ft

from components.theme import (
    Colors,
    Typography,
    Spacing,
    Radius,
    Shadows,
)


class ExecutiveCard(ft.Container):
    """Card executivo moderno para indicadores do Dashboard."""

    def __init__(
        self,
        titulo: str,
        valor: str,
        icone: str = ft.Icons.ANALYTICS,
        cor: str = Colors.Dashboard.REQUESTS,
        cor_fundo: str = Colors.Dashboard.REQUESTS_BG,
        subtitulo: str = "",
        on_click=None,
    ) -> None:
        super().__init__()

        self.expand = True
        self.height = 170

        self.padding = ft.Padding(
            left=18,
            top=16,
            right=18,
            bottom=16,
        )

        self.bgcolor = cor_fundo
        self.border_radius = Radius.XL
        self.shadow = Shadows.CARD

        self.border = ft.Border.all(
            1,
            ft.Colors.with_opacity(0.10, cor),
        )

        self.animate = ft.Animation(
            180,
            ft.AnimationCurve.EASE_OUT,
        )

        self.on_click = on_click

        self.content = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Container(
                    width=54,
                    height=54,
                    border_radius=27,
                    bgcolor=ft.Colors.with_opacity(
                        0.12,
                        cor,
                    ),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        icone,
                        size=27,
                        color=cor,
                    ),
                ),
                ft.Text(
                    valor,
                    size=34,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    titulo,
                    size=Typography.BODY,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    subtitulo,
                    size=Typography.SMALL,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
            ],
        )