from models import Motorista
from services import MotoristaService


class MotoristaController:
    """Controller responsável pelas operações dos motoristas."""

    def __init__(
        self,
        service: MotoristaService | None = None,
    ) -> None:
        self.service = (
            service
            or MotoristaService()
        )

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def listar(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Motorista]:

        return self.service.listar(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
            limite=limite,
            pagina=pagina,
        )

    def listar_ativos(
        self,
    ) -> list[Motorista]:

        return self.service.listar_ativos()

    def buscar_por_id(
        self,
        motorista_id: int,
    ) -> Motorista | None:

        return self.service.buscar_por_id(
            motorista_id,
        )

    def buscar_por_cnh(
        self,
        cnh: str,
    ) -> Motorista | None:

        return self.service.buscar_por_cnh(
            cnh,
        )

    def buscar_por_telefone(
        self,
        telefone: str,
    ) -> Motorista | None:

        return self.service.buscar_por_telefone(
            telefone,
        )

    # ==========================================================
    # DUPLICIDADE
    # ==========================================================

    def telefone_existe(
        self,
        telefone: str,
        ignorar_id: int | None = None,
    ) -> bool:

        return self.service.telefone_existe(
            telefone,
            ignorar_id=ignorar_id,
        )

    def cnh_existe(
        self,
        cnh: str,
        ignorar_id: int | None = None,
    ) -> bool:

        return self.service.cnh_existe(
            cnh,
            ignorar_id=ignorar_id,
        )

    # ==========================================================
    # CRUD
    # ==========================================================

    def cadastrar(
        self,
        motorista: Motorista,
    ) -> tuple[bool, str]:

        return self.service.cadastrar(
            motorista,
        )

    def atualizar(
        self,
        motorista: Motorista,
    ) -> tuple[bool, str]:

        return self.service.atualizar(
            motorista,
        )

    def excluir(
        self,
        motorista_id: int,
    ) -> tuple[bool, str]:

        return self.service.excluir(
            motorista_id,
        )

    def reativar(
        self,
        motorista_id: int,
    ) -> tuple[bool, str]:

        return self.service.reativar(
            motorista_id,
        )

    def quantidade(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
    ) -> int:

        return self.service.quantidade(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
        )