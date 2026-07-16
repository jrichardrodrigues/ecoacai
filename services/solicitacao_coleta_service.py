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

    def obter_estatisticas(self) -> dict:
        """Retorna os indicadores do Dashboard."""

        return self.repository.obter_estatisticas()

    def listar_ultimas(
            self,
            limite: int = 5,
    ) -> list[dict]:
        """
        Retorna as últimas solicitações.
        """

        return self.repository.listar_ultimas(
            limite
        )

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

    def atualizar(
            self,
            solicitacao: SolicitacaoColeta,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        """Atualiza uma solicitação existente."""

        if solicitacao.id is None:
            return (
                False,
                "Solicitação inválida.",
                None,
            )

        if solicitacao.estabelecimento_id <= 0:
            return (
                False,
                "Selecione um estabelecimento.",
                None,
            )

        if solicitacao.quantidade_sacas <= 0:
            return (
                False,
                "A quantidade de sacas deve ser maior que zero.",
                None,
            )

        if solicitacao.quantidade_kg < 0:
            return (
                False,
                "A quantidade em quilos não pode ser negativa.",
                None,
            )

        try:
            atualizada = self.repository.atualizar(
                solicitacao
            )

        except Exception as erro:
            print(
                "Erro ao atualizar solicitação:",
                erro,
            )

            return (
                False,
                "Não foi possível atualizar a solicitação.",
                None,
            )

        return (
            True,
            "Solicitação atualizada com sucesso.",
            atualizada,
        )

    def excluir(
            self,
            solicitacao_id: int,
    ) -> tuple[bool, str]:
        """Exclui uma solicitação."""

        if solicitacao_id <= 0:
            return (
                False,
                "Solicitação inválida.",
            )

        solicitacao = self.repository.buscar_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return (
                False,
                "Solicitação não encontrada.",
            )

        try:
            sucesso = self.repository.excluir(
                solicitacao_id
            )

        except Exception as erro:
            print(
                "Erro ao excluir solicitação:",
                erro,
            )

            return (
                False,
                "Não foi possível excluir a solicitação.",
            )

        if not sucesso:
            return (
                False,
                "Não foi possível excluir a solicitação.",
            )

        return (
            True,
            "Solicitação excluída com sucesso.",
        )

    def alterar_status(
            self,
            solicitacao_id: int,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        """Avança a solicitação para o próximo status."""

        solicitacao = self.repository.buscar_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return (
                False,
                "Solicitação não encontrada.",
                None,
            )

        agora = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        if solicitacao.status == "PENDENTE":

            solicitacao.status = "AGENDADA"
            solicitacao.data_agendada = agora

        elif solicitacao.status == "AGENDADA":

            solicitacao.status = "EM_COLETA"

        elif solicitacao.status == "EM_COLETA":

            solicitacao.status = "CONCLUIDA"
            solicitacao.data_conclusao = agora

        else:

            solicitacao.status = "PENDENTE"
            solicitacao.data_agendada = None
            solicitacao.data_conclusao = None

        try:

            atualizada = self.repository.alterar_status(
                solicitacao
            )

        except Exception as erro:

            print(
                "Erro ao alterar status:",
                erro,
            )

            return (
                False,
                "Não foi possível alterar o status.",
                None,
            )

        return (
            True,
            "Status atualizado com sucesso.",
            atualizada,
        )