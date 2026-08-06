"""
RecuperarSenhaView
==================

Tela de recuperação de senha da ZELURBIS.
"""

from collections.abc import Callable

import flet as ft

from components.fields import CpfField, PasswordField
from components.ui import theme
from components.ui.branding import HeroPanel
from controllers.auth_controller import AuthController
from utils.messages import mostrar_erro, mostrar_sucesso


class RecuperarSenhaView:

    def __init__(self, page: ft.Page, auth_controller: AuthController,
                 on_voltar: Callable[[ft.ControlEvent], None]) -> None:
        self.page = page
        self.controller = auth_controller
        self._on_voltar = on_voltar

        self.cpf = CpfField(usuario_service=None)
        self.nova_senha = PasswordField(label='Nova senha', mostrar_requisitos=True)
        self.confirmar_senha = PasswordField(label='Confirmar senha', mostrar_requisitos=False)

    def alterar_senha(self, e: ft.ControlEvent) -> None:
        if self.nova_senha.value != self.confirmar_senha.value:
            mostrar_erro(self.page, 'As senhas não conferem.')
            return

        ok, mensagem = self.controller.alterar_senha_por_cpf(
            cpf=self.cpf.value,
            nova_senha=self.nova_senha.value,
        )

        if not ok:
            mostrar_erro(self.page, mensagem)
            return

        mostrar_sucesso(self.page, mensagem)
        self._on_voltar(e)

    def build(self) -> ft.Control:
        formulario = ft.Container(
            width=520,
            bgcolor=theme.SURFACE,
            border_radius=theme.RADIUS_XL,
            padding=theme.SPACE_XL,
            content=ft.Column(
                spacing=theme.SPACE_MD,
                controls=[
                    ft.Text('Recuperar senha', size=theme.TITLE,
                            weight=ft.FontWeight.BOLD),
                    self.cpf.container,
                    self.nova_senha.container,
                    self.confirmar_senha.container,
                    ft.FilledButton(
                        'ALTERAR SENHA',
                        icon=ft.Icons.LOCK_RESET,
                        on_click=self.alterar_senha,
                    ),
                    ft.TextButton(
                        '← Voltar ao login',
                        on_click=self._on_voltar,
                    ),
                ],
            ),
        )

        return ft.Container(
            expand=True,
            bgcolor=theme.BACKGROUND,
            padding=theme.SPACE_LG,
            content=ft.Row(
                controls=[
                    ft.Container(HeroPanel(min_height=640), expand=5),
                    ft.Container(formulario, expand=6,
                                 alignment=ft.Alignment.CENTER),
                ],
            ),
        )
