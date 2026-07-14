from collections.abc import Callable

import flet as ft

from views.cadastro_view import CadastroView
from views.estabelecimentos_view import EstabelecimentosView


class NavigationController:

    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.conteudo = ft.Container(
            expand=True,
            padding=20,
            content=self._home(),
        )

        self._rotas: dict[int, Callable[[], ft.Control]] = {
            0: self._home,
            1: self._cadastro,
            2: self._estabelecimentos,
            3: lambda: self._tela_temporaria(
                "Coletas",
                "Aqui ficará a tela de solicitação de coletas.",
            ),
            4: lambda: self._tela_temporaria(
                "Painel",
                "Aqui ficará o painel de solicitações ativas.",
            ),
            5: lambda: self._tela_temporaria(
                "Dashboard",
                "Aqui ficarão os indicadores do sistema.",
            ),
        }

    def _home(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text(
                    "Bem-vindo ao sistema",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Açaí Coleta",
                    size=18,
                ),
                ft.Divider(),
                ft.Text(
                    "Use o menu lateral para navegar entre "
                    "as funcionalidades.",
                    size=16,
                ),
            ],
            spacing=10,
        )

    def _cadastro(self) -> ft.Control:
        return CadastroView(
            self.page,
            on_salvar_sucesso=self.abrir_estabelecimentos,
        ).construir()

    def _estabelecimentos(self):
        return EstabelecimentosView(
            self.page,
            on_novo=self.abrir_cadastro,
        ).build()

    def abrir_cadastro(self) -> None:
        self.conteudo.content = self._cadastro()
        self.page.update()

    def abrir_estabelecimentos(self) -> None:
        self.conteudo.content = self._estabelecimentos()
        self.page.update()

    def _tela_temporaria(
        self,
        titulo: str,
        descricao: str,
    ) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text(
                    titulo,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    descricao,
                    size=16,
                ),
                ft.Divider(),
                ft.Text(
                    "Tela em desenvolvimento.",
                    italic=True,
                ),
            ],
            spacing=10,
        )

    def mudar_tela(self, indice: int) -> None:
        construtor_tela = self._rotas.get(
            indice,
            self._home,
        )

        self.conteudo.content = construtor_tela()