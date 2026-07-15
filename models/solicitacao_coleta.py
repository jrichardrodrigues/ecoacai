from dataclasses import dataclass
from typing import Any


STATUS_PENDENTE = "PENDENTE"
STATUS_AGENDADA = "AGENDADA"
STATUS_EM_COLETA = "EM_COLETA"
STATUS_CONCLUIDA = "CONCLUIDA"

PRIORIDADE_NORMAL = "NORMAL"
PRIORIDADE_URGENTE = "URGENTE"
PRIORIDADE_PROGRAMADA = "PROGRAMADA"


@dataclass
class SolicitacaoColeta:
    """Representa uma solicitação de coleta."""

    id: int | None = None
    estabelecimento_id: int | None = None

    quantidade_sacas: int = 1
    quantidade_kg: float = 0.0

    data_solicitacao: str | None = None
    data_agendada: str | None = None
    data_conclusao: str | None = None

    status: str = STATUS_PENDENTE
    prioridade: str = PRIORIDADE_NORMAL

    observacao: str = ""

    latitude: float | None = None
    longitude: float | None = None

    criado_em: str | None = None
    atualizado_em: str | None = None

    @property
    def numero(self) -> str:
        """Retorna um número amigável para a solicitação."""

        if self.id is None:
            return "COL-NOVA"

        return f"COL-{self.id:06d}"

    @property
    def concluida(self) -> bool:
        """Indica se a solicitação está concluída."""

        return self.status == STATUS_CONCLUIDA

    def to_dict(self) -> dict:
        """Converte a solicitação em dicionário."""

        return {
            "id": self.id,
            "estabelecimento_id": self.estabelecimento_id,
            "quantidade_sacas": self.quantidade_sacas,
            "quantidade_kg": self.quantidade_kg,
            "data_solicitacao": self.data_solicitacao,
            "data_agendada": self.data_agendada,
            "data_conclusao": self.data_conclusao,
            "status": self.status,
            "prioridade": self.prioridade,
            "observacao": self.observacao,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }

    @classmethod
    def from_row(
        cls,
        row: Any,
    ) -> "SolicitacaoColeta":
        """Cria a solicitação a partir de uma linha SQLite."""

        if row is None:
            raise ValueError(
                "Não é possível criar uma solicitação "
                "a partir de uma linha vazia."
            )

        return cls(
            id=row["id"],
            estabelecimento_id=row["estabelecimento_id"],
            quantidade_sacas=row["quantidade_sacas"],
            quantidade_kg=row["quantidade_kg"],
            data_solicitacao=row["data_solicitacao"],
            data_agendada=row["data_agendada"],
            data_conclusao=row["data_conclusao"],
            status=row["status"],
            prioridade=row["prioridade"],
            observacao=row["observacao"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            criado_em=row["criado_em"],
            atualizado_em=row["atualizado_em"],
        )