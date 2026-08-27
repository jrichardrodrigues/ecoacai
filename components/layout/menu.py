import flet as ft

from config import COR_ECOACAI


def criar_menu(
    on_change,
    indice_selecionado: int = 0,
):
    """Cria o menu lateral do módulo ECOAÇAÍ."""

    itens = [
        ("Home", ft.Icons.HOME_ROUNDED),
        ("Cadastro", ft.Icons.PERSON_ADD_ALT_1_ROUNDED),
        ("Solicitantes", ft.Icons.STORE_ROUNDED),
        ("Solicitações", ft.Icons.LOCAL_SHIPPING_ROUNDED),
        ("Motoristas", ft.Icons.BADGE_ROUNDED),
        ("Veículos", ft.Icons.FIRE_TRUCK_ROUNDED),
        ("Operação de Coletas", ft.Icons.LIST_ALT_ROUNDED),
        ("Dashboard", ft.Icons.BAR_CHART_ROUNDED),
        ("Relatórios", ft.Icons.DESCRIPTION_ROUNDED),
    ]

    controles = []

    for indice, (titulo, icone) in enumerate(itens):
        selecionado = indice == indice_selecionado

        controles.append(
            ft.Container(
                height=54,
                padding=ft.Padding.symmetric(
                    horizontal=16,
                ),
                border_radius=10,
                bgcolor=(
                    ft.Colors.with_opacity(
                        0.16,
                        ft.Colors.WHITE,
                    )
                    if selecionado
                    else None
                ),
                ink=True,
                on_click=lambda _e, i=indice: on_change(i),
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            icone,
                            size=26,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            titulo,
                            size=15,
                            weight=(
                                ft.FontWeight.W_700
                                if selecionado
                                else ft.FontWeight.W_600
                            ),
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        )

    return ft.Container(
        width=250,
        bgcolor=COR_ECOACAI,
        padding=ft.Padding.only(
            left=12,
            right=12,
            top=22,
            bottom=22,
        ),
        content=ft.Column(
            controls=controles,
            spacing=6,
        ),
    )