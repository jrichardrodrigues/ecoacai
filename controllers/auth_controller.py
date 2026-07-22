from models import Usuario
from services import AuthService


class AuthController:
    """Ponte entre as telas de autenticação e o AuthService."""

    def __init__(self) -> None:
        self.auth_service = AuthService()
        self._usuario_logado: Usuario | None = None

    @property
    def usuario_logado(self) -> Usuario | None:
        """Retorna o usuário atualmente autenticado."""

        return self._usuario_logado

    def entrar(
        self,
        cpf: str,
        senha: str,
    ) -> tuple[bool, str]:
        """Autentica um usuário."""

        sucesso, mensagem, usuario = (
            self.auth_service.autenticar(cpf, senha)
        )

        if sucesso:
            self._usuario_logado = usuario
        else:
            self._usuario_logado = None

        return sucesso, mensagem

    def sair(self) -> None:
        """Encerra a sessão do usuário autenticado."""

        self._usuario_logado = None

    def esta_autenticado(self) -> bool:
        """Informa se existe um usuário autenticado."""

        return self._usuario_logado is not None