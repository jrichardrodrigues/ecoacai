from collections.abc import Callable

import flet as ft

from components.buttons import LinkButton, PrimaryButton, SecondaryButton
from components.cards import FormCard
from components.fields import CpfField, PasswordField
from components.headers import PageHeader
from components.theme import Colors
from controllers.auth_controller import AuthController
from models import SessaoUsuario
from utils.messages import mostrar_erro


class LoginView:
    """Tela de autenticação da plataforma."""

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

        self.cpf = CpfField(
            usuario_service=None,
        )

        self.senha = PasswordField(
            label="Senha",
            mostrar_requisitos=False,
        )

        self.lembrar_me = ft.Checkbox(label="Lembrar-me", value=False)

    def on_entrar(self, e):
        sucesso, mensagem = self.controller.entrar(
            self.cpf.value,
            self.senha.value,
        )
        if not sucesso:
            mostrar_erro(self.page, mensagem)
            return
        sessao = self.controller.obter_sessao()
        if sessao is None:
            mostrar_erro(self.page, "Não foi possível abrir a sessão.")
            return
        self._on_login_sucesso(sessao)

    def on_criar_conta(self, e):
        self._on_criar_conta(e)

    def on_esqueci_senha(self, e):
        self._on_esqueci_senha(e)

    def construir(self):
        card = FormCard(
            width=500,
            content=ft.Column(
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    PageHeader(
                        title="ZELURBIS",
                        subtitle="Tecnologia a serviço da sustentabilidade",
                        icon=ft.Icons.ECO,
                    ),
                    ft.Text(
                        "Conectando geradores, transportadores e gestores para uma cidade mais limpa.",
                        size=14,
                        color=Colors.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    self.cpf.container,
                    self.senha.container,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.lembrar_me,
                            LinkButton(
                                label="Esqueci minha senha",
                                icon=ft.Icons.KEY_OUTLINED,
                                on_click=self.on_esqueci_senha,
                            ),
                        ],
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
                    ft.Divider(),
                    ft.Text(
                        "Versão 0.9.0 • ZELURBIS",
                        size=11,
                        color=Colors.TEXT_SECONDARY,
                    ),
                ],
            ),
        )

        return ft.Container(
            expand=True,
            bgcolor=Colors.BACKGROUND,
            alignment=ft.Alignment.CENTER,
            padding=20,
            content=card,
        )

    def build(self):
        return self.construir()
