import flet as ft

from views.cadastro_view import CadastroView


class NavigationController:

    def __init__(self, page: ft.Page):
        self.page = page

        self.conteudo = ft.Container(
            expand=True,
            padding=20,
            content=self._home(),
        )

    def _home(self):
        return ft.Column(
            controls=[
                ft.Text("Bem-vindo ao sistema", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Controle de Recolhimento de Caroço do Açaí", size=18),
                ft.Divider(),
                ft.Text("Use o menu lateral para navegar entre as funcionalidades.", size=16),
            ],
            spacing=10,
        )

    def _tela_temporaria(self, titulo: str, descricao: str):
        return ft.Column(
            controls=[
                ft.Text(titulo, size=28, weight=ft.FontWeight.BOLD),
                ft.Text(descricao, size=16),
                ft.Divider(),
                ft.Text("Tela em desenvolvimento.", italic=True),
            ],
            spacing=10,
        )

    def mudar_tela(self, indice: int):
        if indice == 0:
            self.conteudo.content = self._home()

        elif indice == 1:
            self.conteudo.content = CadastroView(self.page).construir()

        elif indice == 2:
            self.conteudo.content = self._tela_temporaria(
                "Coletas",
                "Aqui ficará a tela de solicitação de coletas.",
            )

        elif indice == 3:
            self.conteudo.content = self._tela_temporaria(
                "Painel",
                "Aqui ficará o painel de solicitações ativas.",
            )

        elif indice == 4:
            self.conteudo.content = self._tela_temporaria(
                "Dashboard",
                "Aqui ficarão os indicadores do sistema.",
            )

        else:
            self.conteudo.content = self._home()