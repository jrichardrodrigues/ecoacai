from collections.abc import Callable

import flet as ft

from components.fields import CpfField, PasswordField
from components.ui import theme
from components.ui.branding import HeroPanel
from components.ui.login import LoginPanel
from controllers.auth_controller import AuthController
from models import SessaoUsuario
from utils.messages import mostrar_erro
from services.remember_me_service import RememberMeService

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

        cpf_lembrado = RememberMeService.carregar_cpf()

        if cpf_lembrado:
            self.cpf.value = cpf_lembrado

        self.lembrar_me = ft.Checkbox(
            label="Lembrar-me",
            value=bool(cpf_lembrado),
        )

        self.lembrar_me = ft.Checkbox(
            label="Lembrar-me",
            value=False,
        )

    # ==========================================================
    # AUTENTICAÇÃO
    # ==========================================================

    def on_entrar(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        """Tenta autenticar o usuário com CPF e senha."""

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

        if self.lembrar_me.value:
            RememberMeService.salvar_cpf(
                self.cpf.value,
            )
        else:
            RememberMeService.limpar()

        self._on_login_sucesso(sessao)

    def on_criar_conta(
        self,
        evento: ft.ControlEvent,
    ) -> None:
        """Encaminha para o fluxo de criação de conta."""

        self._on_criar_conta(evento)

    def on_esqueci_senha(
        self,
        evento: ft.ControlEvent,
    ) -> None:
        """Encaminha para o fluxo de recuperação de senha."""

        self._on_esqueci_senha(evento)

    # ==========================================================
    # LAYOUT
    # ==========================================================

    def _layout_compacto(self) -> bool:
        """Informa se a largura atual exige o layout compacto."""

        largura = self.page.width or 1200
        return largura < 900

    def _criar_hero_panel(
        self,
        *,
        compacto: bool,
    ) -> HeroPanel:
        """Cria o painel institucional da tela."""

        return HeroPanel(
            min_height=300 if compacto else 640,
            padding=(
                theme.SPACE_LG
                if compacto
                else theme.SPACE_XL
            ),
        )

    def _criar_login_panel(
        self,
        *,
        compacto: bool,
    ) -> LoginPanel:
        """Cria o painel de autenticação."""

        return LoginPanel(
            cpf_field=self.cpf,
            password_field=self.senha,
            remember_checkbox=self.lembrar_me,
            on_login=self.on_entrar,
            on_register=self.on_criar_conta,
            on_forgot_password=self.on_esqueci_senha,
            version="0.9.1",
            width=None if compacto else 520,
            min_height=560 if compacto else 640,
        )

    def construir(self) -> ft.Control:
        """Constrói a nova tela institucional de login."""

        compacto = self._layout_compacto()

        hero_panel = self._criar_hero_panel(
            compacto=compacto,
        )

        login_panel = self._criar_login_panel(
            compacto=compacto,
        )

        if compacto:
            conteudo: ft.Control = ft.Column(
                controls=[
                    hero_panel,
                    login_panel,
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
                        content=login_panel,
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
        """Mantém compatibilidade com o padrão das Views."""

        return self.construir()
