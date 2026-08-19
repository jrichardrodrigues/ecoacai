from collections.abc import Callable

from datetime import date

import flet as ft

from models import Estabelecimento, Motorista, Solicitacao, Veiculo
from views.cadastro_view import CadastroView
from views.estabelecimentos_view import EstabelecimentosView
from views.solicitacao_form_view import SolicitacaoFormView
from views.dashboard_view import DashboardView
from views.home_page import HomeView
from views.motorista_form_view import MotoristaFormView
from views.motoristas_view import MotoristasView
from views.veiculos_view import VeiculosView
from views.coletas_agendadas_view import ColetasAgendadasView
from views.solicitacoes_gestor_view import SolicitacoesGestorView
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from views.detalhe_solicitacao_gestor_view import (
    DetalheSolicitacaoGestorView,
)
from views.detalhe_coleta_view import DetalheColetaView


class NavigationController:
    """Controla a troca do conteúdo principal da aplicação."""

    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.solicitacao_coleta_controller = (
            SolicitacaoColetaController()
        )

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
            4: self._motoristas,
            5: self._veiculos,
            6: self._coletas_agendadas,
            7: self._dashboard,
        }

    def _mostrar(self, controle: ft.Control) -> None:
        """Exibe um controle na área principal da aplicação."""

        self.conteudo.content = controle
        self.page.update()

    def _dashboard(self) -> ft.Control:
        """Abre o Dashboard."""

        return DashboardView(
            page=self.page,
            on_abrir_solicitacoes=self.abrir_solicitacoes_pendentes,
            on_abrir_agendadas=self.abrir_solicitacoes_agendadas,
            on_abrir_em_coleta=self.abrir_solicitacoes_em_coleta,
            on_abrir_concluidas=self.abrir_solicitacoes_concluidas,
            on_abrir_canceladas=self.abrir_solicitacoes_canceladas,
            on_abrir_para_hoje=self.abrir_solicitacoes_para_hoje,
            on_abrir_todas_solicitacoes=self.abrir_todas_solicitacoes,
            on_abrir_solicitantes=self.abrir_solicitantes,
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

    def _motoristas(self) -> ft.Control:
        """Abre a lista de motoristas."""

        return MotoristasView(
            page=self.page,
            on_novo=self.abrir_cadastro_motorista,
            on_editar=self.abrir_edicao_motorista,
        ).construir()

    def _veiculos(self) -> ft.Control:
        """Abre a lista de veículos."""

        return VeiculosView(
            page=self.page,
            ao_voltar=self._home,
        ).build()

    def _solicitacoes(
            self,
            status_inicial: str | None = None,
            data_agendada_inicial: str | None = None,
            titulo: str = "Solicitações",
            subtitulo: str = "Analise as solicitações de coleta recebidas dos Geradores.",
    ) -> ft.Control:
        """Abre a fila de solicitações recebidas pelo Gestor."""

        return SolicitacoesGestorView(
            page=self.page,
            controller=self.solicitacao_coleta_controller,
            on_ver_detalhes=self.abrir_detalhe_solicitacao,
            status_inicial=status_inicial,
            data_agendada_inicial=data_agendada_inicial,
            titulo=titulo,
            subtitulo=subtitulo,
        ).build()

    def abrir_solicitacoes_pendentes(self) -> None:
        self._mostrar(
            self._solicitacoes(
                status_inicial="PENDENTES",
                titulo="Solicitações Pendentes",
                subtitulo="Solicitações aguardando análise ou atendimento.",
            )
        )

    def abrir_solicitacoes_agendadas(self) -> None:
        self._mostrar(
            self._solicitacoes(
                status_inicial="AGENDADA",
                titulo="Coletas Agendadas",
                subtitulo="Coletas programadas para execução.",
            )
        )

    def abrir_solicitacoes_em_coleta(self) -> None:
        self._mostrar(
            self._solicitacoes(
                status_inicial="EM_COLETA",
                titulo="Coletas em Andamento",
                subtitulo="Coletas atualmente em execução.",
            )
        )

    def abrir_solicitacoes_concluidas(self) -> None:
        self._mostrar(
            self._solicitacoes(
                status_inicial="CONCLUIDA",
                titulo="Coletas Concluídas",
                subtitulo="Coletas finalizadas pela operação.",
            )
        )

    def abrir_solicitacoes_canceladas(self) -> None:
        self._mostrar(
            self._solicitacoes(
                status_inicial="CANCELADA",
                titulo="Solicitações Canceladas",
                subtitulo="Solicitações que foram canceladas.",
            )
        )

    def abrir_solicitacoes_para_hoje(self) -> None:
        hoje = date.today().isoformat()

        self._mostrar(
            self._solicitacoes(
                data_agendada_inicial=hoje,
                titulo="Coletas para Hoje",
                subtitulo="Coletas programadas para a data de hoje.",
            )
        )

    def abrir_todas_solicitacoes(self) -> None:
        self._mostrar(
            self._solicitacoes(
                titulo="Todas as Solicitações",
                subtitulo="Consulte todas as solicitações cadastradas no sistema.",
            )
        )

    def abrir_detalhe_solicitacao(
            self,
            solicitacao_id: int,
            solicitante: str,
    ) -> None:
        """Abre os detalhes de uma solicitação para o Gestor."""

        solicitacao = (
            self.solicitacao_coleta_controller.buscar_por_id(
                solicitacao_id
            )
        )

        if solicitacao is None:
            return

        view = DetalheSolicitacaoGestorView(
            solicitacao=solicitacao,
            solicitante=solicitante,
            on_voltar=self.abrir_solicitacoes,
            on_agendar=self.abrir_agendamento_solicitacao,
        )

        self._mostrar(
            view.build()
        )

    def abrir_agendamento_solicitacao(
            self,
            solicitacao,
    ) -> None:
        """Abre a área de Coletas Agendadas para a solicitação selecionada."""

        view = ColetasAgendadasView(
            page=self.page,
        )

        controle = view.build()

        self._mostrar(
            controle
        )

        view._abrir_dialog_agendamento(
            solicitacao_id=solicitacao.id
        )

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

    def abrir_solicitantes(self) -> None:
        """Abre a relação de solicitantes cadastrados."""
        self._mostrar(
            self._estabelecimentos()
        )

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

    def _coletas_agendadas(self) -> ft.Control:
        """Abre a tela de coletas agendadas."""

        return ColetasAgendadasView(
            page=self.page,
            on_visualizar_coleta=self.abrir_detalhe_coleta,
        ).build()

    def _coletas_agendadas(self) -> ft.Control:
        """Abre a tela de coletas agendadas."""

        return ColetasAgendadasView(
            page=self.page,
            on_visualizar_coleta=self.abrir_detalhe_coleta,
        ).build()

    def abrir_detalhe_coleta(
            self,
            coleta: dict,
    ) -> None:
        """Abre a tela de detalhes de uma coleta."""

        view = DetalheColetaView(
            page=self.page,
            coleta=coleta,
            on_voltar=self.abrir_coletas_agendadas,
        )

        self._mostrar(
            view.build()
        )

    def abrir_coletas_agendadas(self) -> None:
        """Abre a tela de coletas agendadas."""

        self._mostrar(
            self._coletas_agendadas()
        )

    def abrir_motoristas(self) -> None:
        """Retorna à listagem de motoristas."""

        self._mostrar(
            self._motoristas(),
        )

    def abrir_veiculos(self) -> None:
        """Retorna à listagem de veículos."""

        self._mostrar(
            self._veiculos(),
        )

    def abrir_cadastro_motorista(self) -> None:
        """Abre o formulário de cadastro de motorista."""

        formulario = MotoristaFormView(
            page=self.page,
            on_salvar_sucesso=self.abrir_motoristas,
        )

        self._mostrar(
            formulario.construir(),
        )

    def abrir_cadastro_veiculo(self) -> None:
        formulario = VeiculoFormView(
            page=self.page,
            ao_salvar=self.abrir_veiculos,
            ao_cancelar=self.abrir_veiculos,
        )

        self._mostrar(
            formulario.build(),
        )

    def abrir_edicao_motorista(
            self,
            motorista: Motorista,
    ) -> None:
        """Abre o formulário de motorista no modo de edição."""

        formulario = MotoristaFormView(
            page=self.page,
            motorista=motorista,
            on_salvar_sucesso=self.abrir_motoristas,
        )

        self._mostrar(
            formulario.construir(),
        )

    def abrir_edicao_veiculo(
            self,
            veiculo: Veiculo,
    ) -> None:
        formulario = VeiculoFormView(
            page=self.page,
            veiculo=veiculo,
            ao_salvar=self.abrir_veiculos,
            ao_cancelar=self.abrir_veiculos,
        )

        self._mostrar(
            formulario.build(),
        )

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