from __future__ import annotations

from datetime import datetime

from config.constants import (
    STATUS_VEICULOS,
    STATUS_VEICULO_DISPONIVEL,
)
from models import Veiculo
from repositories import VeiculoRepository


class VeiculoService:
    """Regras de negócio dos veículos."""

    def __init__(
        self,
        repository: VeiculoRepository | None = None,
    ) -> None:
        self.repository = repository or VeiculoRepository()

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        veiculo: Veiculo,
    ) -> Veiculo:
        """Valida e cadastra um veículo."""

        self._validar(
            veiculo,
            ignorar_id=None,
        )

        return self.repository.cadastrar(
            veiculo,
        )

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def atualizar(
        self,
        veiculo: Veiculo,
    ) -> Veiculo:
        """Valida e atualiza um veículo."""

        if veiculo.id is None:
            raise ValueError(
                "Veículo sem identificador."
            )

        self._validar(
            veiculo,
            ignorar_id=veiculo.id,
        )

        return self.repository.atualizar(
            veiculo,
        )

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        veiculo_id: int,
    ) -> Veiculo | None:
        return self.repository.buscar_por_id(
            veiculo_id,
        )

    def buscar_por_placa(
        self,
        placa: str,
    ) -> Veiculo | None:
        return self.repository.buscar_por_placa(
            placa,
        )

    def listar(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Veiculo]:

        return self.repository.listar(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
            limite=limite,
            pagina=pagina,
        )

    def listar_ativos(
        self,
    ) -> list[Veiculo]:
        return self.repository.listar_ativos()

    def listar_disponiveis(
        self,
    ) -> list[Veiculo]:
        return self.repository.listar_disponiveis()

    def listar_por_motorista(
        self,
        motorista_id: int,
    ) -> list[Veiculo]:
        return self.repository.listar_por_motorista(
            motorista_id,
        )

    # ==========================================================
    # EXCLUSÃO LÓGICA
    # ==========================================================

    def desativar(
        self,
        veiculo_id: int,
    ) -> bool:
        return self.repository.excluir(
            veiculo_id,
        )

    def reativar(
        self,
        veiculo_id: int,
    ) -> bool:
        return self.repository.reativar(
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

        status = str(
            status or "",
        ).strip().upper()

        if status not in STATUS_VEICULOS:
            raise ValueError(
                "Status do veículo inválido."
            )

        return self.repository.alterar_status(
            veiculo_id,
            status,
        )

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    def _validar(
        self,
        veiculo: Veiculo,
        ignorar_id: int | None,
    ) -> None:

        self._validar_placa(
            veiculo,
            ignorar_id,
        )

        self._validar_marca(
            veiculo,
        )

        self._validar_modelo(
            veiculo,
        )

        self._validar_tipo(
            veiculo,
        )

        self._validar_ano(
            veiculo,
        )

        self._validar_capacidade(
            veiculo,
        )

        self._validar_status(
            veiculo,
        )

    def _validar_placa(
        self,
        veiculo: Veiculo,
        ignorar_id: int | None,
    ) -> None:

        placa = (
            veiculo.placa or ""
        ).strip().upper()

        if not placa:
            raise ValueError(
                "Informe a placa."
            )

        if self.repository.placa_existe(
            placa,
            ignorar_id,
        ):
            raise ValueError(
                "Já existe um veículo com essa placa."
            )

    def _validar_marca(
        self,
        veiculo: Veiculo,
    ) -> None:

        if not (
            veiculo.marca or ""
        ).strip():
            raise ValueError(
                "Informe a marca."
            )

    def _validar_modelo(
        self,
        veiculo: Veiculo,
    ) -> None:

        if not (
            veiculo.modelo or ""
        ).strip():
            raise ValueError(
                "Informe o modelo."
            )

    def _validar_tipo(
        self,
        veiculo: Veiculo,
    ) -> None:

        if not (
            veiculo.tipo or ""
        ).strip():
            raise ValueError(
                "Informe o tipo."
            )

    def _validar_ano(
        self,
        veiculo: Veiculo,
    ) -> None:

        if veiculo.ano is None:
            return

        ano_atual = datetime.now().year + 1

        if (
            veiculo.ano < 1950
            or veiculo.ano > ano_atual
        ):
            raise ValueError(
                "Ano do veículo inválido."
            )

    def _validar_capacidade(
        self,
        veiculo: Veiculo,
    ) -> None:

        if veiculo.capacidade is None:
            return

        if veiculo.capacidade <= 0:
            raise ValueError(
                "A capacidade deve ser maior que zero."
            )

    def _validar_status(
        self,
        veiculo: Veiculo,
    ) -> None:

        if not veiculo.status:
            veiculo.status = (
                STATUS_VEICULO_DISPONIVEL
            )

        veiculo.status = (
            veiculo.status.strip().upper()
        )

        if (
            veiculo.status
            not in STATUS_VEICULOS
        ):
            raise ValueError(
                "Status do veículo inválido."
            )