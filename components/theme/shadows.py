import flet as ft


class Shadows:
    """
    Sistema oficial de sombras do EcoAçaí.

    Todas as superfícies da aplicação devem utilizar estas
    constantes para manter consistência visual.
    """

    # ==========================================================
    # Cards
    # ==========================================================

    CARD = ft.BoxShadow(
        spread_radius=0,
        blur_radius=6,
        color=ft.Colors.with_opacity(
            0.10,
            ft.Colors.BLACK,
        ),
        offset=ft.Offset(0, 1),
    )

    CARD_HOVER = ft.BoxShadow(
        spread_radius=0,
        blur_radius=12,
        color=ft.Colors.with_opacity(
            0.15,
            ft.Colors.BLACK,
        ),
        offset=ft.Offset(0, 4),
    )

    # ==========================================================
    # Diálogos
    # ==========================================================

    DIALOG = ft.BoxShadow(
        spread_radius=0,
        blur_radius=24,
        color=ft.Colors.with_opacity(
            0.20,
            ft.Colors.BLACK,
        ),
        offset=ft.Offset(0, 8),
    )

    # ==========================================================
    # Menus e Popups
    # ==========================================================

    POPUP = ft.BoxShadow(
        spread_radius=0,
        blur_radius=16,
        color=ft.Colors.with_opacity(
            0.18,
            ft.Colors.BLACK,
        ),
        offset=ft.Offset(0, 6),
    )

    # ==========================================================
    # Botões elevados
    # ==========================================================

    BUTTON = ft.BoxShadow(
        spread_radius=0,
        blur_radius=4,
        color=ft.Colors.with_opacity(
            0.12,
            ft.Colors.BLACK,
        ),
        offset=ft.Offset(0, 2),
    )

    # ==========================================================
    # AppBar
    # ==========================================================

    APPBAR = ft.BoxShadow(
        spread_radius=0,
        blur_radius=8,
        color=ft.Colors.with_opacity(
            0.08,
            ft.Colors.BLACK,
        ),
        offset=ft.Offset(0, 2),
    )

    # ==========================================================
    # Sidebar
    # ==========================================================

    SIDEBAR = ft.BoxShadow(
        spread_radius=0,
        blur_radius=10,
        color=ft.Colors.with_opacity(
            0.08,
            ft.Colors.BLACK,
        ),
        offset=ft.Offset(2, 0),
    )

    # ==========================================================
    # Sem sombra
    # ==========================================================

    NONE = None