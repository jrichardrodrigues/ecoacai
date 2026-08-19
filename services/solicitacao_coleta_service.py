from __future__ import annotations

from datetime import datetime
from typing import Any

from models import SolicitacaoColeta
from models.solicitacao_coleta import (
    ORIGEM_GERADOR,
    PRIORIDADE_NORMAL,
    STATUS_AGENDADA,
    STATUS_CANCELADA,
    STATUS_CONCLUIDA,
    STATUS_EM_ANALISE,
    STATUS_EM_COLETA,
    STATUS_EM_DESLOCAMENTO,
    STATUS_RECUSADA,
    STATUS_SOLICITADA,
    TIPO_RESIDUO_CAROCO_ACAI,
    FORMA_BAG,
    FORMA_SACA,
)
from repositories import SolicitacaoColetaRepository


class SolicitacaoColetaService:
    """Regras de negócio das solicitações de coleta."""

    TRANSICOES_STATUS = {
        STATUS_SOLICITADA: STATUS_EM_ANALISE,
        STATUS_EM_ANALISE: STATUS_AGENDADA,
        STATUS_AGENDADA: STATUS_EM_DESLOCAMENTO,
        STATUS_EM_DESLOCAMENTO: STATUS_EM_COLETA,
        STATUS_EM_COLETA: STATUS_CONCLUIDA,
    }

    STATUS_FINAIS = {
        STATUS_CONCLUIDA,
        STATUS_CANCELADA,
        STATUS_RECUSADA,
    }

    def __init__(
        self,
        repository: SolicitacaoColetaRepository | None = None,
    ) -> None:
        self.repository = repository or SolicitacaoColetaRepository()

    @staticmethod
    def _erro_operacao(
        operacao: str,
        erro: Exception,
    ) -> tuple[bool, str, None]:
        """Padroniza o tratamento de erros inesperados."""

        print(f"Erro ao {operacao} solicitação:", erro)

        return (
            False,
            f"Não foi possível {operacao} a solicitação.",
            None,
        )

    @staticmethod
    def _id_valido(identificador: Any) -> bool:
        return (
            isinstance(identificador, int)
            and not isinstance(identificador, bool)
            and identificador > 0
        )

    @classmethod
    def _validar_vinculo(
        cls,
        *,
        organizacao_id: int | None,
        estabelecimento_id: int | None,
    ) -> tuple[bool, str]:
        organizacao_valida = (
            organizacao_id is not None
            and cls._id_valido(organizacao_id)
        )
        estabelecimento_valido = (
            estabelecimento_id is not None
            and cls._id_valido(estabelecimento_id)
        )

        if not organizacao_valida and not estabelecimento_valido:
            return (
                False,
                "A solicitação deve estar vinculada a uma organização.",
            )

        return True, ""

    @classmethod
    def _validar_quantidades(
            cls,
            *,
            quantidade_prevista: int,
    ) -> tuple[bool, str]:
        if (
                not isinstance(quantidade_prevista, int)
                or isinstance(quantidade_prevista, bool)
        ):
            return (
                False,
                "A quantidade informada é inválida.",
            )

        if quantidade_prevista <= 0:
            return (
                False,
                "A quantidade deve ser maior que zero.",
            )

        return True, ""

    @classmethod
    def _validar_solicitacao(
            cls,
            *,
            organizacao_id: int | None,
            estabelecimento_id: int | None,
            quantidade_prevista: int,
    ) -> tuple[bool, str]:
        valido, mensagem = cls._validar_vinculo(
            organizacao_id=organizacao_id,
            estabelecimento_id=estabelecimento_id,
        )

        if not valido:
            return valido, mensagem

        return cls._validar_quantidades(
            quantidade_prevista=quantidade_prevista,
        )

    def listar(
        self,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        return self.repository.listar(
            somente_ativas=somente_ativas,
        )

    def buscar_por_id(
        self,
        solicitacao_id: int,
    ) -> SolicitacaoColeta | None:
        if not self._id_valido(solicitacao_id):
            return None

        return self.repository.buscar_por_id(solicitacao_id)

    def listar_por_organizacao(
        self,
        organizacao_id: int,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        if not self._id_valido(organizacao_id):
            return []

        return self.repository.listar_por_organizacao(
            organizacao_id=organizacao_id,
            somente_ativas=somente_ativas,
        )

    def listar_por_status(
        self,
        status: str,
        *,
        organizacao_id: int | None = None,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        return self.repository.listar_por_status(
            status=status,
            organizacao_id=organizacao_id,
            somente_ativas=somente_ativas,
        )

    def listar_por_periodo(
        self,
        data_inicial,
        data_final,
        *,
        organizacao_id: int | None = None,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        return self.repository.listar_por_periodo(
            data_inicial=data_inicial,
            data_final=data_final,
            organizacao_id=organizacao_id,
            somente_ativas=somente_ativas,
        )

    def obter_estatisticas(
            self,
            organizacao_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> dict:
        return self.repository.obter_estatisticas(
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def obter_tempo_medio_atendimento(
            self,
            organizacao_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> float:
        """Retorna o tempo médio de atendimento em minutos."""

        return self.repository.obter_tempo_medio_atendimento(
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def obter_tempo_medio_coleta(
            self,
            organizacao_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> float:
        """Retorna o tempo médio de coleta em minutos."""

        return self.repository.obter_tempo_medio_coleta(
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def obter_tempo_medio_espera(
        self,
        organizacao_id: int | None = None,
        data_inicial: str | None = None,
        data_final: str | None = None,
    ) -> float:
        """Retorna o tempo médio de espera em minutos."""

        return self.repository.obter_tempo_medio_espera(
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def obter_taxa_cumprimento_agendamento(
            self,
            organizacao_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> float:
        """
        Retorna a taxa percentual de cumprimento do agendamento.

        Considera pontual a chegada realizada até 15 minutos
        após o horário agendado.
        """

        return self.repository.obter_taxa_cumprimento_agendamento(
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def obter_eficiencia_volume_coletado(
            self,
            organizacao_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> float:
        """Retorna a eficiência do volume coletado, em percentual."""

        return self.repository.obter_eficiencia_volume_coletado(
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def obter_evolucao_solicitacoes(
            self,
            organizacao_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> list[dict]:
        """
        Retorna a evolução diária das solicitações e
        das coletas concluídas.
        """
        return self.repository.obter_evolucao_solicitacoes(
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def listar_ultimas(
            self,
            limite: int = 5,
            *,
            organizacao_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> list[dict]:
        return self.repository.listar_ultimas(
            limite=limite,
            organizacao_id=organizacao_id,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def contar_agendadas_hoje(
        self,
        organizacao_id: int | None = None,
    ) -> int:
        return self.repository.contar_agendadas_hoje(
            organizacao_id=organizacao_id,
        )

    def listar_operacional(
            self,
            *,
            status: str | None = None,
            organizacao_id: int | None = None,
            empresa_parceira_id: int | None = None,
            data_agendada: str | None = None,
    ) -> list[dict]:
        return self.repository.listar_operacional(
            status=status,
            organizacao_id=organizacao_id,
            empresa_parceira_id=empresa_parceira_id,
            data_agendada=data_agendada,
        )

    def listar_com_estabelecimento(self) -> list[dict]:
        """Mantém compatibilidade com a interface antiga."""

        return self.repository.listar_com_estabelecimento()

    def criar(
            self,
            quantidade_prevista: int,
            *,
            forma_acondicionamento: str = FORMA_SACA,
            organizacao_id: int | None = None,
            estabelecimento_id: int | None = None,
            empresa_parceira_id: int | None = None,
            usuario_criacao_id: int | None = None,
            motorista_id: int | None = None,
            veiculo_id: int | None = None,
            tipo_residuo: str = TIPO_RESIDUO_CAROCO_ACAI,
            origem: str = ORIGEM_GERADOR,
            prioridade: str = PRIORIDADE_NORMAL,
            data_hora_agendada: str = "",
            observacao_cliente: str = "",
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        """Valida e cadastra uma nova solicitação."""

        valido, mensagem = self._validar_solicitacao(
            organizacao_id=organizacao_id,
            estabelecimento_id=estabelecimento_id,
            quantidade_prevista=quantidade_prevista,
        )

        if not valido:
            return False, mensagem, None

        forma_normalizada = (
            str(forma_acondicionamento or FORMA_SACA)
            .strip()
            .upper()
        )

        if forma_normalizada not in {
            FORMA_SACA,
            FORMA_BAG,
        }:
            return (
                False,
                "Forma de acondicionamento inválida.",
                None,
            )

        solicitacao = SolicitacaoColeta(
            organizacao_id=organizacao_id,
            empresa_parceira_id=empresa_parceira_id,
            usuario_criacao_id=usuario_criacao_id,
            estabelecimento_id=estabelecimento_id,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            tipo_residuo=(
                str(
                    tipo_residuo
                    or TIPO_RESIDUO_CAROCO_ACAI
                )
                .strip()
                .upper()
            ),
            forma_acondicionamento=forma_normalizada,
            quantidade_prevista=quantidade_prevista,
            origem=(
                str(origem or ORIGEM_GERADOR)
                .strip()
                .upper()
            ),
            data_hora_agendada=(
                str(data_hora_agendada or "").strip()
            ),
            observacao_cliente=(
                str(observacao_cliente or "").strip()
            ),
            status=STATUS_SOLICITADA,
            prioridade=(
                str(prioridade or PRIORIDADE_NORMAL)
                .strip()
                .upper()
            ),
            data_solicitacao=self._agora(),
        )

        solicitacao.atualizar_planejamento()

        try:
            cadastrada = self.repository.cadastrar(
                solicitacao
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

        existente = self.repository.buscar_por_id(
            solicitacao.id
        )

        if existente is None:
            return (
                False,
                "Solicitação não encontrada.",
                None,
            )

        if existente.status in self.STATUS_FINAIS:
            return (
                False,
                "Solicitações finalizadas não podem ser alteradas.",
                None,
            )

        valido, mensagem = self._validar_solicitacao(
            organizacao_id=solicitacao.organizacao_id,
            estabelecimento_id=solicitacao.estabelecimento_id,
            quantidade_prevista=solicitacao.quantidade_prevista,
        )

        if not valido:
            return (
                False,
                mensagem,
                None,
            )

        forma_normalizada = (
            str(
                solicitacao.forma_acondicionamento
                or FORMA_SACA
            )
            .strip()
            .upper()
        )

        if forma_normalizada not in {
            FORMA_SACA,
            FORMA_BAG,
        }:
            return (
                False,
                "Forma de acondicionamento inválida.",
                None,
            )

        solicitacao.forma_acondicionamento = (
            forma_normalizada
        )

        solicitacao.atualizar_planejamento()

        try:
            atualizada = self.repository.atualizar(
                solicitacao
            )

        except Exception as erro:
            return self._erro_operacao(
                "atualizar",
                erro,
            )

        if atualizada is None:
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

    def analisar(
        self,
        solicitacao_id: int,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        return self._alterar_para_status(
            solicitacao_id=solicitacao_id,
            status_destino=STATUS_EM_ANALISE,
            status_origem={STATUS_SOLICITADA},
            mensagem="Solicitação encaminhada para análise.",
        )

    def agendar(
        self,
        solicitacao_id: int,
        data_hora_agendada: str,
        *,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        empresa_parceira_id: int | None = None,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada.", None

        if solicitacao.status != STATUS_EM_ANALISE:
            return (
                False,
                "Somente solicitações em análise podem ser agendadas.",
                None,
            )

        data_agendada = str(data_hora_agendada or "").strip()

        if not data_agendada:
            return (
                False,
                "Informe a data e a hora do agendamento.",
                None,
            )

        solicitacao.status = STATUS_AGENDADA
        solicitacao.data_hora_agendada = data_agendada
        solicitacao.motorista_id = motorista_id
        solicitacao.veiculo_id = veiculo_id
        solicitacao.empresa_parceira_id = empresa_parceira_id

        try:
            atualizada = self.repository.atualizar(solicitacao)
        except Exception as erro:
            return self._erro_operacao("agendar", erro)

        return True, "Coleta agendada com sucesso.", atualizada

    def iniciar_deslocamento(
        self,
        solicitacao_id: int,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        return self._alterar_para_status(
            solicitacao_id=solicitacao_id,
            status_destino=STATUS_EM_DESLOCAMENTO,
            status_origem={STATUS_AGENDADA},
            mensagem="Deslocamento iniciado.",
            campo_data="data_hora_inicio",
        )

    def iniciar_coleta(
        self,
        solicitacao_id: int,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        return self._alterar_para_status(
            solicitacao_id=solicitacao_id,
            status_destino=STATUS_EM_COLETA,
            status_origem={STATUS_EM_DESLOCAMENTO},
            mensagem="Coleta iniciada.",
            campo_data="data_hora_chegada",
        )

    def concluir(
        self,
        solicitacao_id: int,
        *,
        quantidade_sacas_coletada: int | None = None,
        quantidade_kg_coletado: float | None = None,
        observacao_operacional: str | None = None,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada.", None

        if solicitacao.status != STATUS_EM_COLETA:
            return (
                False,
                "Somente coletas em andamento podem ser concluídas.",
                None,
            )

        if quantidade_sacas_coletada is not None:
            if quantidade_sacas_coletada < 0:
                return (
                    False,
                    "A quantidade de sacas coletada é inválida.",
                    None,
                )
            solicitacao.quantidade_sacas_coletada = (
                quantidade_sacas_coletada
            )

        if quantidade_kg_coletado is not None:
            if quantidade_kg_coletado < 0:
                return (
                    False,
                    "A quantidade coletada em quilos é inválida.",
                    None,
                )
            solicitacao.quantidade_kg_coletado = quantidade_kg_coletado

        if observacao_operacional is not None:
            solicitacao.observacao_operacional = (
                str(observacao_operacional).strip()
            )

        solicitacao.status = STATUS_CONCLUIDA
        solicitacao.data_hora_conclusao = self._agora()

        try:
            atualizada = self.repository.atualizar(solicitacao)
        except Exception as erro:
            return self._erro_operacao("concluir", erro)

        return True, "Coleta concluída com sucesso.", atualizada

    def cancelar(
        self,
        solicitacao_id: int,
        observacao: str = "",
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada.", None

        if solicitacao.status in self.STATUS_FINAIS:
            return (
                False,
                "Esta solicitação não permite cancelamento.",
                None,
            )

        if solicitacao.status in {
            STATUS_EM_DESLOCAMENTO,
            STATUS_EM_COLETA,
        }:
            return (
                False,
                "Não é possível cancelar uma coleta em execução.",
                None,
            )

        solicitacao.status = STATUS_CANCELADA

        if observacao:
            solicitacao.observacao_operacional = str(observacao).strip()

        try:
            atualizada = self.repository.atualizar(solicitacao)
        except Exception as erro:
            return self._erro_operacao("cancelar", erro)

        return True, "Solicitação cancelada com sucesso.", atualizada

    def recusar(
        self,
        solicitacao_id: int,
        motivo: str,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada.", None

        if solicitacao.status not in {
            STATUS_SOLICITADA,
            STATUS_EM_ANALISE,
        }:
            return (
                False,
                "Esta solicitação não pode ser recusada.",
                None,
            )

        motivo_normalizado = str(motivo or "").strip()

        if not motivo_normalizado:
            return False, "Informe o motivo da recusa.", None

        solicitacao.status = STATUS_RECUSADA
        solicitacao.observacao_operacional = motivo_normalizado

        try:
            atualizada = self.repository.atualizar(solicitacao)
        except Exception as erro:
            return self._erro_operacao("recusar", erro)

        return True, "Solicitação recusada.", atualizada

    def alterar_status(
        self,
        solicitacao_id: int,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        """Mantém compatibilidade com as Views antigas."""

        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada.", None

        destino = self.TRANSICOES_STATUS.get(solicitacao.status)

        if destino is None:
            return (
                False,
                "A solicitação não permite nova alteração de status.",
                None,
            )

        if destino == STATUS_EM_ANALISE:
            return self.analisar(solicitacao_id)

        if destino == STATUS_AGENDADA:
            data_agendada = (
                solicitacao.data_hora_agendada
                or self._agora()
            )
            return self.agendar(
                solicitacao_id=solicitacao_id,
                data_hora_agendada=data_agendada,
                motorista_id=solicitacao.motorista_id,
                veiculo_id=solicitacao.veiculo_id,
                empresa_parceira_id=solicitacao.empresa_parceira_id,
            )

        if destino == STATUS_EM_DESLOCAMENTO:
            return self.iniciar_deslocamento(solicitacao_id)

        if destino == STATUS_EM_COLETA:
            return self.iniciar_coleta(solicitacao_id)

        if destino == STATUS_CONCLUIDA:
            return self.concluir(solicitacao_id)

        return False, "Transição de status não reconhecida.", None

    def _alterar_para_status(
        self,
        *,
        solicitacao_id: int,
        status_destino: str,
        status_origem: set[str],
        mensagem: str,
        campo_data: str | None = None,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada.", None

        if solicitacao.status not in status_origem:
            return False, "Transição de status não permitida.", None

        solicitacao.status = status_destino

        if campo_data is not None:
            setattr(solicitacao, campo_data, self._agora())

        try:
            atualizada = self.repository.alterar_status(solicitacao)
        except Exception as erro:
            return self._erro_operacao("alterar o status de", erro)

        return True, mensagem, atualizada

    def atribuir_empresa_parceira(
        self,
        solicitacao_id: int,
        empresa_parceira_id: int,
    ) -> tuple[bool, str, SolicitacaoColeta | None]:
        if not self._id_valido(empresa_parceira_id):
            return False, "Empresa parceira inválida.", None

        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada.", None

        if solicitacao.status in self.STATUS_FINAIS:
            return (
                False,
                "Não é possível alterar uma solicitação finalizada.",
                None,
            )

        try:
            atualizada = self.repository.vincular_empresa_parceira(
                solicitacao_id=solicitacao_id,
                empresa_parceira_id=empresa_parceira_id,
            )
        except Exception as erro:
            return self._erro_operacao(
                "atribuir empresa parceira à",
                erro,
            )

        if atualizada is None:
            return (
                False,
                "Não foi possível atribuir a empresa parceira.",
                None,
            )

        return (
            True,
            "Empresa parceira atribuída com sucesso.",
            atualizada,
        )

    def excluir(
        self,
        solicitacao_id: int,
    ) -> tuple[bool, str]:
        """Desativa uma solicitação sem removê-la fisicamente."""

        if not self._id_valido(solicitacao_id):
            return False, "Solicitação inválida."

        solicitacao = self.repository.buscar_por_id(solicitacao_id)

        if solicitacao is None:
            return False, "Solicitação não encontrada."

        if solicitacao.status in {
            STATUS_EM_DESLOCAMENTO,
            STATUS_EM_COLETA,
            STATUS_CONCLUIDA,
        }:
            return False, "Esta solicitação não pode ser excluída."

        try:
            sucesso = self.repository.excluir(solicitacao_id)
        except Exception as erro:
            print("Erro ao excluir solicitação:", erro)
            return False, "Não foi possível excluir a solicitação."

        if not sucesso:
            return False, "Não foi possível excluir a solicitação."

        return True, "Solicitação excluída com sucesso."

    @staticmethod
    def _agora() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
