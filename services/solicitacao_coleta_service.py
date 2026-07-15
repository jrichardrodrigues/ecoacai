from datetime import datetime

from models import (
    STATUS_PENDENTE,
    SolicitacaoColeta,
)
from repositories import SolicitacaoColetaRepository


class SolicitacaoColetaService:
    """Regras de negócio das solicitações."""

    def __init__(self):
        self.repository = SolicitacaoColetaRepository()

    def listar(self):
        return self.repository.listar()

    def buscar_por_id(
        self,
        solicitacao_id: int,
    ):
        return self.repository.buscar_por_id(
            solicitacao_id
        )

    def criar(
            self,
            estabelecimento_id: int,
            quantidade_sacas: int,
            quantidade_kg: float = 0,
            observacao: str = "",
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        """Valida e cadastra uma solicitação."""

        if estabelecimento_id <= 0:
            return (
                False,
                "Selecione um estabelecimento.",
                None,
            )

        if quantidade_sacas <= 0:
            return (
                False,
                "A quantidade de sacas deve ser maior que zero.",
                None,
            )

        if quantidade_kg < 0:
            return (
                False,
                "A quantidade em quilos não pode ser negativa.",
                None,
            )

        solicitacao = SolicitacaoColeta(
            estabelecimento_id=estabelecimento_id,
            quantidade_sacas=quantidade_sacas,
            quantidade_kg=quantidade_kg,
            observacao=observacao.strip(),
            status=STATUS_PENDENTE,
            data_solicitacao=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        try:
            cadastrada = self.repository.cadastrar(
                solicitacao,
            )
        except Exception as erro:
            print(
                "Erro ao cadastrar solicitação:",
                erro,
            )
            return (
                False,
                "Não foi possível cadastrar a solicitação.",
                None,
            )

        return (
            True,
            "Solicitação cadastrada com sucesso.",
            cadastrada,
        )
