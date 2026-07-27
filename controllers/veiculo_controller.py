from __future__ import annotations

from models import Veiculo
from services import VeiculoService


class VeiculoController:
    """Controller responsável pelas operações de veículos."""

    def __init__(
        self,
        service: VeiculoService | None = None,
    ) -> None:
        self.service = service or VeiculoService()

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        veiculo: Veiculo,
    ) -> Veiculo:
        return self.service.cadastrar(
            veiculo,
        )

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def atualizar(
        self,
        veiculo: Veiculo,
    ) -> Veiculo:
        return self.service.atualizar(
            veiculo,
        )

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        veiculo_id: int,
    ) -> Veiculo | None:
        return self.service.buscar_por_id(
            veiculo_id,
        )

    def buscar_por_placa(
        self,
        placa: str,
    ) -> Veiculo | None:
        return self.service.buscar_por_placa(
            placa,
        )

    def listar(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Veiculo]:
        return self.service.listar(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
            limite=limite,
            pagina=pagina,
        )

    def listar_ativos(
        self,
    ) -> list[Veiculo]:
        return self.service.listar_ativos()

    def listar_disponiveis(
        self,
    ) -> list[Veiculo]:
        return self.service.listar_disponiveis()

    def listar_por_motorista(
        self,
        motorista_id: int,
    ) -> list[Veiculo]:
        return self.service.listar_por_motorista(
            motorista_id,
        )

    # ==========================================================
    # EXCLUSÃO LÓGICA
    # ==========================================================

    def desativar(
        self,
        veiculo_id: int,
    ) -> bool:
        return self.service.desativar(
            veiculo_id,
        )

    def reativar(
        self,
        veiculo_id: int,
    ) -> bool:
        return self.service.reativar(
            veiculo_id,
        )

    # ==========================================================
    # STATUS
    # ==========================================================

    def alterar_status(
        self,
        veiculo_id: int,
        status: str,
    ) -> bool:
        return self.service.alterar_status(
            veiculo_id,
            status,
        )

    # ==========================================================
    # UTILITÁRIOS
    # ==========================================================

    def quantidade(
        self,
    ) -> int:
        return self.service.repository.quantidade()

    def placa_existe(
        self,
        placa: str,
        ignorar_id: int | None = None,
    ) -> bool:
        return self.service.repository.placa_existe(
            placa,
            ignorar_id,
        )