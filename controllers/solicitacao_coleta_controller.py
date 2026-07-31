from services import SolicitacaoColetaService


class SolicitacaoColetaController:
    """Controller das solicitações de coleta."""

    def __init__(self):
        self.service = SolicitacaoColetaService()

    def listar(self):
        return self.service.listar()

    def obter_estatisticas(self):
        """Retorna os indicadores do Dashboard."""

        return self.service.obter_estatisticas()

    def listar_ultimas(
            self,
            limite: int = 5,
    ):
        """
        Retorna as últimas solicitações.
        """

        return self.service.listar_ultimas(
            limite
        )

    def buscar_por_id(
        self,
        solicitacao_id: int,
    ):
        return self.service.buscar_por_id(
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
    ):
        return self.service.criar(
            estabelecimento_id=estabelecimento_id,
            quantidade_sacas_prevista=quantidade_sacas_prevista,
            quantidade_kg_previsto=quantidade_kg_previsto,
            data_hora_agendada=data_hora_agendada,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            observacao_cliente=observacao_cliente,
        )

    def atualizar(
            self,
            solicitacao,
    ):
        """Atualiza uma solicitação."""

        return self.service.atualizar(
            solicitacao
        )

    def excluir(
            self,
            solicitacao_id: int,
    ):
        """Exclui uma solicitação."""

        return self.service.excluir(
            solicitacao_id
        )

    def alterar_status(
            self,
            solicitacao_id: int,
    ):
        """Altera o status da solicitação."""

        return self.service.alterar_status(
            solicitacao_id
        )

    def listar_com_estabelecimento(self):
        """Lista as solicitações juntamente com o nome do estabelecimento."""

        return self.service.listar_com_estabelecimento()