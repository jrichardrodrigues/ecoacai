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

    def obter_estatisticas(
            self,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> dict:
        """Retorna todos os indicadores do Dashboard."""

        estatisticas = (
            self.solicitacao_service.obter_estatisticas(
                data_inicial=data_inicial,
                data_final=data_final,
            )
        )

        if data_inicial or data_final:
            estatisticas["total_estabelecimentos"] = (
                estatisticas.get(
                    "estabelecimentos_periodo",
                    0,
                )
            )
        else:
            estatisticas["total_estabelecimentos"] = (
                self.estabelecimento_controller
                .quantidade_estabelecimentos()
            )

        estatisticas["tempo_medio_atendimento"] = (
            self.solicitacao_service.obter_tempo_medio_atendimento(
                data_inicial=data_inicial,
                data_final=data_final,
            )
        )

        estatisticas["tempo_medio_coleta"] = (
            self.solicitacao_service.obter_tempo_medio_coleta(
                data_inicial=data_inicial,
                data_final=data_final,
            )
        )

        estatisticas["tempo_medio_espera"] = (
            self.solicitacao_service.obter_tempo_medio_espera(
                data_inicial=data_inicial,
                data_final=data_final,
            )
        )

        estatisticas["taxa_cumprimento_agendamento"] = (
            self.solicitacao_service.obter_taxa_cumprimento_agendamento(
                data_inicial=data_inicial,
                data_final=data_final,
            )
        )

        estatisticas["eficiencia_volume_coletado"] = (
            self.solicitacao_service.obter_eficiencia_volume_coletado(
                data_inicial=data_inicial,
                data_final=data_final,
            )
        )

        estatisticas["evolucao_solicitacoes"] = (
            self.solicitacao_service.obter_evolucao_solicitacoes(
                data_inicial=data_inicial,
                data_final=data_final,
            )
        )

        estatisticas["coletas_hoje"] = (
            self.solicitacao_service
            .contar_agendadas_hoje()
        )

        return estatisticas

    def listar_ultimas(
            self,
            limite: int = 5,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> list[dict]:
        """Retorna as últimas solicitações."""

        return self.solicitacao_service.listar_ultimas(
            limite=limite,
            data_inicial=data_inicial,
            data_final=data_final,
        )