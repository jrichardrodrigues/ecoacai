from dataclasses import dataclass
from typing import Any


STATUS_PENDENTE = "PENDENTE"
STATUS_AGENDADA = "AGENDADA"
STATUS_EM_COLETA = "EM_COLETA"
STATUS_CONCLUIDA = "CONCLUIDA"
STATUS_CANCELADA = "CANCELADA"

PRIORIDADE_NORMAL = "NORMAL"
PRIORIDADE_URGENTE = "URGENTE"
PRIORIDADE_PROGRAMADA = "PROGRAMADA"


@dataclass(slots=True)
class SolicitacaoColeta:
    """Representa uma solicitação de coleta."""

    # ------------------------------------------------------------------
    # Identificação
    # ------------------------------------------------------------------
    id: int | None = None
    codigo: str = ""

    # ------------------------------------------------------------------
    # Relacionamentos
    # ------------------------------------------------------------------
    estabelecimento_id: int | None = None
    motorista_id: int | None = None
    veiculo_id: int | None = None

    # ------------------------------------------------------------------
    # Planejamento
    # ------------------------------------------------------------------
    quantidade_sacas_prevista: int = 0
    quantidade_kg_previsto: float = 0.0

    # ------------------------------------------------------------------
    # Execução
    # ------------------------------------------------------------------
    quantidade_sacas_coletada: int = 0
    quantidade_kg_coletado: float = 0.0

    # ------------------------------------------------------------------
    # Datas
    # ------------------------------------------------------------------
    data_solicitacao: str | None = None
    data_hora_agendada: str | None = None
    data_hora_inicio: str | None = None
    data_hora_chegada: str | None = None
    data_hora_conclusao: str | None = None

    # ------------------------------------------------------------------
    # Operação
    # ------------------------------------------------------------------
    status: str = STATUS_PENDENTE
    prioridade: str = PRIORIDADE_NORMAL

    # ------------------------------------------------------------------
    # Observações
    # ------------------------------------------------------------------
    observacao_cliente: str = ""
    observacao_operacional: str = ""

    # ------------------------------------------------------------------
    # Localização
    # ------------------------------------------------------------------
    latitude: float | None = None
    longitude: float | None = None

    # ------------------------------------------------------------------
    # Controle
    # ------------------------------------------------------------------
    ativo: bool = True

    criado_em: str | None = None
    atualizado_em: str | None = None

    # ==============================================================
    # PROPRIEDADES
    # ==============================================================

    @property
    def numero(self) -> str:
        """Retorna o código amigável da solicitação."""

        if self.codigo:
            return self.codigo

        if self.id is None:
            return "COL-NOVA"

        return f"COL-{self.id:06d}"

    @property
    def concluida(self) -> bool:
        """Indica se a solicitação já foi concluída."""

        return self.status == STATUS_CONCLUIDA

    @property
    def em_andamento(self) -> bool:
        """Indica se a coleta está em andamento."""

        return self.status == STATUS_EM_COLETA

    @property
    def pendente(self) -> bool:
        """Indica se a solicitação ainda está pendente."""

        return self.status == STATUS_PENDENTE

    @property
    def agendada(self) -> bool:
        """Indica se a solicitação está agendada."""

        return self.status == STATUS_AGENDADA

    @property
    def cancelada(self) -> bool:
        """Indica se a solicitação foi cancelada."""

        return self.status == STATUS_CANCELADA

    # ==============================================================
    # CONVERSÃO
    # ==============================================================

    def to_dict(self) -> dict:
        """Converte a solicitação para dicionário."""

        return {
            "id": self.id,
            "codigo": self.codigo,
            "estabelecimento_id": self.estabelecimento_id,
            "motorista_id": self.motorista_id,
            "veiculo_id": self.veiculo_id,
            "quantidade_sacas_prevista": self.quantidade_sacas_prevista,
            "quantidade_kg_previsto": self.quantidade_kg_previsto,
            "quantidade_sacas_coletada": self.quantidade_sacas_coletada,
            "quantidade_kg_coletado": self.quantidade_kg_coletado,
            "data_solicitacao": self.data_solicitacao,
            "data_hora_agendada": self.data_hora_agendada,
            "data_hora_inicio": self.data_hora_inicio,
            "data_hora_chegada": self.data_hora_chegada,
            "data_hora_conclusao": self.data_hora_conclusao,
            "status": self.status,
            "prioridade": self.prioridade,
            "observacao_cliente": self.observacao_cliente,
            "observacao_operacional": self.observacao_operacional,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "ativo": self.ativo,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }

    @classmethod
    def from_row(
        cls,
        row: Any,
    ) -> "SolicitacaoColeta":
        """Cria uma solicitação a partir de uma linha retornada pelo SQLite."""

        if row is None:
            raise ValueError(
                "Não é possível criar uma solicitação "
                "a partir de uma linha vazia."
            )

        return cls(
            id=row["id"],
            codigo=row["codigo"],
            estabelecimento_id=row["estabelecimento_id"],
            motorista_id=row["motorista_id"],
            veiculo_id=row["veiculo_id"],
            quantidade_sacas_prevista=row["quantidade_sacas_prevista"],
            quantidade_kg_previsto=row["quantidade_kg_previsto"],
            quantidade_sacas_coletada=row["quantidade_sacas_coletada"],
            quantidade_kg_coletado=row["quantidade_kg_coletado"],
            data_solicitacao=row["data_solicitacao"],
            data_hora_agendada=row["data_hora_agendada"],
            data_hora_inicio=row["data_hora_inicio"],
            data_hora_chegada=row["data_hora_chegada"],
            data_hora_conclusao=row["data_hora_conclusao"],
            status=row["status"],
            prioridade=row["prioridade"],
            observacao_cliente=row["observacao_cliente"],
            observacao_operacional=row["observacao_operacional"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            ativo=bool(row["ativo"]),
            criado_em=row["criado_em"],
            atualizado_em=row["atualizado_em"],
        )

    @classmethod
    def from_dict(
        cls,
        dados: dict,
    ) -> "SolicitacaoColeta":
        """Cria uma solicitação a partir de um dicionário."""

        return cls(
            id=dados.get("id"),
            codigo=dados.get("codigo", ""),
            estabelecimento_id=dados.get("estabelecimento_id"),
            motorista_id=dados.get("motorista_id"),
            veiculo_id=dados.get("veiculo_id"),
            quantidade_sacas_prevista=dados.get(
                "quantidade_sacas_prevista", 0
            ),
            quantidade_kg_previsto=dados.get(
                "quantidade_kg_previsto", 0.0
            ),
            quantidade_sacas_coletada=dados.get(
                "quantidade_sacas_coletada", 0
            ),
            quantidade_kg_coletado=dados.get(
                "quantidade_kg_coletado", 0.0
            ),
            data_solicitacao=dados.get("data_solicitacao"),
            data_hora_agendada=dados.get("data_hora_agendada"),
            data_hora_inicio=dados.get("data_hora_inicio"),
            data_hora_chegada=dados.get("data_hora_chegada"),
            data_hora_conclusao=dados.get("data_hora_conclusao"),
            status=dados.get("status", STATUS_PENDENTE),
            prioridade=dados.get("prioridade", PRIORIDADE_NORMAL),
            observacao_cliente=dados.get(
                "observacao_cliente", ""
            ),
            observacao_operacional=dados.get(
                "observacao_operacional", ""
            ),
            latitude=dados.get("latitude"),
            longitude=dados.get("longitude"),
            ativo=dados.get("ativo", True),
            criado_em=dados.get("criado_em"),
            atualizado_em=dados.get("atualizado_em"),
        )