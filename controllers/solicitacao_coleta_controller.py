from services import SolicitacaoColetaService


class SolicitacaoColetaController:
    """Controller das solicitações de coleta."""

    def __init__(self):
        self.service = SolicitacaoColetaService()

    def listar(self):
        return self.service.listar()

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
        quantidade_sacas: int,
        quantidade_kg: float = 0,
        observacao: str = "",
    ):
        return self.service.criar(
            estabelecimento_id=estabelecimento_id,
            quantidade_sacas=quantidade_sacas,
            quantidade_kg=quantidade_kg,
            observacao=observacao,
        )