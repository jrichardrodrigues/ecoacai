import flet as ft

from views.showroom_view import ShowroomView


def main(page: ft.Page):

    page.title = "Showroom"

    page.add(

        ShowroomView().build()

    )


ft.run(main)