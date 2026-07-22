from collections.abc import Callable

import flet as ft

from models import Estabelecimento, Solicitacao
from views.cadastro_view import CadastroView
from views.estabelecimentos_view import EstabelecimentosView
from views.solicitacoes_view import SolicitacoesView
from views.solicitacao_form_view import SolicitacaoFormView
from views.dashboard_view import DashboardView
from views.home_page import HomeView


class NavigationController:
    """Controla a troca do conteúdo principal da aplicação."""

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
            3: self._solicitacoes,
            4: lambda: self._tela_temporaria(
                "Coletas Ativas",
                "Acompanhe em tempo real as coletas pendentes, agendadas e em andamento.",
            ),
            5: self._dashboard,
        }

    def _mostrar(self, controle: ft.Control) -> None:
        """Exibe um controle na área principal da aplicação."""

        self.conteudo.content = controle
        self.page.update()

    def _dashboard(self) -> ft.Control:
        """Abre o Dashboard."""

        return DashboardView(
            page=self.page,
        ).build()

    def _home(self) -> ft.Control:
        return HomeView().build()

    def _cadastro(self) -> ft.Control:
        return CadastroView(
            page=self.page,
            on_salvar_sucesso=self.abrir_estabelecimentos,
        ).construir()

    def _estabelecimentos(self) -> ft.Control:
        return EstabelecimentosView(
            page=self.page,
            on_novo=self.abrir_cadastro,
            on_editar=self.abrir_edicao,
            on_solicitar_coleta=self.abrir_nova_solicitacao_para_estabelecimento,
        ).build()

    def _solicitacoes(self) -> ft.Control:
        """Abre a lista de solicitações."""

        return SolicitacoesView(
            page=self.page,
            on_nova_solicitacao=self.abrir_nova_solicitacao,
            on_editar_solicitacao=self.abrir_edicao_solicitacao,
        ).build()

    def abrir_cadastro(self) -> None:
        """Abre o formulário no modo de cadastro."""

        self._mostrar(self._cadastro())

    def abrir_edicao(
            self,
            estabelecimento: Estabelecimento,
    ) -> None:
        """Abre o formulário preenchido no modo de edição."""

        cadastro_view = CadastroView(
            page=self.page,
            estabelecimento=estabelecimento,
            on_salvar_sucesso=self.abrir_estabelecimentos,
        )

        self._mostrar(cadastro_view.construir())

    def abrir_estabelecimentos(self) -> None:
        """Retorna à listagem e recarrega os dados."""

        self._mostrar(self._estabelecimentos())

    def abrir_solicitacoes(self) -> None:
        """Retorna para a lista de solicitações."""

        self._mostrar(self._solicitacoes())

    def abrir_nova_solicitacao(self) -> None:
        """Abre o formulário de nova solicitação."""

        formulario = SolicitacaoFormView(
            page=self.page,
            on_cancelar=self.abrir_solicitacoes,
            on_salvar_sucesso=self.abrir_solicitacoes,
        )

        self._mostrar(formulario.build())

    def abrir_nova_solicitacao_para_estabelecimento(
            self,
            estabelecimento_id: int,
    ) -> None:
        """Abre uma nova solicitação já vinculada ao estabelecimento."""

        formulario = SolicitacaoFormView(
            page=self.page,
            estabelecimento_id=estabelecimento_id,
            on_cancelar=self.abrir_solicitacoes,
            on_salvar_sucesso=self.abrir_solicitacoes,
        )

        self._mostrar(formulario.build())

    def abrir_edicao_solicitacao(
            self,
            solicitacao: Solicitacao,
    ) -> None:
        """Abre o formulário em modo de edição."""

        formulario = SolicitacaoFormView(
            page=self.page,
            solicitacao=solicitacao,
            on_cancelar=self.abrir_solicitacoes,
            on_salvar_sucesso=self.abrir_solicitacoes,
        )

        self._mostrar(formulario.build())

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
        """Muda a tela com base no índice do menu."""

        construtor_tela = self._rotas.get(
            indice,
            self._home,
        )

        self._mostrar(construtor_tela())