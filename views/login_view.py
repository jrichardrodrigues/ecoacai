from collections.abc import Callable

import flet as ft

from components.buttons import (
    LinkButton,
    PrimaryButton,
    SecondaryButton,
)
from components.cards import FormCard
from components.fields import CpfField, PasswordField
from components.headers import PageHeader
from components.theme import Colors
from config import APP_NAME, APP_SUBTITLE
from controllers.auth_controller import AuthController
from models import Usuario
from utils.messages import mostrar_erro


class LoginView:
    """Tela de autenticação da plataforma ECOAÇAÍ."""

    def __init__(
        self,
        page: ft.Page,
        auth_controller: AuthController,
        on_login_sucesso: Callable[[Usuario], None],
        on_criar_conta: Callable[[ft.ControlEvent], None],
        on_esqueci_senha: Callable[[ft.ControlEvent], None],
    ) -> None:
        self.page = page
        self.controller = auth_controller

        self._on_login_sucesso = on_login_sucesso
        self._on_criar_conta = on_criar_conta
        self._on_esqueci_senha = on_esqueci_senha

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

    def on_entrar(self, e: ft.ControlEvent) -> None:
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

        usuario = self.controller.usuario_logado

        if usuario is None:
            mostrar_erro(
                self.page,
                "Não foi possível recuperar o usuário autenticado.",
            )
            return

        self._on_login_sucesso(usuario)

    def on_criar_conta(self, e: ft.ControlEvent) -> None:
        """Encaminha o evento para o fluxo de criação de conta."""

        self._on_criar_conta(e)

    def on_esqueci_senha(self, e: ft.ControlEvent) -> None:
        """Encaminha o evento para o fluxo de recuperação de senha."""

        self._on_esqueci_senha(e)

    def construir(self) -> ft.Control:
        """Constrói e retorna o conteúdo visual da tela de login."""

        card = FormCard(
            content=ft.Column(
                controls=[
                    PageHeader(
                        title=APP_NAME,
                        subtitle=APP_SUBTITLE,
                        icon=ft.Icons.ECO,
                    ),
                    self.cpf.container,
                    self.senha.container,
                    ft.Row(
                        controls=[
                            self.lembrar_me,
                            LinkButton(
                                label="Esqueci minha senha",
                                icon=ft.Icons.KEY_OUTLINED,
                                on_click=self.on_esqueci_senha,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    PrimaryButton(
                        label="ENTRAR",
                        icon=ft.Icons.LOGIN,
                        expand=True,
                        on_click=self.on_entrar,
                    ),
                    ft.Divider(),
                    ft.Text(
                        "Ainda não possui uma conta?",
                        color=Colors.TEXT_SECONDARY,
                    ),
                    SecondaryButton(
                        label="CRIAR CONTA",
                        icon=ft.Icons.PERSON_ADD_OUTLINED,
                        expand=True,
                        on_click=self.on_criar_conta,
                    ),
                ],
                spacing=18,
            ),
            width=460,
        )

        return ft.Container(
            expand=True,
            bgcolor=Colors.BACKGROUND,
            alignment=ft.Alignment.CENTER,
            padding=20,
            content=card,
        )

    def build(self) -> ft.Control:
        """
        Mantém compatibilidade com locais que ainda chamem build().
        """

        return self.construir()