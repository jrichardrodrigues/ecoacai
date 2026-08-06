from __future__ import annotations

import flet as ft

from components.ui import theme
from .auth_mode import AuthMode


class AuthHeader(ft.Column):
    TITULOS = {
        AuthMode.LOGIN: "Bem-vindo à ZELURBIS",
        AuthMode.RECOVERY: "Recuperar senha",
        AuthMode.REGISTER: "Criar sua conta",
    }

    SUBTITULOS = {
        AuthMode.LOGIN: "Acesse sua conta para continuar.",
        AuthMode.RECOVERY: "Informe seu CPF e defina uma nova senha.",
        AuthMode.REGISTER: "Preencha seus dados para acessar a plataforma.",
    }

    def __init__(self, mode: AuthMode) -> None:
        super().__init__(
            controls=[
                ft.Text(
                    self.TITULOS[mode],
                    size=theme.TITLE,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXT_PRIMARY,
                ),
                ft.Text(
                    self.SUBTITULOS[mode],
                    size=theme.BODY,
                    color=theme.TEXT_SECONDARY,
                ),
            ],
            spacing=theme.SPACE_XS,
        )
