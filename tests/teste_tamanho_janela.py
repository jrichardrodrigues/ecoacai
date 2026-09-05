import flet as ft


def main(page: ft.Page) -> None:
    page.title = "Teste tamanho mínimo"

    page.window.width = 1330
    page.window.height = 920

    page.window.min_width = 1200
    page.window.min_height = 700

    page.add(
        ft.Text(
            "Tente reduzir esta janela abaixo de 1200 x 700",
            size=24,
        )
    )


ft.run(main)