from __future__ import annotations

import re

from models import Organizacao
from repositories import OrganizacaoRepository
from services.sessao_service import SessaoService


class OrganizacaoService:
    """
    Regras de negócio das organizações da Plataforma ZELURBIS.
    """

    TIPO_GERADOR = "GERADOR"

    def __init__(
        self,
        repository: OrganizacaoRepository | None = None,
        sessao_service: SessaoService | None = None,
    ) -> None:

        self.repository = repository or OrganizacaoRepository()
        self.sessao_service = sessao_service or SessaoService()

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

        nome = self._normalizar(nome)
        documento = self._somente_digitos(documento)
        telefone = self._somente_digitos(telefone)
        email = email.strip().lower()

        if not nome:
            return (
                False,
                "Informe o nome da organização.",
                None,
            )

        if len(nome) < 3:
            return (
                False,
                "Nome da organização inválido.",
                None,
            )

        if not documento:
            return (
                False,
                "Informe o CPF ou CNPJ.",
                None,
            )

        if self.repository.documento_existe(documento):
            return (
                False,
                "Já existe uma organização com este documento.",
                None,
            )

        if email:

            if not self._validar_email(email):
                return (
                    False,
                    "E-mail inválido.",
                    None,
                )

        organizacao = Organizacao(
            tipo=self.TIPO_GERADOR,
            nome=nome,
            documento=documento,
            telefone=telefone,
            email=email,
            ativo=True,
        )

        try:

            organizacao = self.repository.cadastrar(
                organizacao
            )

            self.sessao_service.atualizar_organizacao(
                organizacao
            )

        except Exception as erro:

            return (
                False,
                str(erro),
                None,
            )

        return (
            True,
            "Organização cadastrada com sucesso.",
            organizacao,
        )

    # =====================================================
    # CONSULTAS
    # =====================================================

    def buscar_por_id(
        self,
        organizacao_id: int,
    ) -> Organizacao | None:

        return self.repository.buscar_por_id(
            organizacao_id
        )

    def listar_geradores(
        self,
    ) -> list[Organizacao]:

        return self.repository.listar_por_tipo(
            self.TIPO_GERADOR
        )

    # =====================================================
    # VALIDAÇÕES
    # =====================================================

    @staticmethod
    def _normalizar(
        texto: str,
    ) -> str:

        return " ".join(
            str(texto or "").strip().split()
        )

    @staticmethod
    def _somente_digitos(
        texto: str,
    ) -> str:

        return "".join(
            c
            for c in str(texto or "")
            if c.isdigit()
        )

    @staticmethod
    def _validar_email(
        email: str,
    ) -> bool:

        padrao = (
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        return re.fullmatch(
            padrao,
            email,
        ) is not None