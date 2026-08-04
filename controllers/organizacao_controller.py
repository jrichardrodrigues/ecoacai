from __future__ import annotations

from models import Organizacao
from services.organizacao_service import OrganizacaoService
from services.sessao_service import SessaoService


class OrganizacaoController:
    """Controla o fluxo de organizações."""

    def __init__(
        self,
        organizacao_service: OrganizacaoService | None = None,
        sessao_service: SessaoService | None = None,
    ) -> None:
        self.organizacao_service = (
            organizacao_service or OrganizacaoService()
        )

        self.sessao_service = (
            sessao_service or SessaoService()
        )

    # =====================================================
    # CADASTRO
    # =====================================================

    def cadastrar_gerador(
            self,
            nome: str,
            documento: str,
            telefone: str = "",
            email: str = "",
    ) -> tuple[bool, str, Organizacao | None]:
        sucesso, mensagem, organizacao = (
            self.organizacao_service.cadastrar_gerador(
                nome=nome,
                documento=documento,
                telefone=telefone,
                email=email,
            )
        )

        if sucesso and organizacao is not None:
            self.sessao_service.atualizar_organizacao(
                organizacao
            )

        return (
            sucesso,
            mensagem,
            organizacao,
        )

    # =====================================================
    # CONSULTAS
    # =====================================================

    def buscar_por_id(
        self,
        organizacao_id: int,
    ) -> Organizacao | None:

        return self.organizacao_service.buscar_por_id(
            organizacao_id
        )

    def listar_geradores(
        self,
    ) -> list[Organizacao]:

        return (
            self.organizacao_service.listar_geradores()
        )

    # =====================================================
    # SESSÃO
    # =====================================================

    def possui_organizacao(
        self,
    ) -> bool:

        return (
            self.sessao_service.possui_organizacao()
        )

    def organizacao_atual(
        self,
    ) -> Organizacao | None:

        return (
            self.sessao_service.obter_organizacao()
        )