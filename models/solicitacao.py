from dataclasses import dataclass, asdict


@dataclass
class Solicitacao:
    id: int = 0
    usuario_id: int = 0
    tipo: str = ""
    quantidade: int = 1
    status: str = "PENDENTE"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, dados):
        return cls(**dados)