from models import Usuario
from repositories import UsuarioRepository
from services import PasswordService


class AuthService:
    """Executa as regras de autenticação do usuário."""

    def __init__(self) -> None:
        self.repository = UsuarioRepository()
        self.password_service = PasswordService()

    def autenticar(
        self,
        cpf: str,
        senha: str,
    ) -> tuple[bool, str, Usuario | None]:
        """
        Autentica um usuário utilizando CPF e senha.

        Retorna:
            (sucesso, mensagem, usuario)
        """

        usuario = self.repository.buscar_por_cpf(cpf)

        if usuario is None:
            return False, "CPF não encontrado.", None

        if not usuario.ativo:
            return False, "Usuário desativado.", None

        if not usuario.celular_confirmado:
            return (
                False,
                "Confirme o WhatsApp antes de entrar.",
                None,
            )

        if not self.password_service.verificar(
            senha,
            usuario.senha_hash,
        ):
            return False, "Senha incorreta.", None

        return True, "Login realizado com sucesso.", usuario