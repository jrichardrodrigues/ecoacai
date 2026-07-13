import flet as ft

from config import APP_NAME, COR_FUNDO
from controllers import AuthController
from repositories import SQLiteDatabase
from utils.messages import mostrar_erro, mostrar_sucesso
from views.home_view import construir_interface
from views.login_view import LoginView


def main(page: ft.Page):
    SQLiteDatabase().inicializar()

    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COR_FUNDO
    page.padding = 0

    auth_controller = AuthController()

    def mostrar_login():
        page.clean()
        page.appbar = None

        login_view = LoginView(
            page=page,
            auth_controller=auth_controller,
            on_login_sucesso=login_realizado,
            on_criar_conta=abrir_cadastro,
            on_esqueci_senha=abrir_recuperacao,
        )

        page.add(login_view.construir())
        page.update()

    def login_realizado(usuario):
        construir_interface(page)

        mostrar_sucesso(
            page,
            f"Bem-vindo, {usuario.nome}!",
        )

    def abrir_cadastro(e):
        mostrar_erro(
            page,
            "A tela de criação da conta será "
            "implementada na próxima etapa.",
        )

    def abrir_recuperacao(e):
        mostrar_erro(
            page,
            "A recuperação pelo WhatsApp será "
            "implementada em uma próxima etapa.",
        )

    mostrar_login()


if __name__ == "__main__":
    ft.run(main=main)