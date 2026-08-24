import flet as ft

from components import criar_app_bar, criar_menu
from controllers.navigation_controller import NavigationController


def construir_interface(
        page: ft.Page,
        on_voltar_zelurbis=None,
) -> None:
    """Monta a área principal exibida após o login."""

    page.clean()

    page.appbar = criar_app_bar(
        on_voltar_zelurbis=on_voltar_zelurbis,
    )

    navigation_controller = NavigationController(page)

    menu_area = ft.Container()

    def ao_mudar_menu(indice: int) -> None:
        """Atualiza o menu selecionado e muda a tela."""

        menu_area.content = criar_menu(
            on_change=ao_mudar_menu,
            indice_selecionado=indice,
        )

        navigation_controller.mudar_tela(indice)

    menu_area.content = criar_menu(
        on_change=ao_mudar_menu,
        indice_selecionado=0,
    )

    layout_principal = ft.Row(
        controls=[
            menu_area,
            ft.VerticalDivider(width=1),
            navigation_controller.conteudo,
        ],
        expand=True,
        spacing=0,
    )

    page.add(layout_principal)
    page.update()