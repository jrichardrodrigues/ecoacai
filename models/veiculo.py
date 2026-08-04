from __future__ import annotations

from dataclasses import dataclass
from config.constants import StatusVeiculo


@dataclass(slots=True)
class Veiculo:
    """
    Modelo de domínio para veículos.

    Representa um veículo utilizado nas coletas de caroço de açaí.
    """

    id: int | None = None

    placa: str = ""
    marca: str = ""
    modelo: str = ""

    ano: int | None = None

    tipo: str = ""

    capacidade: float | None = None

    motorista_id: int | None = None

    status: str = StatusVeiculo.DISPONIVEL

    ativo: bool = True

    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""

        return {
            "id": self.id,
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "tipo": self.tipo,
            "capacidade": self.capacidade,
            "motorista_id": self.motorista_id,
            "status": self.status,
            "ativo": self.ativo,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Veiculo":
        """Cria um objeto Veiculo a partir de um dicionário."""

        return cls(
            id=dados.get("id"),
            placa=dados.get("placa", ""),
            marca=dados.get("marca", ""),
            modelo=dados.get("modelo", ""),
            ano=dados.get("ano"),
            tipo=dados.get("tipo", ""),
            capacidade=dados.get("capacidade"),
            motorista_id=dados.get("motorista_id"),
            status=dados.get("status", "DISPONIVEL"),
            ativo=bool(dados.get("ativo", True)),
        )