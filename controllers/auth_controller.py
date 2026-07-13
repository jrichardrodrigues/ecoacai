from models import Usuario
from services import AuthService


class AuthController:
    """Ponte entre as telas de autenticação e o AuthService."""

    def __init__(self):
        self.auth_service = AuthService()
        self.usuario_logado: Usuario | None = None

    def entrar(
        self,
        cpf: str,
        senha: str,
    ) -> tuple[bool, str]:
        sucesso, mensagem, usuario = (
            self.auth_service.autenticar(cpf, senha)
        )

        if sucesso:
            self.usuario_logado = usuario

        return sucesso, mensagem

    def sair(self):
        self.usuario_logado = None

    def esta_autenticado(self) -> bool:
        return self.usuario_logado is not None