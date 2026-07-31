from __future__ import annotations

from services.coletas_agendadas_service import (
    ColetasAgendadasService,
)


class ColetasAgendadasController:
    """
    Controller da Agenda de Coletas.

    Responsável por receber as ações da View e
    encaminhá-las ao Service.

    Não contém regras de negócio.
    """

    def __init__(
        self,
        service: ColetasAgendadasService | None = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else ColetasAgendadasService()
        )

    # ======================================================
    # CONSULTAS
    # ======================================================

    def listar(
        self,
        status: str | None = None,
    ):
        return self.service.listar(
            status=status,
        )

    def obter_por_id(
        self,
        solicitacao_id: int,
    ):
        return self.service.obter_por_id(
            solicitacao_id,
        )

    def pesquisar(
        self,
        *,
        data: str | None = None,
        status: str | None = None,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        estabelecimento_id: int | None = None,
    ):
        return self.service.pesquisar(
            data=data,
            status=status,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            estabelecimento_id=estabelecimento_id,
        )

    def agenda_hoje(
        self,
        *,
        status: str | None = None,
    ):
        return self.service.agenda_hoje(
            status=status,
        )

    def agenda_periodo(
        self,
        data_inicial: str,
        data_final: str,
        *,
        status: str | None = None,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
    ):
        return self.service.agenda_periodo(
            data_inicial=data_inicial,
            data_final=data_final,
            status=status,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
        )

    def total_por_status(
        self,
        *,
        data_inicial: str | None = None,
        data_final: str | None = None,
    ):
        return self.service.total_por_status(
            data_inicial=data_inicial,
            data_final=data_final,
        )

    # ======================================================
    # OPERAÇÕES
    # ======================================================

    def agendar(
        self,
        solicitacao_id: int,
        data_hora_agendada: str,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        *,
        janela_minutos: int = 60,
    ):
        return self.service.agendar(
            solicitacao_id=solicitacao_id,
            data_hora_agendada=data_hora_agendada,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            janela_minutos=janela_minutos,
        )

    def reagendar(
        self,
        solicitacao_id: int,
        nova_data_hora: str,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        *,
        janela_minutos: int = 60,
    ):
        return self.service.reagendar(
            solicitacao_id=solicitacao_id,
            nova_data_hora=nova_data_hora,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            janela_minutos=janela_minutos,
        )

    def iniciar_coleta(
        self,
        solicitacao_id: int,
    ):
        return self.service.iniciar_coleta(
            solicitacao_id,
        )

    def concluir_coleta(
        self,
        solicitacao_id: int,
    ):
        return self.service.concluir_coleta(
            solicitacao_id,
        )

    def cancelar_coleta(
        self,
        solicitacao_id: int,
    ):
        return self.service.cancelar_coleta(
            solicitacao_id,
        )

    # ======================================================
    # DISPONIBILIDADE
    # ======================================================

    def motorista_disponivel(
        self,
        motorista_id: int,
        data_hora_agendada: str,
        *,
        solicitacao_ignorada_id: int | None = None,
        janela_minutos: int = 60,
    ):
        return self.service.motorista_disponivel(
            motorista_id=motorista_id,
            data_hora_agendada=data_hora_agendada,
            solicitacao_ignorada_id=solicitacao_ignorada_id,
            janela_minutos=janela_minutos,
        )

    def veiculo_disponivel(
        self,
        veiculo_id: int,
        data_hora_agendada: str,
        *,
        solicitacao_ignorada_id: int | None = None,
        janela_minutos: int = 60,
    ):
        return self.service.veiculo_disponivel(
            veiculo_id=veiculo_id,
            data_hora_agendada=data_hora_agendada,
            solicitacao_ignorada_id=solicitacao_ignorada_id,
            janela_minutos=janela_minutos,
        )