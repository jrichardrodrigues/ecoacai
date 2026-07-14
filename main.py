import flet as ft

from config import APP_NAME, COR_FUNDO
from repositories.sqlite_database import SQLiteDatabase
from views.home_view import construir_interface


def main(page: ft.Page) -> None:
    SQLiteDatabase().inicializar()

    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COR_FUNDO
    page.padding = 0

    # Teste temporário: abre diretamente a área principal.
    construir_interface(page)


if __name__ == "__main__":
    ft.run(main=main)