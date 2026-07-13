import flet as ft

from components import (
    criar_app_bar,
    criar_menu,
    card_titulo,
)


def main(page: ft.Page):

    page.title = "Teste"

    page.appbar = criar_app_bar()

    menu = criar_menu(
        lambda e: print(e.control.selected_index)
    )

    conteudo = ft.Column(
        [
            card_titulo("Componentes funcionando!")
        ],
        expand=True,
    )

    page.add(
        ft.Row(
            [
                menu,
                ft.VerticalDivider(),
                conteudo,
            ],
            expand=True,
        )
    )


ft.run(main)