from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Usuario:
    id: int | None = None

    nome: str = ""
    cpf: str = ""
    celular: str = ""

    cep: str = ""
    logradouro: str = ""
    numero: str = ""
    complemento: str = ""
    bairro: str = ""
    cidade: str = ""
    uf: str = ""

    senha_hash: str = ""
    celular_confirmado: bool = False
    ativo: bool = True

    criado_em: str | None = None
    atualizado_em: str | None = None

    # Campos legados temporários.
    email: str = ""
    endereco: str = ""
    setor: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dados: dict) -> "Usuario":
        campos_validos = cls.__dataclass_fields__.keys()

        dados_filtrados = {
            campo: valor
            for campo, valor in dados.items()
            if campo in campos_validos
        }

        return cls(**dados_filtrados)

    @classmethod
    def from_row(cls, row: Any) -> "Usuario":
        if row is None:
            raise ValueError("Não é possível criar usuário a partir de uma linha vazia.")

        return cls(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            celular=row["celular"],
            cep=row["cep"],
            logradouro=row["logradouro"],
            numero=row["numero"],
            complemento=row["complemento"] or "",
            bairro=row["bairro"],
            cidade=row["cidade"],
            uf=row["uf"],
            senha_hash=row["senha_hash"],
            celular_confirmado=bool(row["celular_confirmado"]),
            ativo=bool(row["ativo"]),
            criado_em=row["criado_em"],
            atualizado_em=row["atualizado_em"],
        )

    @property
    def endereco_completo(self) -> str:
        partes = [
            self.logradouro,
            self.numero,
            self.complemento,
            self.bairro,
            self.cidade,
            self.uf,
            self.cep,
        ]

        return ", ".join(
            str(parte).strip()
            for parte in partes
            if str(parte or "").strip()
        )