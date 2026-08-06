from __future__ import annotations

from models import SessaoUsuario, Usuario
from services.auth_service import AuthService
from services.sessao_service import SessaoService


class AuthController:
    """Coordena a autenticação e a sessão do usuário."""

    def __init__(
        self,
        auth_service: AuthService | None = None,
        sessao_service: SessaoService | None = None,
    ) -> None:
        self.auth_service = auth_service or AuthService()
        self.sessao_service = sessao_service or SessaoService()

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
        """Autentica o usuário e abre sua sessão."""

        sucesso, mensagem, usuario = (
            self.auth_service.autenticar(
                cpf,
                senha,
            )
        )

        if not sucesso or usuario is None:
            self._usuario_logado = None
            self.sessao_service.encerrar_sessao()

            return False, mensagem

        try:
            sessao = self.sessao_service.abrir_sessao(
                usuario
            )
        except (ValueError, RuntimeError) as erro:
            self._usuario_logado = None
            self.sessao_service.encerrar_sessao()

            return False, str(erro)

        self._usuario_logado = sessao.usuario

        return True, mensagem

    def obter_sessao(self) -> SessaoUsuario | None:
        """Retorna a sessão autenticada atual."""

        return self.sessao_service.obter_sessao()

    def precisa_configurar_organizacao(self) -> bool:
        """Informa se o usuário ainda não possui organização."""

        sessao = self.obter_sessao()

        return (
            sessao is not None
            and not sessao.possui_organizacao
        )

    def sair(self) -> None:
        """Encerra completamente a sessão."""

        self._usuario_logado = None
        self.sessao_service.encerrar_sessao()

    def esta_autenticado(self) -> bool:
        """Informa se existe uma sessão autenticada."""

        return self.sessao_service.esta_autenticado()

    def alterar_senha_por_cpf(
            self,
            cpf: str,
            nova_senha: str,
    ) -> tuple[bool, str]:
        """
        Altera a senha de um usuário a partir do CPF.
        """

        return self.auth_service.alterar_senha_por_cpf(
            cpf=cpf,
            nova_senha=nova_senha,
        )