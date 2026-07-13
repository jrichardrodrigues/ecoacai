from services import AuthService


class LoginController:
    def __init__(self, auth_service=None):
        self.auth_service = auth_service or AuthService()

    def entrar(
        self,
        cpf: str,
        senha: str,
    ):
        return self.auth_service.autenticar(
            cpf,
            senha,
        )