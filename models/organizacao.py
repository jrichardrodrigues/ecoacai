from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Organizacao:
    """Representa uma organização participante da ZELURBIS."""

    id: int | None = None

    tipo: str = ""
    nome: str = ""
    documento: str = ""

    email: str = ""
    telefone: str = ""

    ativo: bool = True

    criado_em: str | None = None
    atualizado_em: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_row(cls, row: Any) -> "Organizacao":
        if row is None:
            raise ValueError(
                "Não é possível criar uma organização a partir de uma linha vazia."
            )

        return cls(
            id=row["id"],
            tipo=row["tipo"],
            nome=row["nome"],
            documento=row["documento"] or "",
            email=row["email"] or "",
            telefone=row["telefone"] or "",
            ativo=bool(row["ativo"]),
            criado_em=row["criado_em"],
            atualizado_em=row["atualizado_em"],
        )