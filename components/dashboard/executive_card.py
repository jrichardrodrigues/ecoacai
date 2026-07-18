import flet as ft

from components.theme import Colors, Typography, Spacing, Radius, Shadows

class ExecutiveCard(ft.Container):
    """Card compacto para indicadores do Dashboard Executivo."""

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
        self.padding = Spacing.LG
        self.border_radius = Radius.XL
        self.bgcolor = cor_fundo

        self.border = ft.Border.all(
            1,
            ft.Colors.with_opacity(0.10, cor),
        )

        self.shadow = Shadows.CARD

        self.on_click = on_click

        self.animate = ft.Animation(
            180,
            ft.AnimationCurve.EASE_OUT,
        )

        conteudo_inferior: list[ft.Control] = [
            ft.Text(
                valor,
                size=Typography.H1,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREY_900,
            ),
        ]

        if subtitulo:
            conteudo_inferior.append(
                ft.Text(
                    subtitulo,
                    size=Typography.LABEL,
                    color=ft.Colors.GREY_700,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
            )

        self.content = ft.Column(
            spacing=Spacing.MD,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            titulo,
                            size=Typography.SMALL,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.GREY_700,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            expand=True,
                        ),
                        ft.Container(
                            width=Spacing.ICON_CONTAINER,
                            height=Spacing.ICON_CONTAINER,
                            border_radius=Radius.LG,
                            bgcolor=ft.Colors.with_opacity(
                                0.14,
                                cor,
                            ),
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                icone,
                                size=Spacing.ICON_SIZE_MD,
                                color=cor,
                            ),
                        ),
                    ],
                ),
                ft.Column(
                    spacing=Spacing.XS,
                    controls=conteudo_inferior,
                ),
            ],
        )