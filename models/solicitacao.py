from dataclasses import asdict, dataclass


@dataclass
class Solicitacao:
    id: int = 0
    codigo: str = ""

    estabelecimento_id: int = 0

    quantidade_sacas_prevista: int = 1
    quantidade_kg: float = 0.0

    data_solicitacao: str = ""
    data_agendada: str = ""
    data_conclusao: str = ""

    status: str = "PENDENTE"
    prioridade: str = "NORMAL"

    observacao: str = ""

    motorista: str = ""
    veiculo: str = ""

    latitude: float | None = None
    longitude: float | None = None

    criado_em: str = ""
    atualizado_em: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dados: dict) -> "Solicitacao":
        return cls(**dados)