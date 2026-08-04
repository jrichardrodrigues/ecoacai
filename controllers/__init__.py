from .auth_controller import AuthController
from .coletas_agendadas_controller import ColetasAgendadasController
from .dashboard_controller import DashboardController
from .estabelecimento_controller import EstabelecimentoController
from .login_controller import LoginController
from .motorista_controller import MotoristaController
from .organizacao_controller import OrganizacaoController
from .solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from .usuario_controller import UsuarioController
from .veiculo_controller import VeiculoController


__all__ = [
    "AuthController",
    "ColetasAgendadasController",
    "DashboardController",
    "EstabelecimentoController",
    "LoginController",
    "MotoristaController",
    "OrganizacaoController",
    "SolicitacaoColetaController",
    "UsuarioController",
    "VeiculoController",
]