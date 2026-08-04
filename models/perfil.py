from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Perfil:
    """Representa um perfil de acesso da plataforma."""

    id: int | None = None
    codigo: str = ""
    nome: str = ""
    descricao: str = ""
    ativo: bool = True

    criado_em: str | None = None
    atualizado_em: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_row(cls, row: Any) -> "Perfil":
        if row is None:
            raise ValueError(
                "Não é possível criar um perfil a partir de uma linha vazia."
            )

        return cls(
            id=row["id"],
            codigo=row["codigo"],
            nome=row["nome"],
            descricao=row["descricao"] or "",
            ativo=bool(row["ativo"]),
            criado_em=row["criado_em"],
            atualizado_em=row["atualizado_em"],
        )