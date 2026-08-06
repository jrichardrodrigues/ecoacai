from collections.abc import Callable

import flet as ft

from components.fields import CpfField, PasswordField
from components.ui import theme
from components.ui.auth import AuthMode, AuthPanel
from components.ui.branding import HeroPanel
from controllers.auth_controller import AuthController
from models import SessaoUsuario
from utils.messages import mostrar_erro


class LoginView:
    """Tela de autenticação institucional da ZELURBIS."""

    def __init__(
        self,
        page: ft.Page,
        auth_controller: AuthController,
        on_login_sucesso: Callable[[SessaoUsuario], None],
        on_criar_conta: Callable[[ft.ControlEvent], None],
        on_esqueci_senha: Callable[[ft.ControlEvent], None],
    ) -> None:
        self.page = page
        self.controller = auth_controller

        self._on_login_sucesso = on_login_sucesso
        self._on_criar_conta = on_criar_conta
        self._on_esqueci_senha = on_esqueci_senha

        self.page.title = "ZELURBIS"

        self.cpf = CpfField(
            usuario_service=None,
        )

        self.senha = PasswordField(
            label="Senha",
            mostrar_requisitos=False,
        )

        self.lembrar_me = ft.Checkbox(
            label="Lembrar-me",
            value=False,
        )

    def on_entrar(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        sucesso, mensagem = self.controller.entrar(
            self.cpf.value,
            self.senha.value,
        )

        if not sucesso:
            mostrar_erro(
                self.page,
                mensagem,
            )
            return

        sessao = self.controller.obter_sessao()

        if sessao is None:
            mostrar_erro(
                self.page,
                "Não foi possível abrir a sessão.",
            )
            return

        self._on_login_sucesso(sessao)

    def on_criar_conta(
        self,
        evento: ft.ControlEvent,
    ) -> None:
        self._on_criar_conta(evento)

    def on_esqueci_senha(
        self,
        evento: ft.ControlEvent,
    ) -> None:
        self._on_esqueci_senha(evento)

    def _layout_compacto(self) -> bool:
        largura = self.page.width or 1200
        return largura < 900

    def construir(self) -> ft.Control:
        compacto = self._layout_compacto()

        hero_panel = HeroPanel(
            min_height=300 if compacto else 640,
            padding=(
                theme.SPACE_LG
                if compacto
                else theme.SPACE_XL
            ),
        )

        auth_panel = AuthPanel(
            mode=AuthMode.LOGIN,
            fields=[
                self.cpf.container,
                self.senha.container,
            ],
            on_primary=self.on_entrar,
            on_register=self.on_criar_conta,
            on_forgot_password=self.on_esqueci_senha,
            remember_checkbox=self.lembrar_me,
            version="0.9.1",
            width=None if compacto else 520,
            height=560 if compacto else 640,
        )

        if compacto:
            conteudo: ft.Control = ft.Column(
                controls=[
                    hero_panel,
                    auth_panel,
                ],
                spacing=theme.SPACE_MD,
                horizontal_alignment=(
                    ft.CrossAxisAlignment.STRETCH
                ),
            )
        else:
            conteudo = ft.Row(
                controls=[
                    ft.Container(
                        content=hero_panel,
                        expand=5,
                    ),
                    ft.Container(
                        content=auth_panel,
                        expand=6,
                    ),
                ],
                spacing=0,
                vertical_alignment=(
                    ft.CrossAxisAlignment.STRETCH
                ),
            )

        return ft.Container(
            expand=True,
            bgcolor=theme.BACKGROUND,
            alignment=ft.Alignment.CENTER,
            padding=theme.SPACE_LG,
            content=ft.Container(
                width=1120,
                border_radius=theme.RADIUS_XL,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=conteudo,
            ),
        )

    def build(self) -> ft.Control:
        return self.construir()
