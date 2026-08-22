from collections.abc import Callable

import flet as ft


class ZelurbisHomeView:
    """Página inicial da Plataforma ZELURBIS."""

    def __init__(
        self,
        page: ft.Page,
        on_acessar_ecoacai: Callable[[], None],
        on_sair: Callable[[], None] | None = None,
    ) -> None:
        self.page = page
        self.on_acessar_ecoacai = on_acessar_ecoacai
        self.on_sair = on_sair

    def _criar_card_modulo(
        self,
        *,
        nome: str,
        descricao: str,
        icone: str,
        disponivel: bool = False,
        on_acessar: Callable[[], None] | None = None,
    ) -> ft.Control:
        """Cria um card de solução da plataforma."""

        if disponivel:
            acao = ft.FilledButton(
                content="ACESSAR",
                icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                on_click=lambda _e: (
                    on_acessar()
                    if on_acessar is not None
                    else None
                ),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN_800,
                    color=ft.Colors.WHITE,
                ),
            )
        else:
            acao = ft.Container(
                padding=ft.Padding.symmetric(
                    horizontal=14,
                    vertical=7,
                ),
                border_radius=20,
                bgcolor=ft.Colors.GREY_200,
                content=ft.Text(
                    "EM BREVE",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_700,
                ),
            )

        return ft.Container(
            padding=24,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=52,
                        height=52,
                        border_radius=14,
                        bgcolor=(
                            ft.Colors.GREEN_50
                            if disponivel
                            else ft.Colors.GREY_100
                        ),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            icone,
                            size=28,
                            color=(
                                ft.Colors.GREEN_800
                                if disponivel
                                else ft.Colors.GREY_600
                            ),
                        ),
                    ),
                    ft.Text(
                        nome,
                        size=21,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                    ft.Text(
                        descricao,
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(expand=True),
                    ft.Row(
                        controls=[acao],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=12,
            ),
        )

    def build(self) -> ft.Control:
        """Constrói a Home principal da ZELURBIS."""

        ecoacai = self._criar_card_modulo(
            nome="ECOAÇAÍ",
            descricao=(
                "Gestão da coleta, transporte e destinação "
                "dos resíduos do açaí."
            ),
            icone=ft.Icons.ECO_OUTLINED,
            disponivel=True,
            on_acessar=self.on_acessar_ecoacai,
        )

        ecooleo = self._criar_card_modulo(
            nome="ECOÓLEO",
            descricao=(
                "Gestão da coleta e destinação "
                "de óleos residuais."
            ),
            icone=ft.Icons.WATER_DROP_OUTLINED,
        )

        ecogarrafas = self._criar_card_modulo(
            nome="ECOGARRAFAS",
            descricao=(
                "Gestão da coleta e logística "
                "de garrafas e embalagens de vidro."
            ),
            icone=ft.Icons.RECYCLING_ROUNDED,
        )

        cabecalho = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "ZELURBIS",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_900,
                        ),
                        ft.Text(
                            "Tecnologia a serviço da sustentabilidade.",
                            size=13,
                            color=ft.Colors.GREY_700,
                        ),
                    ],
                    spacing=2,
                ),
                ft.Container(expand=True),
                *(
                    [
                        ft.TextButton(
                            content="Sair",
                            icon=ft.Icons.LOGOUT_ROUNDED,
                            on_click=lambda _e: self.on_sair(),
                        )
                    ]
                    if self.on_sair is not None
                    else []
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_50,
            padding=40,
            content=ft.Column(
                controls=[
                    cabecalho,
                    ft.Divider(
                        height=1,
                        color=ft.Colors.GREY_300,
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Bem-vindo à ZELURBIS",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                    ft.Text(
                        "Plataforma Inteligente de Gestão Ambiental Urbana",
                        size=18,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "Selecione uma solução para acessar:",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_800,
                    ),
                    ft.Container(height=8),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=ecoacai,
                                height=260,
                                col={
                                    "sm": 12,
                                    "md": 6,
                                    "lg": 4,
                                },
                            ),
                            ft.Container(
                                content=ecooleo,
                                height=260,
                                col={
                                    "sm": 12,
                                    "md": 6,
                                    "lg": 4,
                                },
                            ),
                            ft.Container(
                                content=ecogarrafas,
                                height=260,
                                col={
                                    "sm": 12,
                                    "md": 6,
                                    "lg": 4,
                                },
                            ),
                        ],
                        spacing=18,
                        run_spacing=18,
                    ),
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
            ),
        )
