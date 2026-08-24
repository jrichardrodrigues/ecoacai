from collections.abc import Callable

import flet as ft

from models import SessaoUsuario

from config.constants import (
    VERDE_SIDEBAR,
    VERDE_SIDEBAR_ATIVO,
    VERDE_DESTAQUE,
    COR_ECOACAI,
    COR_ECOOLEO,
    COR_ECOGARRAFAS,
)

class ZelurbisHomeView:
    """Página inicial da Plataforma ZELURBIS."""

    def __init__(
            self,
            page: ft.Page,
            on_acessar_ecoacai: Callable[[], None],
            on_sair: Callable[[], None] | None = None,
            sessao: SessaoUsuario | None = None,
    ) -> None:
        self.page = page
        self.on_acessar_ecoacai = on_acessar_ecoacai
        self.on_sair = on_sair
        self.sessao = sessao

    def _criar_item_sidebar(
            self,
            *,
            icone: str,
            titulo: str,
            selecionado: bool = False,
    ) -> ft.Control:
        """Cria um item visual da navegação lateral."""

        nome_usuario = "Gestor"
        nome_perfil = "Perfil do usuário"

        if self.sessao is not None:
            nome_usuario = (
                    self.sessao.usuario.nome.strip()
                    or "Usuário"
            )

            nome_perfil = (
                    self.sessao.perfil.nome.strip()
                    or self.sessao.perfil.codigo.replace(
                "_",
                " ",
            ).title()
            )

        return ft.Container(
            height=52,
            padding=ft.Padding.symmetric(
                horizontal=16,
                vertical=8,
            ),
            border_radius=12,
            bgcolor=(
                VERDE_SIDEBAR_ATIVO
                if selecionado
                else None
            ),
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icone,
                        size=22,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        titulo,
                        size=14,
                        weight=(
                            ft.FontWeight.W_600
                            if selecionado
                            else ft.FontWeight.W_400
                        ),
                        color=ft.Colors.WHITE,
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _criar_sidebar(self) -> ft.Control:
        """Cria a navegação institucional da ZELURBIS."""

        nome_usuario = "Gestor"
        nome_perfil = "Perfil do usuário"

        if self.sessao is not None:
            nome_usuario = (
                    self.sessao.usuario.nome.strip()
                    or "Usuário"
            )

            nome_perfil = (
                    self.sessao.perfil.nome.strip()
                    or self.sessao.perfil.codigo.replace(
                "_",
                " ",
            ).title()
            )

        return ft.Container(
            width=260,
            bgcolor=VERDE_SIDEBAR,
            padding=ft.Padding.only(
                left=22,
                right=22,
                top=30,
                bottom=22,
            ),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.ECO_ROUNDED,
                                size=42,
                                color=VERDE_DESTAQUE,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "ZELURBIS",
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Text(
                                        "Gestão Ambiental Urbana",
                                        size=11,
                                        color=ft.Colors.WHITE70,
                                    ),
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.Container(height=32),

                    self._criar_item_sidebar(
                        icone=ft.Icons.HOME_ROUNDED,
                        titulo="Página inicial",
                        selecionado=True,
                    ),

                    self._criar_item_sidebar(
                        icone=ft.Icons.ECO_OUTLINED,
                        titulo="Módulos",
                    ),

                    self._criar_item_sidebar(
                        icone=ft.Icons.INFO_OUTLINE_ROUNDED,
                        titulo="Sobre a plataforma",
                    ),

                    ft.Container(expand=True),

                    ft.Container(
                        width=float("inf"),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Column(
                            controls=[
                                ft.Icon(
                                    ft.Icons.ECO_ROUNDED,
                                    size=38,
                                    color=VERDE_DESTAQUE,
                                ),
                                ft.Text(
                                    "Tecnologia a serviço\nda sustentabilidade.",
                                    size=12,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            spacing=8,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),

                    ft.Container(height=28),

                    ft.Container(
                        padding=14,
                        border_radius=12,
                        bgcolor=VERDE_SIDEBAR_ATIVO,
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(
                                        ft.Icons.PERSON_ROUNDED,
                                        size=25,
                                        color=VERDE_SIDEBAR,
                                    ),
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            nome_usuario,
                                            size=13,
                                            weight=ft.FontWeight.W_600,
                                            color=ft.Colors.WHITE,
                                        ),
                                        ft.Text(
                                            nome_perfil,
                                            size=11,
                                            color=ft.Colors.WHITE70,
                                        ),
                                    ],
                                    spacing=1,
                                    expand=True,
                                ),
                                ft.PopupMenuButton(
                                    icon=ft.Icons.EXPAND_MORE_ROUNDED,
                                    icon_color=ft.Colors.WHITE70,
                                    items=[
                                        ft.PopupMenuItem(
                                            content="Meu perfil",
                                            icon=ft.Icons.PERSON_OUTLINE_ROUNDED,
                                            on_click=lambda _e: None,
                                        ),
                                        ft.PopupMenuItem(
                                            content="Sair",
                                            icon=ft.Icons.LOGOUT_ROUNDED,
                                            on_click=lambda _e: (
                                                self.on_sair()
                                                if self.on_sair is not None
                                                else None
                                            ),
                                        ),
                                    ],
                                )
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                ],
                spacing=6,
            ),
        )

    def _criar_card_modulo(
            self,
            *,
            nome: str,
            descricao: str,
            icone: str,
            cor_modulo: str,
            disponivel: bool = False,
            on_acessar: Callable[[], None] | None = None,
    ) -> ft.Control:
        """Cria um card de solução da plataforma."""

        cor_suave = ft.Colors.with_opacity(
            0.10,
            cor_modulo,
        )

        cor_borda = ft.Colors.with_opacity(
            0.35,
            cor_modulo,
        )

        if disponivel:
            status = ft.Container(
                padding=ft.Padding.symmetric(
                    horizontal=10,
                    vertical=5,
                ),
                border_radius=20,
                bgcolor=cor_suave,
                content=ft.Text(
                    "MÓDULO ATIVO",
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color=cor_modulo,
                ),
            )

            acao = ft.FilledButton(
                content="ACESSAR",
                icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                on_click=lambda _e: (
                    on_acessar()
                    if on_acessar is not None
                    else None
                ),
                style=ft.ButtonStyle(
                    bgcolor=cor_modulo,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(
                        radius=20,
                    ),
                    padding=ft.Padding.symmetric(
                        horizontal=18,
                        vertical=10,
                    ),
                ),
            )


        else:
            status = ft.Container(
                padding=ft.Padding.symmetric(
                    horizontal=10,
                    vertical=5,
                ),
                border_radius=20,
                bgcolor=cor_suave,
                content=ft.Text(
                    "EM BREVE",
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color=cor_modulo,
                ),
            )

            acao = ft.Text(
                "Em desenvolvimento",
                size=12,
                italic=True,
                weight=ft.FontWeight.W_500,
                color=cor_modulo,
            )

        return ft.Container(
            padding=22,
            border=ft.Border.all(
                1,
                cor_borda,
            ),
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=48,
                                height=48,
                                border_radius=13,
                                bgcolor=cor_suave,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(
                                    icone,
                                    size=26,
                                    color=cor_modulo,
                                ),
                            ),
                            ft.Container(expand=True),
                            status,
                        ],
                    ),

                    ft.Text(
                        nome,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=cor_modulo,
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

    def _criar_conteudo_principal(self) -> ft.Control:
        """Cria a área principal da Home."""

        ecoacai = self._criar_card_modulo(
            nome="ECOAÇAÍ",
            descricao=(
                "Gestão da coleta, transporte e destinação "
                "dos resíduos do açaí."
            ),
            icone=ft.Icons.ECO_OUTLINED,
            cor_modulo=COR_ECOACAI,
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
            cor_modulo=COR_ECOOLEO,
        )

        ecogarrafas = self._criar_card_modulo(
            nome="ECOGARRAFAS",
            descricao=(
                "Gestão da coleta e logística "
                "de garrafas e embalagens de vidro."
            ),
            icone=ft.Icons.RECYCLING_ROUNDED,
            cor_modulo=COR_ECOGARRAFAS,
        )

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_50,
            padding=ft.Padding.only(
                left=38,
                right=38,
                top=30,
                bottom=30,
            ),
            content=ft.Column(
                controls=[
                    # -------------------------------------------------
                    # HERO INSTITUCIONAL
                    # -------------------------------------------------
                    ft.Container(
                        width=float("inf"),
                        height=345,
                        border_radius=18,
                        bgcolor="#F3F8EC",
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        image=ft.DecorationImage(
                            src="assets/images/zelurbis/planeta_conectado.png",
                            fit=ft.BoxFit.COVER,
                            alignment=ft.Alignment.CENTER_RIGHT,
                        ),
                        padding=ft.Padding.only(
                            left=30,
                            right=30,
                            top=26,
                            bottom=22,
                        ),
                        content=ft.Container(
                            width=720,
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "ZELURBIS",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        color=VERDE_DESTAQUE,
                                    ),

                                    ft.Text(
                                        "Uma plataforma.\n"
                                        "Múltiplas soluções.\n"
                                        "Um futuro sustentável.",
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color=VERDE_SIDEBAR,
                                    ),

                                    ft.Text(
                                        "A ZELURBIS integra tecnologia, "
                                        "gestão e pessoas para transformar "
                                        "a maneira como os resíduos são "
                                        "gerenciados nas cidades.",
                                        size=15,
                                        color=ft.Colors.GREY_700,
                                        width=560,
                                    ),

                                    ft.Container(expand=True),

                                    # ---------------------------------
                                    # PILARES DA PLATAFORMA
                                    # ---------------------------------
                                    ft.Row(
                                        controls=[
                                            # Sustentável
                                            ft.Row(
                                                controls=[
                                                    ft.Container(
                                                        width=42,
                                                        height=42,
                                                        border_radius=21,
                                                        bgcolor=VERDE_DESTAQUE,
                                                        alignment=ft.Alignment.CENTER,
                                                        content=ft.Icon(
                                                            ft.Icons.ECO_ROUNDED,
                                                            size=23,
                                                            color=ft.Colors.WHITE,
                                                        ),
                                                    ),
                                                    ft.Column(
                                                        controls=[
                                                            ft.Text(
                                                                "Sustentável",
                                                                size=13,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=VERDE_SIDEBAR,
                                                            ),
                                                            ft.Text(
                                                                "Impacto positivo\n"
                                                                "no meio ambiente",
                                                                size=11,
                                                                color=ft.Colors.GREY_700,
                                                            ),
                                                        ],
                                                        spacing=1,
                                                    ),
                                                ],
                                                spacing=10,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),

                                            # Inteligente
                                            ft.Row(
                                                controls=[
                                                    ft.Container(
                                                        width=42,
                                                        height=42,
                                                        border_radius=21,
                                                        bgcolor=ft.Colors.GREEN_700,
                                                        alignment=ft.Alignment.CENTER,
                                                        content=ft.Icon(
                                                            ft.Icons.INSIGHTS_ROUNDED,
                                                            size=23,
                                                            color=ft.Colors.WHITE,
                                                        ),
                                                    ),
                                                    ft.Column(
                                                        controls=[
                                                            ft.Text(
                                                                "Inteligente",
                                                                size=13,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=VERDE_SIDEBAR,
                                                            ),
                                                            ft.Text(
                                                                "Dados e tecnologia\n"
                                                                "para decisões melhores",
                                                                size=11,
                                                                color=ft.Colors.GREY_700,
                                                            ),
                                                        ],
                                                        spacing=1,
                                                    ),
                                                ],
                                                spacing=10,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),

                                            # Integrada
                                            ft.Row(
                                                controls=[
                                                    ft.Container(
                                                        width=42,
                                                        height=42,
                                                        border_radius=21,
                                                        bgcolor=ft.Colors.GREEN_800,
                                                        alignment=ft.Alignment.CENTER,
                                                        content=ft.Icon(
                                                            ft.Icons.GROUPS_ROUNDED,
                                                            size=23,
                                                            color=ft.Colors.WHITE,
                                                        ),
                                                    ),
                                                    ft.Column(
                                                        controls=[
                                                            ft.Text(
                                                                "Integrada",
                                                                size=13,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=VERDE_SIDEBAR,
                                                            ),
                                                            ft.Text(
                                                                "Conexão entre todos\n"
                                                                "os agentes da cadeia",
                                                                size=11,
                                                                color=ft.Colors.GREY_800,
                                                            ),
                                                        ],
                                                        spacing=1,
                                                    ),
                                                ],
                                                spacing=10,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ],
                                        spacing=28,
                                        wrap=False,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=8,
                                horizontal_alignment=(
                                    ft.CrossAxisAlignment.START
                                ),
                            ),
                        ),
                    ),

                    ft.Container(height=16),

                    # -------------------------------------------------
                    # SOLUÇÕES
                    # -------------------------------------------------
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Soluções",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_900,
                            ),
                            ft.Container(expand=True),
                            ft.Text(
                                "Explore os módulos da plataforma",
                                size=13,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=ecoacai,
                                height=245,
                                col={
                                    "sm": 12,
                                    "md": 6,
                                    "lg": 4,
                                },
                            ),
                            ft.Container(
                                content=ecooleo,
                                height=245,
                                col={
                                    "sm": 12,
                                    "md": 6,
                                    "lg": 4,
                                },
                            ),
                            ft.Container(
                                content=ecogarrafas,
                                height=245,
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
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

    def build(self) -> ft.Control:
        """Constrói a Home principal da ZELURBIS."""

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_50,
            content=ft.Row(
                controls=[
                    self._criar_sidebar(),
                    self._criar_conteudo_principal(),
                ],
                spacing=0,
                expand=True,
            ),
        )