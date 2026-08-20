from __future__ import annotations

from datetime import datetime
from typing import Any

from repositories.agenda_repository import AgendaRepository
from repositories.repository_result import RepositoryResult
from config.constants import StatusColeta


class ColetasAgendadasService:
    """
    Serviço responsável pelas regras de negócio da agenda de coletas.

    Faz a comunicação entre o Controller e o AgendaRepository,
    validando os dados e retornando resultados padronizados.
    """

    _FORMATO_DATA = "%Y-%m-%d"
    _FORMATO_DATA_HORA = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        repository: AgendaRepository | None = None,
    ) -> None:
        self.repository = repository or AgendaRepository()

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def listar(
        self,
        status: str | None = None,
    ) -> RepositoryResult:
        """Lista as solicitações disponíveis na agenda."""

        try:
            registros = self.repository.listar(
                status=status,
            )

            return RepositoryResult(
                sucesso=True,
                mensagem=self._mensagem_quantidade(
                    registros,
                    singular="coleta encontrada.",
                    plural="coletas encontradas.",
                ),
                dados=registros,
            )

        except ValueError as erro:
            return self._falha(str(erro))

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível listar as coletas.",
                erro,
            )

    def obter_por_id(
        self,
        solicitacao_id: int,
    ) -> RepositoryResult:
        """Obtém uma solicitação pelo identificador."""

        if not self._id_valido(solicitacao_id):
            return self._falha(
                "Identificador da solicitação inválido."
            )

        try:
            registro = self.repository.obter_por_id(
                solicitacao_id
            )

            if registro is None:
                return self._falha(
                    "Solicitação não encontrada."
                )

            return RepositoryResult(
                sucesso=True,
                dados=registro,
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível consultar a solicitação.",
                erro,
            )

    def pesquisar(
        self,
        *,
        data: str | None = None,
        status: str | None = None,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        estabelecimento_id: int | None = None,
    ) -> RepositoryResult:
        """Pesquisa coletas combinando filtros opcionais."""

        if data:
            validacao_data = self._validar_data(data)

            if validacao_data.falhou:
                return validacao_data

        validacao_ids = self._validar_ids_opcionais(
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            estabelecimento_id=estabelecimento_id,
        )

        if validacao_ids.falhou:
            return validacao_ids

        try:
            registros = self.repository.pesquisar(
                data=data,
                status=status,
                motorista_id=motorista_id,
                veiculo_id=veiculo_id,
                estabelecimento_id=estabelecimento_id,
            )

            return RepositoryResult(
                sucesso=True,
                mensagem=self._mensagem_quantidade(
                    registros,
                    singular="coleta encontrada.",
                    plural="coletas encontradas.",
                ),
                dados=registros,
            )

        except ValueError as erro:
            return self._falha(str(erro))

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível pesquisar as coletas.",
                erro,
            )

    def agenda_hoje(
        self,
        *,
        status: str | None = None,
    ) -> RepositoryResult:
        """Retorna as coletas agendadas para a data atual."""

        try:
            registros = self.repository.agenda_hoje(
                status=status,
            )

            return RepositoryResult(
                sucesso=True,
                mensagem=self._mensagem_quantidade(
                    registros,
                    singular="coleta agendada para hoje.",
                    plural="coletas agendadas para hoje.",
                ),
                dados=registros,
            )

        except ValueError as erro:
            return self._falha(str(erro))

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível consultar a agenda de hoje.",
                erro,
            )

    def agenda_periodo(
        self,
        data_inicial: str,
        data_final: str,
        *,
        status: str | None = None,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
    ) -> RepositoryResult:
        """Retorna as coletas agendadas dentro de um período."""

        validacao_periodo = self._validar_periodo(
            data_inicial,
            data_final,
        )

        if validacao_periodo.falhou:
            return validacao_periodo

        validacao_ids = self._validar_ids_opcionais(
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
        )

        if validacao_ids.falhou:
            return validacao_ids

        try:
            registros = self.repository.agenda_periodo(
                data_inicial=data_inicial.strip(),
                data_final=data_final.strip(),
                status=status,
                motorista_id=motorista_id,
                veiculo_id=veiculo_id,
            )

            return RepositoryResult(
                sucesso=True,
                mensagem=self._mensagem_quantidade(
                    registros,
                    singular="coleta encontrada no período.",
                    plural="coletas encontradas no período.",
                ),
                dados=registros,
            )

        except ValueError as erro:
            return self._falha(str(erro))

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível consultar a agenda do período.",
                erro,
            )

    def total_por_status(
        self,
        *,
        data_inicial: str | None = None,
        data_final: str | None = None,
    ) -> RepositoryResult:
        """Retorna os totais das solicitações agrupados por status."""

        if data_inicial or data_final:
            validacao_datas = self._validar_periodo_opcional(
                data_inicial=data_inicial,
                data_final=data_final,
            )

            if validacao_datas.falhou:
                return validacao_datas

        try:
            totais = self.repository.total_por_status(
                data_inicial=data_inicial,
                data_final=data_final,
            )

            return RepositoryResult(
                sucesso=True,
                dados=totais,
            )

        except ValueError as erro:
            return self._falha(str(erro))

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível obter os indicadores da agenda.",
                erro,
            )

    # ==========================================================
    # OPERAÇÕES
    # ==========================================================

    def agendar(
        self,
        solicitacao_id: int,
        data_hora_agendada: str,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        *,
        janela_minutos: int = 60,
    ) -> RepositoryResult:
        """
        Agenda uma solicitação.

        Antes de salvar, verifica a existência da solicitação,
        seu status e a disponibilidade do motorista e do veículo.
        """

        validacao = self._validar_operacao_agendamento(
            solicitacao_id=solicitacao_id,
            data_hora_agendada=data_hora_agendada,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            janela_minutos=janela_minutos,
        )

        if validacao.falhou:
            return validacao

        solicitacao = self.repository.obter_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return self._falha(
                "Solicitação não encontrada."
            )

        status_atual = self._normalizar_texto(
            solicitacao.get("status")
        )

        if status_atual not in {
            StatusColeta.EM_ANALISE,
            StatusColeta.AGENDADA,
        }:
            return self._falha(
                "Somente solicitações em análise ou agendadas "
                "podem ser agendadas."
            )

        disponibilidade = self._validar_disponibilidade(
            data_hora_agendada=data_hora_agendada,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            janela_minutos=janela_minutos,
        )

        if disponibilidade.falhou:
            return disponibilidade

        try:
            sucesso = self.repository.agendar(
                solicitacao_id=solicitacao_id,
                data_hora_agendada=data_hora_agendada.strip(),
                motorista_id=motorista_id,
                veiculo_id=veiculo_id,
            )

            if not sucesso:
                return self._falha(
                    "Não foi possível agendar a coleta."
                )

            coleta_atualizada = self.repository.obter_por_id(
                solicitacao_id
            )

            return RepositoryResult(
                sucesso=True,
                mensagem="Coleta agendada com sucesso.",
                dados=coleta_atualizada,
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível agendar a coleta.",
                erro,
            )

    def reagendar(
        self,
        solicitacao_id: int,
        nova_data_hora: str,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        *,
        janela_minutos: int = 60,
    ) -> RepositoryResult:
        """Reagenda uma coleta que esteja com status AGENDADA."""

        validacao = self._validar_operacao_agendamento(
            solicitacao_id=solicitacao_id,
            data_hora_agendada=nova_data_hora,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            janela_minutos=janela_minutos,
        )

        if validacao.falhou:
            return validacao

        solicitacao = self.repository.obter_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return self._falha(
                "Solicitação não encontrada."
            )

        if self._normalizar_texto(
                solicitacao.get("status")
        ) != StatusColeta.AGENDADA:
            return self._falha(
                "Somente coletas agendadas podem ser reagendadas."
            )

        motorista_final = (
            motorista_id
            if motorista_id is not None
            else solicitacao.get("motorista_id")
        )

        veiculo_final = (
            veiculo_id
            if veiculo_id is not None
            else solicitacao.get("veiculo_id")
        )

        disponibilidade = self._validar_disponibilidade(
            data_hora_agendada=nova_data_hora,
            motorista_id=motorista_final,
            veiculo_id=veiculo_final,
            solicitacao_ignorada_id=solicitacao_id,
            janela_minutos=janela_minutos,
        )

        if disponibilidade.falhou:
            return disponibilidade

        try:
            sucesso = self.repository.reagendar(
                solicitacao_id=solicitacao_id,
                nova_data_hora=nova_data_hora.strip(),
                motorista_id=motorista_id,
                veiculo_id=veiculo_id,
            )

            if not sucesso:
                return self._falha(
                    "Não foi possível reagendar a coleta."
                )

            coleta_atualizada = self.repository.obter_por_id(
                solicitacao_id
            )

            return RepositoryResult(
                sucesso=True,
                mensagem="Coleta reagendada com sucesso.",
                dados=coleta_atualizada,
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível reagendar a coleta.",
                erro,
            )

    def iniciar_coleta(
        self,
        solicitacao_id: int,
    ) -> RepositoryResult:
        """Inicia uma coleta que esteja agendada."""

        validacao = self._validar_status_atual(
            solicitacao_id=solicitacao_id,
            status_esperado=StatusColeta.AGENDADA,
            mensagem=(
                "Somente coletas agendadas podem ser iniciadas."
            ),
        )

        if validacao.falhou:
            return validacao

        try:
            sucesso = self.repository.iniciar_coleta(
                solicitacao_id
            )

            if not sucesso:
                return self._falha(
                    "Não foi possível iniciar a coleta."
                )

            return RepositoryResult(
                sucesso=True,
                mensagem="Coleta iniciada com sucesso.",
                dados=self.repository.obter_por_id(
                    solicitacao_id
                ),
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível iniciar a coleta.",
                erro,
            )

    def registrar_chegada(
            self,
            solicitacao_id: int,
    ) -> RepositoryResult:
        """Registra a chegada da equipe ao local da coleta."""

        validacao = self._validar_status_atual(
            solicitacao_id=solicitacao_id,
            status_esperado=StatusColeta.EM_COLETA,
            mensagem=(
                "Somente coletas em andamento podem registrar chegada."
            ),
        )

        if validacao.falhou:
            return validacao

        try:
            sucesso = self.repository.registrar_chegada(
                solicitacao_id
            )

            if not sucesso:
                return self._falha(
                    "Não foi possível registrar a chegada."
                )

            return RepositoryResult(
                sucesso=True,
                mensagem="Chegada registrada com sucesso.",
                dados=self.repository.obter_por_id(
                    solicitacao_id
                ),
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível registrar a chegada.",
                erro,
            )

    def concluir_coleta(
            self,
            solicitacao_id: int,
            quantidade_coletada: int,
            peso_coletado_kg: float,
            observacao_operacional: str = "",
    ) -> RepositoryResult:
        """Conclui uma coleta que esteja em andamento."""

        validacao = self._validar_status_atual(
            solicitacao_id=solicitacao_id,
            status_esperado=StatusColeta.EM_COLETA,
            mensagem=(
                "Somente coletas em andamento podem ser concluídas."
            ),
        )

        if validacao.falhou:
            return validacao

        if quantidade_coletada <= 0:
            return self._falha(
                "Informe a quantidade efetivamente coletada."
            )

        if peso_coletado_kg <= 0:
            return self._falha(
                "Informe o peso efetivamente coletado."
            )

        observacao_operacional = str(
            observacao_operacional or ""
        ).strip()

        try:
            sucesso = self.repository.concluir_coleta(
                solicitacao_id=solicitacao_id,
                quantidade_coletada=quantidade_coletada,
                peso_coletado_kg=peso_coletado_kg,
                observacao_operacional=observacao_operacional,
            )

            if not sucesso:
                return self._falha(
                    "Não foi possível concluir a coleta."
                )

            return RepositoryResult(
                sucesso=True,
                mensagem="Coleta concluída com sucesso.",
                dados=self.repository.obter_por_id(
                    solicitacao_id
                ),
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível concluir a coleta.",
                erro,
            )

    def cancelar_coleta(
            self,
            solicitacao_id: int,
            motivo: str,
    ) -> RepositoryResult:
        """Cancela uma solicitação e registra o motivo."""

        if not self._id_valido(solicitacao_id):
            return self._falha(
                "Identificador da solicitação inválido."
            )

        solicitacao = self.repository.obter_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return self._falha(
                "Solicitação não encontrada."
            )

        status_atual = self._normalizar_texto(
            solicitacao.get("status")
        )

        if status_atual not in {
            StatusColeta.SOLICITADA,
            StatusColeta.EM_ANALISE,
            StatusColeta.AGENDADA,
        }:
            return self._falha(
                "Somente solicitações solicitadas, em análise "
                "ou agendadas podem ser canceladas."
            )

        motivo_normalizado = str(
            motivo or ""
        ).strip()

        if not motivo_normalizado:
            return self._falha(
                "Informe o motivo do cancelamento."
            )

        try:
            sucesso = self.repository.cancelar_coleta(
                solicitacao_id=solicitacao_id,
                motivo=motivo_normalizado,
            )

            if not sucesso:
                return self._falha(
                    "Não foi possível cancelar a coleta."
                )

            return RepositoryResult(
                sucesso=True,
                mensagem="Coleta cancelada com sucesso.",
                dados=self.repository.obter_por_id(
                    solicitacao_id
                ),
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível cancelar a coleta.",
                erro,
            )

    def recusar_coleta(
            self,
            solicitacao_id: int,
            motivo: str,
    ) -> RepositoryResult:
        """Recusa uma solicitação em análise e registra o motivo."""

        if not self._id_valido(solicitacao_id):
            return self._falha(
                "Identificador da solicitação inválido."
            )

        solicitacao = self.repository.obter_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return self._falha(
                "Solicitação não encontrada."
            )

        status_atual = self._normalizar_texto(
            solicitacao.get("status")
        )

        if status_atual != StatusColeta.EM_ANALISE:
            return self._falha(
                "Somente solicitações em análise podem ser recusadas."
            )

        motivo_normalizado = str(
            motivo or ""
        ).strip()

        if not motivo_normalizado:
            return self._falha(
                "Informe o motivo da recusa."
            )

        try:
            sucesso = self.repository.recusar_coleta(
                solicitacao_id=solicitacao_id,
                motivo=motivo_normalizado,
            )

            if not sucesso:
                return self._falha(
                    "Não foi possível recusar a solicitação."
                )

            return RepositoryResult(
                sucesso=True,
                mensagem="Solicitação recusada com sucesso.",
                dados=self.repository.obter_por_id(
                    solicitacao_id
                ),
            )

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível recusar a solicitação.",
                erro,
            )

    # ==========================================================
    # DISPONIBILIDADE
    # ==========================================================

    def motorista_disponivel(
        self,
        motorista_id: int,
        data_hora_agendada: str,
        *,
        solicitacao_ignorada_id: int | None = None,
        janela_minutos: int = 60,
    ) -> RepositoryResult:
        """Verifica a disponibilidade de um motorista."""

        if not self._id_valido(motorista_id):
            return self._falha(
                "Identificador do motorista inválido."
            )

        validacao_data = self._validar_data_hora(
            data_hora_agendada
        )

        if validacao_data.falhou:
            return validacao_data

        if janela_minutos < 0:
            return self._falha(
                "A janela de conflito não pode ser negativa."
            )

        try:
            resultado = self.repository.motorista_disponivel(
                motorista_id=motorista_id,
                data_hora_agendada=data_hora_agendada.strip(),
                solicitacao_ignorada_id=solicitacao_ignorada_id,
                janela_minutos=janela_minutos,
            )

            disponivel = bool(
                resultado.get("disponivel")
            )

            return RepositoryResult(
                sucesso=disponivel,
                mensagem=str(
                    resultado.get(
                        "mensagem",
                        "Motorista disponível."
                        if disponivel
                        else "Motorista indisponível.",
                    )
                ),
                dados=resultado,
            )

        except ValueError as erro:
            return self._falha(str(erro))

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível verificar o motorista.",
                erro,
            )

    def veiculo_disponivel(
        self,
        veiculo_id: int,
        data_hora_agendada: str,
        *,
        solicitacao_ignorada_id: int | None = None,
        janela_minutos: int = 60,
    ) -> RepositoryResult:
        """Verifica a disponibilidade de um veículo."""

        if not self._id_valido(veiculo_id):
            return self._falha(
                "Identificador do veículo inválido."
            )

        validacao_data = self._validar_data_hora(
            data_hora_agendada
        )

        if validacao_data.falhou:
            return validacao_data

        if janela_minutos < 0:
            return self._falha(
                "A janela de conflito não pode ser negativa."
            )

        try:
            resultado = self.repository.veiculo_disponivel(
                veiculo_id=veiculo_id,
                data_hora_agendada=data_hora_agendada.strip(),
                solicitacao_ignorada_id=solicitacao_ignorada_id,
                janela_minutos=janela_minutos,
            )

            disponivel = bool(
                resultado.get("disponivel")
            )

            return RepositoryResult(
                sucesso=disponivel,
                mensagem=str(
                    resultado.get(
                        "mensagem",
                        "Veículo disponível."
                        if disponivel
                        else "Veículo indisponível.",
                    )
                ),
                dados=resultado,
            )

        except ValueError as erro:
            return self._falha(str(erro))

        except Exception as erro:
            return self._erro_inesperado(
                "Não foi possível verificar o veículo.",
                erro,
            )

    # ==========================================================
    # MÉTODOS INTERNOS
    # ==========================================================

    def _validar_operacao_agendamento(
        self,
        *,
        solicitacao_id: int,
        data_hora_agendada: str,
        motorista_id: int | None,
        veiculo_id: int | None,
        janela_minutos: int,
    ) -> RepositoryResult:
        """Valida os dados básicos de agendamento."""

        if not self._id_valido(solicitacao_id):
            return self._falha(
                "Identificador da solicitação inválido."
            )

        validacao_data = self._validar_data_hora(
            data_hora_agendada,
            exigir_futura=True,
        )

        if validacao_data.falhou:
            return validacao_data

        validacao_ids = self._validar_ids_opcionais(
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
        )

        if validacao_ids.falhou:
            return validacao_ids

        if janela_minutos < 0:
            return self._falha(
                "A janela de conflito não pode ser negativa."
            )

        return self._sucesso()

    def _validar_disponibilidade(
        self,
        *,
        data_hora_agendada: str,
        motorista_id: int | None,
        veiculo_id: int | None,
        solicitacao_ignorada_id: int | None = None,
        janela_minutos: int = 60,
    ) -> RepositoryResult:
        """Valida os conflitos de motorista e veículo."""

        if motorista_id is not None:
            resultado_motorista = self.motorista_disponivel(
                motorista_id=motorista_id,
                data_hora_agendada=data_hora_agendada,
                solicitacao_ignorada_id=solicitacao_ignorada_id,
                janela_minutos=janela_minutos,
            )

            if resultado_motorista.falhou:
                return resultado_motorista

        if veiculo_id is not None:
            resultado_veiculo = self.veiculo_disponivel(
                veiculo_id=veiculo_id,
                data_hora_agendada=data_hora_agendada,
                solicitacao_ignorada_id=solicitacao_ignorada_id,
                janela_minutos=janela_minutos,
            )

            if resultado_veiculo.falhou:
                return resultado_veiculo

        return self._sucesso()

    def _validar_status_atual(
        self,
        *,
        solicitacao_id: int,
        status_esperado: str,
        mensagem: str,
    ) -> RepositoryResult:
        """Verifica se a solicitação está no status esperado."""

        if not self._id_valido(solicitacao_id):
            return self._falha(
                "Identificador da solicitação inválido."
            )

        solicitacao = self.repository.obter_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return self._falha(
                "Solicitação não encontrada."
            )

        status_atual = self._normalizar_texto(
            solicitacao.get("status")
        )

        if status_atual != status_esperado:
            return self._falha(mensagem)

        return self._sucesso(
            dados=solicitacao
        )

    def _validar_data(
        self,
        valor: str,
    ) -> RepositoryResult:
        """Valida uma data no formato AAAA-MM-DD."""

        valor_normalizado = valor.strip()

        if not valor_normalizado:
            return self._falha(
                "Data não informada."
            )

        try:
            datetime.strptime(
                valor_normalizado,
                self._FORMATO_DATA,
            )

        except ValueError:
            return self._falha(
                "Data inválida. Utilize o formato AAAA-MM-DD."
            )

        return self._sucesso(
            dados=valor_normalizado
        )

    def _validar_data_hora(
        self,
        valor: str,
        *,
        exigir_futura: bool = False,
    ) -> RepositoryResult:
        """Valida uma data e hora no formato SQLite."""

        valor_normalizado = valor.strip()

        if not valor_normalizado:
            return self._falha(
                "Data e hora não informadas."
            )

        try:
            data_hora = datetime.strptime(
                valor_normalizado,
                self._FORMATO_DATA_HORA,
            )

        except ValueError:
            return self._falha(
                "Data e hora inválidas. Utilize o formato "
                "AAAA-MM-DD HH:MM:SS."
            )

        if exigir_futura and data_hora <= datetime.now():
            return self._falha(
                "A data e a hora do agendamento devem ser futuras."
            )

        return self._sucesso(
            dados=data_hora
        )

    def _validar_periodo(
        self,
        data_inicial: str,
        data_final: str,
    ) -> RepositoryResult:
        """Valida um período obrigatório."""

        inicio = self._validar_data(
            data_inicial
        )

        if inicio.falhou:
            return RepositoryResult(
                sucesso=False,
                mensagem=f"Data inicial: {inicio.mensagem}",
            )

        fim = self._validar_data(
            data_final
        )

        if fim.falhou:
            return RepositoryResult(
                sucesso=False,
                mensagem=f"Data final: {fim.mensagem}",
            )

        inicio_data = datetime.strptime(
            data_inicial.strip(),
            self._FORMATO_DATA,
        )

        fim_data = datetime.strptime(
            data_final.strip(),
            self._FORMATO_DATA,
        )

        if inicio_data > fim_data:
            return self._falha(
                "A data inicial não pode ser maior que a data final."
            )

        return self._sucesso()

    def _validar_periodo_opcional(
        self,
        *,
        data_inicial: str | None,
        data_final: str | None,
    ) -> RepositoryResult:
        """Valida um período cujas datas são opcionais."""

        if data_inicial:
            inicio = self._validar_data(
                data_inicial
            )

            if inicio.falhou:
                return RepositoryResult(
                    sucesso=False,
                    mensagem=f"Data inicial: {inicio.mensagem}",
                )

        if data_final:
            fim = self._validar_data(
                data_final
            )

            if fim.falhou:
                return RepositoryResult(
                    sucesso=False,
                    mensagem=f"Data final: {fim.mensagem}",
                )

        if data_inicial and data_final:
            inicio_data = datetime.strptime(
                data_inicial.strip(),
                self._FORMATO_DATA,
            )

            fim_data = datetime.strptime(
                data_final.strip(),
                self._FORMATO_DATA,
            )

            if inicio_data > fim_data:
                return self._falha(
                    "A data inicial não pode ser maior "
                    "que a data final."
                )

        return self._sucesso()

    def _validar_ids_opcionais(
        self,
        *,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        estabelecimento_id: int | None = None,
    ) -> RepositoryResult:
        """Valida identificadores opcionais."""

        campos = {
            "motorista": motorista_id,
            "veículo": veiculo_id,
            "estabelecimento": estabelecimento_id,
        }

        for nome, identificador in campos.items():
            if (
                identificador is not None
                and not self._id_valido(identificador)
            ):
                return self._falha(
                    f"Identificador do {nome} inválido."
                )

        return self._sucesso()

    @staticmethod
    def _id_valido(
        identificador: Any,
    ) -> bool:
        """Verifica se um identificador é inteiro e positivo."""

        return (
            isinstance(identificador, int)
            and not isinstance(identificador, bool)
            and identificador > 0
        )

    @staticmethod
    def _normalizar_texto(
        valor: Any,
    ) -> str:
        """Normaliza um valor textual para comparação."""

        if valor is None:
            return ""

        return str(valor).strip().upper()

    @staticmethod
    def _mensagem_quantidade(
        registros: list[dict],
        *,
        singular: str,
        plural: str,
    ) -> str:
        """Cria uma mensagem de acordo com a quantidade retornada."""

        quantidade = len(registros)

        if quantidade == 0:
            return "Nenhuma coleta encontrada."

        if quantidade == 1:
            return f"1 {singular}"

        return f"{quantidade} {plural}"

    @staticmethod
    def _sucesso(
        mensagem: str = "",
        dados: Any = None,
    ) -> RepositoryResult:
        """Cria um resultado bem-sucedido."""

        return RepositoryResult(
            sucesso=True,
            mensagem=mensagem,
            dados=dados,
        )

    @staticmethod
    def _falha(
        mensagem: str,
        dados: Any = None,
    ) -> RepositoryResult:
        """Cria um resultado de falha controlada."""

        return RepositoryResult(
            sucesso=False,
            mensagem=mensagem,
            dados=dados,
        )

    @staticmethod
    def _erro_inesperado(
        mensagem: str,
        erro: Exception,
    ) -> RepositoryResult:
        """
        Cria um resultado para uma falha inesperada.

        O erro técnico é mantido em dados para facilitar os testes
        e o registro posterior em log.
        """

        return RepositoryResult(
            sucesso=False,
            mensagem=mensagem,
            dados={
                "tipo_erro": type(erro).__name__,
                "detalhes": str(erro),
            },
        )