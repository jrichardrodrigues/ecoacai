from datetime import datetime

from config import StatusSolicitacao

from models import SolicitacaoColeta
from repositories import SolicitacaoColetaRepository


class SolicitacaoColetaService:
    """Regras de negócio das solicitações."""

    def __init__(self):
        self.repository = SolicitacaoColetaRepository()

    def _erro_operacao(
            self,
            operacao: str,
            erro: Exception,
    ) -> tuple:
        """Padroniza o tratamento de erros inesperados."""

        print(
            f"Erro ao {operacao} solicitação:",
            erro,
        )

        return (
            False,
            f"Não foi possível {operacao} a solicitação.",
            None,
        )

    def _validar_solicitacao(
            self,
            estabelecimento_id: int,
            quantidade_sacas_prevista: int,
            quantidade_kg_previsto: float,
    ) -> tuple[bool, str]:
        """Valida os dados básicos de uma solicitação."""

        if estabelecimento_id <= 0:
            return (
                False,
                "Selecione um estabelecimento.",
            )

        if quantidade_sacas_prevista <= 0:
            return (
                False,
                "A quantidade de sacas deve ser maior que zero.",
            )

        if quantidade_kg_previsto < 0:
            return (
                False,
                "A quantidade em quilos não pode ser negativa.",
            )

        return True, ""

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
            quantidade_sacas_prevista: int,
            quantidade_kg_previsto: float = 0,
            data_hora_agendada: str = "",
            motorista_id: int | None = None,
            veiculo_id: int | None = None,
            observacao_cliente: str = "",
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        """Valida e cadastra uma solicitação."""

        valido, mensagem = self._validar_solicitacao(
            estabelecimento_id,
            quantidade_sacas_prevista,
            quantidade_kg_previsto,
        )

        if not valido:
            return (
                False,
                mensagem,
                None,
            )

        solicitacao = SolicitacaoColeta(
            estabelecimento_id=estabelecimento_id,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            quantidade_sacas_prevista=quantidade_sacas_prevista,
            quantidade_kg_previsto=quantidade_kg_previsto,
            data_hora_agendada=(
                    data_hora_agendada or ""
            ).strip(),
            observacao_cliente=(
                    observacao_cliente or ""
            ).strip(),
            status = StatusSolicitacao.PENDENTE,
            data_solicitacao=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        try:
            cadastrada = self.repository.cadastrar(
                solicitacao,
            )

        except Exception as erro:
            return self._erro_operacao(
                "cadastrar",
                erro,
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

        valido, mensagem = self._validar_solicitacao(
            solicitacao.estabelecimento_id,
            solicitacao.quantidade_sacas_prevista,
            solicitacao.quantidade_kg_previsto,
        )

        if not valido:
            return (
                False,
                mensagem,
                None,
            )

        if solicitacao.quantidade_kg_previsto < 0:
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

            return self._erro_operacao(

                "atualizar",

                erro,

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

        if solicitacao.status == StatusSolicitacao.PENDENTE:
            solicitacao.status = StatusSolicitacao.AGENDADA
            solicitacao.data_hora_agendada = agora

        elif solicitacao.status == StatusSolicitacao.AGENDADA:
            solicitacao.status = StatusSolicitacao.EM_DESLOCAMENTO
            solicitacao.data_hora_inicio = agora

        elif solicitacao.status == StatusSolicitacao.EM_DESLOCAMENTO:
            solicitacao.status = StatusSolicitacao.EM_COLETA
            solicitacao.data_hora_chegada = agora

        elif solicitacao.status == StatusSolicitacao.EM_COLETA:
            solicitacao.status = StatusSolicitacao.CONCLUIDA
            solicitacao.data_hora_conclusao = agora

        else:
            return (
                False,
                "A solicitação já foi concluída ou não permite nova alteração de status.",
                None,
            )

        try:
            atualizada = self.repository.alterar_status(
                solicitacao
            )

        except Exception as erro:
            return self._erro_operacao(
                "alterar o status de",
                erro,
            )

        return (
            True,
            "Status atualizado com sucesso.",
            atualizada,
        )

    def contar_agendadas_hoje(self) -> int:
        """Retorna a quantidade de coletas agendadas para hoje."""

        return self.repository.contar_agendadas_hoje()

    def listar_com_estabelecimento(self):
        """Lista as solicitações juntamente com o nome do estabelecimento."""

        return self.repository.listar_com_estabelecimento()