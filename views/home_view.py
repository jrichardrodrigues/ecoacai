import flet as ft

from components import criar_app_bar, criar_menu
from controllers.navigation_controller import NavigationController


def construir_interface(page: ft.Page) -> None:
    """Monta a área principal exibida após o login."""

    page.clean()
    page.appbar = criar_app_bar()

    navigation_controller = NavigationController(page)

    def ao_mudar_menu(e: ft.ControlEvent) -> None:
        indice_selecionado = e.control.selected_index

        if indice_selecionado is None:
            return

        navigation_controller.mudar_tela(indice_selecionado)
        page.update()

    menu = criar_menu(ao_mudar_menu)

    layout_principal = ft.Row(
        controls=[
            menu,
            ft.VerticalDivider(width=1),
            navigation_controller.conteudo,
        ],
        expand=True,
        spacing=0,
    )

    page.add(layout_principal)
    page.update()