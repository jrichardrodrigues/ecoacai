import flet as ft


def mostrar_mensagem(
    page: ft.Page,
    texto: str,
    cor: str,
    icone,
) -> None:
    """Exibe uma mensagem padronizada no ECOAÇAÍ."""

    snackbar = ft.SnackBar(
        bgcolor=cor,
        behavior=ft.SnackBarBehavior.FLOATING,
        margin=20,
        duration=3000,
        show_close_icon=True,
        content=ft.Row(
            controls=[
                ft.Icon(
                    icone,
                    color=ft.Colors.WHITE,
                    size=22,
                ),
                ft.Text(
                    texto,
                    color=ft.Colors.WHITE,
                    size=15,
                    weight=ft.FontWeight.W_500,
                    expand=True,
                ),
            ],
            spacing=12,
        ),
        open=True,
    )

    page.overlay.append(snackbar)
    page.update()


def mostrar_sucesso(
    page: ft.Page,
    texto: str,
) -> None:
    mostrar_mensagem(
        page,
        texto,
        ft.Colors.GREEN_700,
        ft.Icons.CHECK_CIRCLE,
    )


def mostrar_erro(
    page: ft.Page,
    texto: str,
) -> None:
    mostrar_mensagem(
        page,
        texto,
        ft.Colors.RED_700,
        ft.Icons.ERROR,
    )


def mostrar_aviso(
    page: ft.Page,
    texto: str,
) -> None:
    mostrar_mensagem(
        page,
        texto,
        ft.Colors.ORANGE_700,
        ft.Icons.WARNING,
    )


def mostrar_info(
    page: ft.Page,
    texto: str,
) -> None:
    mostrar_mensagem(
        page,
        texto,
        ft.Colors.BLUE_700,
        ft.Icons.INFO,
    )