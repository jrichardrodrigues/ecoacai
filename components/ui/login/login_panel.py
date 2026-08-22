"""
LoginPanel
==========

Componente reutilizável do formulário de autenticação da ZELURBIS.

Projeto: ZELURBIS
Versão: UI 1.0
"""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.fields import CpfField, PasswordField
from components.ui import theme


class LoginPanel(ft.Container):
    """Exibe o formulário visual de autenticação."""

    def __init__(
        self,
        *,
        cpf_field: CpfField,
        password_field: PasswordField,
        remember_checkbox: ft.Checkbox,
        on_login: Callable[[ft.ControlEvent], None],
        on_register: Callable[[ft.ControlEvent], None],
        on_forgot_password: Callable[[ft.ControlEvent], None],
        version: str = "0.9.1",
        width: int | float | None = 520,
        min_height: int | float = 640,
    ) -> None:
        self.cpf_field = cpf_field
        self.password_field = password_field
        self.remember_checkbox = remember_checkbox

        self.on_login = on_login
        self.on_register = on_register
        self.on_forgot_password = on_forgot_password

        self.version = str(version or "").strip()

        super().__init__(
            width=width,
            height=min_height,
            padding=theme.SPACE_XL,
            bgcolor=theme.SURFACE,
            border_radius=theme.RADIUS_XL,
            content=self._construir(),
        )

    def _criar_botao_entrar(self) -> ft.Control:
        """Cria o botão principal de autenticação."""

        return ft.FilledButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Icon(
                        ft.Icons.LOGIN_ROUNDED,
                        size=22,
                    ),
                    ft.Text(
                        "ENTRAR",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
            on_click=self.on_login,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=theme.PRIMARY,
                color=theme.SURFACE,
                shape=ft.RoundedRectangleBorder(
                    radius=theme.RADIUS_MD,
                ),
                padding=ft.Padding.symmetric(
                    horizontal=theme.SPACE_LG,
                    vertical=0,
                ),
            ),
        )

    def _criar_botao_criar_conta(self) -> ft.Control:
        """Cria o botão secundário de cadastro."""

        return ft.OutlinedButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Icon(
                        ft.Icons.PERSON_ADD_OUTLINED,
                        size=22,
                    ),
                    ft.Text(
                        "CRIAR CONTA",
                        size=16,
                        weight=ft.FontWeight.W_600,
                    ),
                ],
            ),
            on_click=self.on_register,
            height=58,
            style=ft.ButtonStyle(
                color=theme.PRIMARY,
                side=ft.BorderSide(
                    width=1,
                    color=theme.PRIMARY,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=theme.RADIUS_MD,
                ),
                padding=ft.Padding.symmetric(
                    horizontal=theme.SPACE_LG,
                    vertical=0,
                ),
            ),
        )

    def _criar_link_esqueci_senha(self) -> ft.Control:
        """Cria o link de recuperação de senha."""

        return ft.TextButton(
            content="Esqueci minha senha",
            icon=ft.Icons.KEY_OUTLINED,
            on_click=self.on_forgot_password,
            style=ft.ButtonStyle(
                color=theme.PRIMARY,
                padding=0,
            ),
        )

    def _criar_rodape(self) -> ft.Control:
        """Cria o rodapé institucional do formulário."""

        versao = (
            f"Versão {self.version} • ZELURBIS"
            if self.version
            else "ZELURBIS"
        )

        return ft.Column(
            controls=[
                ft.Text(
                    "Acesso protegido e seguro",
                    size=theme.CAPTION,
                    color=theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    versao,
                    size=theme.CAPTION,
                    color=theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=theme.SPACE_XS,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _construir(self) -> ft.Control:
        """Monta o formulário completo."""

        return ft.Column(
            controls=[
                ft.Container(height=theme.SPACE_SM),
                ft.Text(
                    "Bem-vindo à ZELURBIS",
                    size=theme.TITLE,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXT_PRIMARY,
                ),
                ft.Text(
                    "Acesse sua conta para continuar.",
                    size=theme.BODY,
                    color=theme.TEXT_SECONDARY,
                ),
                ft.Container(height=theme.SPACE_SM),
                self.cpf_field.container,
                self.password_field.container,
                ft.Row(
                    controls=[
                        self.remember_checkbox,
                        ft.Container(expand=True),
                        self._criar_link_esqueci_senha(),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=self._criar_botao_entrar(),
                            expand=True,
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Divider(
                            color=theme.BORDER,
                            expand=True,
                        ),
                        ft.Text(
                            "ou",
                            size=theme.CAPTION,
                            color=theme.TEXT_SECONDARY,
                        ),
                        ft.Divider(
                            color=theme.BORDER,
                            expand=True,
                        ),
                    ],
                    spacing=theme.SPACE_SM,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(
                    "Ainda não possui uma conta?",
                    size=theme.BODY,
                    color=theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=self._criar_botao_criar_conta(),
                            expand=True,
                        ),
                    ],
                ),
                ft.Container(expand=True),
                self._criar_rodape(),
            ],
            spacing=theme.SPACE_MD,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
