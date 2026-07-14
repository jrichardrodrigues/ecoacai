from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Estabelecimento:
    """Representa um estabelecimento atendido pela coleta."""

    id: int | None = None

    nome: str = ""
    cpf: str = ""
    email: str = ""
    celular: str = ""

    endereco: str = ""
    bairro: str = ""
    setor: str = ""

    ativo: bool = True

    criado_em: str | None = None
    atualizado_em: str | None = None

    def to_dict(self) -> dict:
        """Converte o estabelecimento em dicionário."""

        return asdict(self)

    @classmethod
    def from_row(cls, row: Any) -> "Estabelecimento":
        """Cria um estabelecimento a partir de uma linha SQLite."""

        if row is None:
            raise ValueError(
                "Não é possível criar um estabelecimento "
                "a partir de uma linha vazia."
            )

        return cls(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            email=row["email"],
            celular=row["celular"],
            endereco=row["endereco"],
            bairro=row["bairro"],
            setor=row["setor"],
            ativo=bool(row["ativo"]),
            criado_em=row["criado_em"],
            atualizado_em=row["atualizado_em"],
        )

    @property
    def endereco_completo(self) -> str:
        """Retorna o endereço acompanhado do bairro."""

        endereco = self.endereco.strip()
        bairro = self.bairro.strip()

        if endereco and bairro:
            return f"{endereco}, {bairro}"

        return endereco or bairro