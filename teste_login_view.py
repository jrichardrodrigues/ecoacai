import flet as ft

from views.login_view import LoginView


def main(page: ft.Page):

    page.title = "EcoAçaí"

    page.add(

        LoginView(page).build()

    )


if __name__ == "__main__":
    ft.run(main)