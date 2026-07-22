from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from services.solicitacao_coleta_service import (
    SolicitacaoColetaService,
)


class DashboardController:
    """Centraliza as informações exibidas no Dashboard."""

    def __init__(self) -> None:
        self.solicitacao_service = SolicitacaoColetaService()
        self.estabelecimento_controller = (
            EstabelecimentoController()
        )

    def obter_estatisticas(self) -> dict:
        """Retorna todos os indicadores do Dashboard."""

        estatisticas = (
            self.solicitacao_service.obter_estatisticas()
        )

        estatisticas["total_estabelecimentos"] = (
            self.estabelecimento_controller
            .quantidade_estabelecimentos()
        )

        estatisticas["coletas_hoje"] = (
            self.solicitacao_service
            .contar_agendadas_hoje()
        )

        return estatisticas

    def listar_ultimas(
        self,
        limite: int = 5,
    ) -> list[dict]:
        """Retorna as últimas solicitações."""

        return self.solicitacao_service.listar_ultimas(
            limite,
        )