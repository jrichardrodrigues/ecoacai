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
from controllers import LoginController


class LoginView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = LoginController()

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

    def on_entrar(self, e):
        sucesso, resultado = self.controller.entrar(
            self.cpf.value,
            self.senha.value,
        )

        if sucesso:
            print("Login realizado com sucesso!")
            print(resultado)
        else:
            print(resultado)

    def on_criar_conta(self, e):
        print("Botão CRIAR CONTA clicado")

    def on_esqueci_senha(self, e):
        print("Botão ESQUECI MINHA SENHA clicado")

    def build(self):
        card = FormCard(
            content=ft.Column(
                controls=[
                    PageHeader(
                        title="EcoAçaí",
                        subtitle=(
                            "Plataforma Inteligente de Recolhimento\n"
                            "de Caroço de Açaí"
                        ),
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