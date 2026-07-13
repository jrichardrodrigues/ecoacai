import flet as ft

from components import criar_app_bar, criar_menu
from controllers import NavigationController


def construir_interface(page: ft.Page):
    page.clean()
    page.appbar = None

    page.title = "Controle de Recolhimento de Caroço do Açaí"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    page.appbar = criar_app_bar()

    navigation_controller = NavigationController(page)

    def ao_mudar_menu(e):
        navigation_controller.mudar_tela(
            e.control.selected_index
        )
        page.update()

    menu = criar_menu(ao_mudar_menu)

    page.add(
        ft.Row(
            controls=[
                menu,
                ft.VerticalDivider(width=1),
                navigation_controller.conteudo,
            ],
            expand=True,
        )
    )

    page.update()