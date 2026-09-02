from __future__ import annotations

from datetime import date

from models import SolicitacaoColeta
from services import SolicitacaoColetaService


class SolicitacaoColetaController:
    """Controller das solicitações de coleta."""

    def __init__(
        self,
        service: SolicitacaoColetaService | None = None,
    ) -> None:
        self.service = (
            service or SolicitacaoColetaService()
        )

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def listar(
        self,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        """Lista todas as solicitações."""

        return self.service.listar(
            somente_ativas=somente_ativas,
        )

    def buscar_por_id(
        self,
        solicitacao_id: int,
    ) -> SolicitacaoColeta | None:
        """Busca uma solicitação pelo identificador."""

        return self.service.buscar_por_id(
            solicitacao_id
        )

    def listar_por_organizacao(
        self,
        organizacao_id: int,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        """Lista as solicitações de uma organização."""

        return self.service.listar_por_organizacao(
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
        """Lista solicitações por status."""

        return self.service.listar_por_status(
            status=status,
            organizacao_id=organizacao_id,
            somente_ativas=somente_ativas,
        )

    def listar_por_periodo(
        self,
        data_inicial: str | date,
        data_final: str | date,
        *,
        organizacao_id: int | None = None,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        """Lista solicitações dentro de um período."""

        return self.service.listar_por_periodo(
            data_inicial=data_inicial,
            data_final=data_final,
            organizacao_id=organizacao_id,
            somente_ativas=somente_ativas,
        )

    def listar_operacional(
            self,
            *,
            status: str | None = None,
            organizacao_id: int | None = None,
            empresa_parceira_id: int | None = None,
            data_agendada: str | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
            pesquisa: str | None = None,
    ) -> list[dict]:
        """Lista solicitações com seus vínculos operacionais."""

        return self.service.listar_operacional(
            status=status,
            organizacao_id=organizacao_id,
            empresa_parceira_id=empresa_parceira_id,
            data_agendada=data_agendada,
            data_inicial=data_inicial,
            data_final=data_final,
            pesquisa=pesquisa,
        )

    def listar_com_estabelecimento(
        self,
    ) -> list[dict]:
        """
        Mantém compatibilidade com a interface antiga.

        Para novos fluxos, prefira listar_operacional().
        """

        return self.service.listar_com_estabelecimento()

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def obter_estatisticas(
        self,
        organizacao_id: int | None = None,
    ) -> dict:
        """Retorna os indicadores das solicitações."""

        return self.service.obter_estatisticas(
            organizacao_id=organizacao_id,
        )

    def listar_ultimas(
        self,
        limite: int = 5,
        *,
        organizacao_id: int | None = None,
    ) -> list[dict]:
        """Retorna as solicitações mais recentes."""

        return self.service.listar_ultimas(
            limite=limite,
            organizacao_id=organizacao_id,
        )

    def contar_agendadas_hoje(
        self,
        organizacao_id: int | None = None,
    ) -> int:
        """Retorna a quantidade de coletas agendadas hoje."""

        return self.service.contar_agendadas_hoje(
            organizacao_id=organizacao_id,
        )

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def criar(
            self,
            quantidade_prevista: int,
            *,
            forma_acondicionamento: str = "SACA",
            organizacao_id: int | None = None,
            estabelecimento_id: int | None = None,
            empresa_parceira_id: int | None = None,
            usuario_criacao_id: int | None = None,
            motorista_id: int | None = None,
            veiculo_id: int | None = None,
            tipo_residuo: str = "CAROCO_ACAI",
            origem: str = "GERADOR",
            prioridade: str = "NORMAL",
            data_hora_agendada: str = "",
            observacao_cliente: str = "",
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Cria uma nova solicitação de coleta."""

        return self.service.criar(
            quantidade_prevista=quantidade_prevista,
            forma_acondicionamento=forma_acondicionamento,
            organizacao_id=organizacao_id,
            estabelecimento_id=estabelecimento_id,
            empresa_parceira_id=empresa_parceira_id,
            usuario_criacao_id=usuario_criacao_id,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            tipo_residuo=tipo_residuo,
            origem=origem,
            prioridade=prioridade,
            data_hora_agendada=data_hora_agendada,
            observacao_cliente=observacao_cliente,
        )

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def atualizar(
        self,
        solicitacao: SolicitacaoColeta,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Atualiza uma solicitação existente."""

        return self.service.atualizar(
            solicitacao
        )

    # ==========================================================
    # FLUXO OPERACIONAL
    # ==========================================================

    def analisar(
        self,
        solicitacao_id: int,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Encaminha uma solicitação para análise."""

        return self.service.analisar(
            solicitacao_id
        )

    def agendar(
        self,
        solicitacao_id: int,
        data_hora_agendada: str,
        *,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        empresa_parceira_id: int | None = None,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Agenda uma solicitação de coleta."""

        return self.service.agendar(
            solicitacao_id=solicitacao_id,
            data_hora_agendada=data_hora_agendada,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            empresa_parceira_id=empresa_parceira_id,
        )

    def iniciar_deslocamento(
        self,
        solicitacao_id: int,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Registra o início do deslocamento."""

        return self.service.iniciar_deslocamento(
            solicitacao_id
        )

    def iniciar_coleta(
        self,
        solicitacao_id: int,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Registra o início da coleta."""

        return self.service.iniciar_coleta(
            solicitacao_id
        )

    def concluir(
        self,
        solicitacao_id: int,
        *,
        quantidade_sacas_coletada: int | None = None,
        quantidade_kg_coletado: float | None = None,
        observacao_operacional: str | None = None,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Conclui uma coleta em andamento."""

        return self.service.concluir(
            solicitacao_id=solicitacao_id,
            quantidade_sacas_coletada=(
                quantidade_sacas_coletada
            ),
            quantidade_kg_coletado=(
                quantidade_kg_coletado
            ),
            observacao_operacional=(
                observacao_operacional
            ),
        )

    def cancelar(
        self,
        solicitacao_id: int,
        observacao: str = "",
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Cancela uma solicitação permitida."""

        return self.service.cancelar(
            solicitacao_id=solicitacao_id,
            observacao=observacao,
        )

    def recusar(
        self,
        solicitacao_id: int,
        motivo: str,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Recusa uma solicitação informando o motivo."""

        return self.service.recusar(
            solicitacao_id=solicitacao_id,
            motivo=motivo,
        )

    def atribuir_empresa_parceira(
        self,
        solicitacao_id: int,
        empresa_parceira_id: int,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """Atribui uma Empresa Parceira à solicitação."""

        return self.service.atribuir_empresa_parceira(
            solicitacao_id=solicitacao_id,
            empresa_parceira_id=empresa_parceira_id,
        )

    # ==========================================================
    # COMPATIBILIDADE COM AS VIEWS ANTIGAS
    # ==========================================================

    def alterar_status(
        self,
        solicitacao_id: int,
    ) -> tuple[
        bool,
        str,
        SolicitacaoColeta | None,
    ]:
        """
        Avança para o próximo status permitido.

        Mantido temporariamente para as Views antigas.
        Nas novas telas, utilize os métodos específicos.
        """

        return self.service.alterar_status(
            solicitacao_id
        )

    # ==========================================================
    # EXCLUSÃO LÓGICA
    # ==========================================================

    def excluir(
        self,
        solicitacao_id: int,
    ) -> tuple[bool, str]:
        """Desativa uma solicitação."""

        return self.service.excluir(
            solicitacao_id
        )

    def restaurar(
            self,
            solicitacao_id: int,
    ) -> tuple[bool, str]:
        """Restaura uma solicitação excluída logicamente."""

        return self.service.restaurar(
            solicitacao_id
        )

    def listar_excluidas(
            self,
            organizacao_id: int | None = None,
    ) -> list[dict]:
        """Lista as solicitações excluídas logicamente."""

        return self.service.listar_excluidas(
            organizacao_id=organizacao_id,
        )