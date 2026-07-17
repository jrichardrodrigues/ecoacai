import flet as ft


class ExecutiveCard(ft.Container):
    """Card compacto para indicadores do Dashboard Executivo."""

    def __init__(
        self,
        titulo: str,
        valor: str,
        icone: str = ft.Icons.ANALYTICS,
        cor: str = ft.Colors.BLUE_700,
        cor_fundo: str = ft.Colors.BLUE_50,
        subtitulo: str = "",
        on_click=None,
    ) -> None:
        super().__init__()

        self.expand = True
        self.padding = 16
        self.border_radius = 16
        self.bgcolor = cor_fundo
        self.border = ft.Border.all(
            1,
            ft.Colors.with_opacity(0.10, cor),
        )
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(
                0.12,
                ft.Colors.BLACK,
            ),
            offset=ft.Offset(0, 2),
        )
        self.on_click = on_click
        self.animate = ft.Animation(
            180,
            ft.AnimationCurve.EASE_OUT,
        )

        conteudo_inferior: list[ft.Control] = [
            ft.Text(
                valor,
                size=30,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREY_900,
            ),
        ]

        if subtitulo:
            conteudo_inferior.append(
                ft.Text(
                    subtitulo,
                    size=11,
                    color=ft.Colors.GREY_700,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
            )

        self.content = ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            titulo,
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.GREY_700,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            expand=True,
                        ),
                        ft.Container(
                            width=44,
                            height=44,
                            border_radius=14,
                            bgcolor=ft.Colors.with_opacity(
                                0.14,
                                cor,
                            ),
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                icone,
                                size=25,
                                color=cor,
                            ),
                        ),
                    ],
                ),
                ft.Column(
                    spacing=2,
                    controls=conteudo_inferior,
                ),
            ],
        )