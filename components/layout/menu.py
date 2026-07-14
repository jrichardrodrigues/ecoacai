import flet as ft


def criar_menu(on_change):
    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=90,
        min_extended_width=220,
        leading=ft.Icon(
            ft.Icons.LOCAL_SHIPPING,
            size=40,
        ),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PERSON_ADD_ALT_OUTLINED,
                selected_icon=ft.Icons.PERSON_ADD,
                label="Cadastro",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.STORE_OUTLINED,
                selected_icon=ft.Icons.STORE,
                label="Estabelecimentos",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.LOCAL_SHIPPING_OUTLINED,
                selected_icon=ft.Icons.LOCAL_SHIPPING,
                label="Coletas",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.LIST_ALT_OUTLINED,
                selected_icon=ft.Icons.LIST_ALT,
                label="Painel",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BAR_CHART_OUTLINED,
                selected_icon=ft.Icons.BAR_CHART,
                label="Dashboard",
            ),
        ],
        on_change=on_change,
    )