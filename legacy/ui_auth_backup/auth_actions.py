from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.ui import theme
from .auth_mode import AuthMode


class AuthActions(ft.Column):
    def __init__(
        self,
        *,
        mode: AuthMode,
        on_primary: Callable[[ft.ControlEvent], None],
        on_back: Callable[[ft.ControlEvent], None] | None = None,
        on_register: Callable[[ft.ControlEvent], None] | None = None,
        on_forgot_password: Callable[[ft.ControlEvent], None] | None = None,
    ) -> None:
        controls: list[ft.Control] = []

        if mode == AuthMode.LOGIN:
            controls.append(
                ft.FilledButton(
                    content="ENTRAR",
                    icon=ft.Icons.LOGIN_ROUNDED,
                    on_click=on_primary,
                    height=48,
                    expand=True,
                    style=self._primary_style(),
                )
            )

            if on_register is not None:
                controls.extend([
                    ft.Row(
                        controls=[
                            ft.Divider(color=theme.BORDER, expand=True),
                            ft.Text(
                                "ou",
                                size=theme.CAPTION,
                                color=theme.TEXT_SECONDARY,
                            ),
                            ft.Divider(color=theme.BORDER, expand=True),
                        ],
                        spacing=theme.SPACE_SM,
                    ),
                    ft.Text(
                        "Ainda não possui uma conta?",
                        size=theme.BODY,
                        color=theme.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.OutlinedButton(
                        content="CRIAR CONTA",
                        icon=ft.Icons.PERSON_ADD_OUTLINED,
                        on_click=on_register,
                        height=46,
                        expand=True,
                        style=self._secondary_style(),
                    ),
                ])

            self.forgot_password_button = ft.TextButton(
                content="Esqueci minha senha",
                icon=ft.Icons.KEY_OUTLINED,
                on_click=on_forgot_password,
                visible=on_forgot_password is not None,
                style=ft.ButtonStyle(
                    color=theme.PRIMARY,
                    padding=0,
                ),
            )
        else:
            label = "ALTERAR SENHA" if mode == AuthMode.RECOVERY else "CRIAR CONTA"
            icon = ft.Icons.LOCK_RESET if mode == AuthMode.RECOVERY else ft.Icons.PERSON_ADD_OUTLINED

            controls.append(
                ft.FilledButton(
                    content=label,
                    icon=icon,
                    on_click=on_primary,
                    height=48,
                    expand=True,
                    style=self._primary_style(),
                )
            )

            if on_back is not None:
                controls.append(
                    ft.TextButton(
                        content="Voltar ao login",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=on_back,
                        style=ft.ButtonStyle(color=theme.PRIMARY),
                    )
                )

            self.forgot_password_button = None

        super().__init__(
            controls=controls,
            spacing=theme.SPACE_MD,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    @staticmethod
    def _primary_style() -> ft.ButtonStyle:
        return ft.ButtonStyle(
            bgcolor=theme.PRIMARY,
            color=theme.SURFACE,
            shape=ft.RoundedRectangleBorder(radius=theme.RADIUS_MD),
        )

    @staticmethod
    def _secondary_style() -> ft.ButtonStyle:
        return ft.ButtonStyle(
            color=theme.PRIMARY,
            side=ft.BorderSide(width=1, color=theme.PRIMARY),
            shape=ft.RoundedRectangleBorder(radius=theme.RADIUS_MD),
        )
