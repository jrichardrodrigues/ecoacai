from dataclasses import dataclass


@dataclass
class Motorista:
    """Representa um motorista cadastrado no sistema."""

    nome: str
    telefone: str = ""
    cnh: str = ""
    categoria_cnh: str = ""
    ativo: bool = True
    id: int | None = None

    def to_dict(self) -> dict:
        """Converte o motorista para dicionário."""

        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "cnh": self.cnh,
            "categoria_cnh": self.categoria_cnh,
            "ativo": self.ativo,
        }

    @classmethod
    def from_row(
            cls,
            row,
    ) -> "Motorista":
        """Cria um motorista a partir de um sqlite3.Row."""

        if row is None:
            return None

        return cls(
            id=row["id"],
            nome=row["nome"],
            telefone=row["telefone"],
            cnh=row["cnh"],
            categoria_cnh=row["categoria_cnh"],
            ativo=bool(row["ativo"]),
        )

    @classmethod
    def from_dict(
        cls,
        dados: dict,
    ) -> "Motorista":
        """Cria um motorista a partir de um dicionário."""

        return cls(
            id=dados.get("id"),
            nome=dados.get("nome", ""),
            telefone=dados.get("telefone", ""),
            cnh=dados.get("cnh", ""),
            categoria_cnh=dados.get(
                "categoria_cnh",
                "",
            ),
            ativo=bool(
                dados.get("ativo", True)
            ),
        )