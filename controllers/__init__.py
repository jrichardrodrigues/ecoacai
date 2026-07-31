from .auth_controller import AuthController
from .coletas_agendadas_controller import ColetasAgendadasController
from .dashboard_controller import DashboardController
from .estabelecimento_controller import EstabelecimentoController
from .motorista_controller import MotoristaController
from .solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from .veiculo_controller import VeiculoController


__all__ = [
    "AuthController",
    "ColetasAgendadasController",
    "DashboardController",
    "EstabelecimentoController",
    "MotoristaController",
    "SolicitacaoColetaController",
    "VeiculoController",
]