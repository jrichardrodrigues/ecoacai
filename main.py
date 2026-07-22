import flet as ft

from config import APP_NAME, COR_FUNDO
from controllers.auth_controller import AuthController
from repositories.sqlite_database import SQLiteDatabase
from views.home_view import construir_interface
from views.login_view import LoginView


def main(page: ft.Page) -> None:
    SQLiteDatabase().inicializar()

    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COR_FUNDO
    page.padding = 0

    auth_controller = AuthController()

    def abrir_area_principal(usuario) -> None:
        page.clean()
        construir_interface(page)
        page.update()

    def abrir_criar_conta(e: ft.ControlEvent) -> None:
        print("Abrir tela de criação de conta")

    def abrir_recuperacao_senha(e: ft.ControlEvent) -> None:
        print("Abrir recuperação de senha")

    login_view = LoginView(
        page=page,
        auth_controller=auth_controller,
        on_login_sucesso=abrir_area_principal,
        on_criar_conta=abrir_criar_conta,
        on_esqueci_senha=abrir_recuperacao_senha,
    )

    # page.add(login_view.build())

    # Teste temporário: abre diretamente a área principal.
    construir_interface(page)


if __name__ == "__main__":
    ft.run(main=main)