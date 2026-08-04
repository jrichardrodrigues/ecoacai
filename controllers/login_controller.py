from controllers.auth_controller import AuthController
from models import SessaoUsuario


class LoginController:
    """
    Coordena o fluxo de entrada da aplicação.
    """

    def __init__(
        self,
        auth_controller: AuthController | None = None,
    ) -> None:

        self.auth_controller = (
            auth_controller or AuthController()
        )

    def entrar(
        self,
        cpf: str,
        senha: str,
    ) -> tuple[bool, str]:

        return self.auth_controller.entrar(
            cpf,
            senha,
        )

    def obter_sessao(
        self,
    ) -> SessaoUsuario | None:

        return self.auth_controller.obter_sessao()

    def precisa_configurar_organizacao(
        self,
    ) -> bool:

        return (
            self.auth_controller
            .precisa_configurar_organizacao()
        )

    def sair(
        self,
    ) -> None:

        self.auth_controller.sair()