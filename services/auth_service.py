from repositories import UsuarioRepository
from services import PasswordService


class AuthService:

    def __init__(self):

        self.repository = UsuarioRepository()

        self.password_service = PasswordService()

    def autenticar(
        self,
        cpf: str,
        senha: str,
    ):

        usuario = self.repository.buscar_por_cpf(cpf)

        if usuario is None:
            return False, "CPF não encontrado."

        if not usuario.ativo:
            return False, "Usuário desativado."

        if not usuario.celular_confirmado:
            return (
                False,
                "Confirme o WhatsApp antes de entrar.",
            )

        senha_valida = self.password_service.verificar(
            senha,
            usuario.senha_hash,
        )

        if not senha_valida:
            return False, "Senha incorreta."

        return True, usuario