"""
controllers/usuario_controller.py

Controller responsável pela comunicação entre
a View e o UsuarioService.
"""

from models import Usuario
from services.usuario_service import UsuarioService


class UsuarioController:
    """Controller do módulo de usuários."""

    def __init__(self) -> None:
        self.usuario_service = UsuarioService()

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar_usuario(
        self,
        dados: dict,
    ) -> tuple[bool, str, Usuario | None]:
        """
        Cadastra um novo usuário.

        Retorna:
            (sucesso, mensagem, usuario)
        """

        return self.usuario_service.cadastrar(dados)

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        usuario_id: int,
    ) -> Usuario | None:
        """Busca um usuário pelo ID."""

        return self.usuario_service.buscar_por_id(
            usuario_id
        )

    def buscar_por_cpf(
        self,
        cpf: str,
    ) -> Usuario | None:
        """Busca um usuário pelo CPF."""

        return self.usuario_service.buscar_por_cpf(
            cpf
        )

    def listar(
        self,
        somente_ativos: bool = True,
    ) -> list[Usuario]:
        """Lista os usuários cadastrados."""

        return self.usuario_service.listar(
            somente_ativos=somente_ativos
        )

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    def cpf_existe(
        self,
        cpf: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se o CPF já existe."""

        return self.usuario_service.cpf_existe(
            cpf,
            ignorar_id,
        )

    def celular_existe(
        self,
        celular: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se o celular já existe."""

        return self.usuario_service.celular_existe(
            celular,
            ignorar_id,
        )