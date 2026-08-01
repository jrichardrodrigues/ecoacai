import flet as ft

from views.coletas_agendadas_view import ColetasAgendadasView


def main(page: ft.Page):
    page.title = "Teste - Coletas Agendadas"
    page.window.width = 1600
    page.window.height = 900
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO

    view = ColetasAgendadasView(page)

    page.add(view.build())


ft.app(target=main)