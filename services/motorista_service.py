from models import Motorista
from repositories.motorista_repository import (
    MotoristaRepository,
)


class MotoristaService:
    """Regras de negócio relacionadas aos motoristas."""

    def __init__(
        self,
        repository: MotoristaRepository | None = None,
    ) -> None:
        self.repository = (
            repository
            or MotoristaRepository()
        )

    # ==========================================================
    # TRATAMENTO DE ERROS
    # ==========================================================

    @staticmethod
    def _erro_operacao(
        operacao: str,
        erro: Exception,
    ) -> tuple[bool, str]:
        """Padroniza o tratamento de erros inesperados."""

        print(
            f"Erro inesperado ao {operacao} motorista:",
            erro,
        )

        return (
            False,
            f"Não foi possível {operacao} o motorista.",
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
        """Retorna motoristas com filtros opcionais."""

        return self.repository.listar(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
            limite=limite,
            pagina=pagina,
        )

    def listar_ativos(
        self,
    ) -> list[Motorista]:
        """Retorna somente os motoristas ativos."""

        return self.repository.listar_ativos()

    def buscar_por_id(
        self,
        motorista_id: int,
    ) -> Motorista | None:
        """Busca um motorista pelo identificador."""

        return self.repository.buscar_por_id(
            motorista_id,
        )

    def buscar_por_cnh(
        self,
        cnh: str,
    ) -> Motorista | None:
        """Busca um motorista pela CNH."""

        return self.repository.buscar_por_cnh(
            cnh,
        )

    def buscar_por_telefone(
        self,
        telefone: str,
    ) -> Motorista | None:
        """Busca um motorista pelo telefone celular."""

        return self.repository.buscar_por_telefone(
            telefone,
        )

    # ==========================================================
    # VERIFICAÇÃO DE DUPLICIDADE
    # ==========================================================

    def telefone_existe(
        self,
        telefone: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe motorista com o telefone."""

        return self.repository.telefone_existe(
            telefone,
            ignorar_id=ignorar_id,
        )

    def cnh_existe(
        self,
        cnh: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe motorista com a CNH."""

        return self.repository.cnh_existe(
            cnh,
            ignorar_id=ignorar_id,
        )

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        motorista: Motorista,
    ) -> tuple[bool, str]:
        """Cadastra um novo motorista."""

        try:
            self.repository.cadastrar(
                motorista,
            )

        except ValueError as erro:
            return (
                False,
                str(erro),
            )

        except Exception as erro:
            return self._erro_operacao(
                "cadastrar",
                erro,
            )

        return (
            True,
            "Motorista cadastrado com sucesso.",
        )

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def atualizar(
        self,
        motorista: Motorista,
    ) -> tuple[bool, str]:
        """Atualiza um motorista existente."""

        try:
            self.repository.atualizar(
                motorista,
            )

        except ValueError as erro:
            return (
                False,
                str(erro),
            )

        except Exception as erro:
            return self._erro_operacao(
                "atualizar",
                erro,
            )

        return (
            True,
            "Motorista atualizado com sucesso.",
        )

    # ==========================================================
    # EXCLUSÃO LÓGICA E REATIVAÇÃO
    # ==========================================================

    def excluir(
        self,
        motorista_id: int,
    ) -> tuple[bool, str]:
        """Realiza a exclusão lógica do motorista."""

        try:
            excluido = self.repository.excluir(
                motorista_id,
            )

        except Exception as erro:
            return self._erro_operacao(
                "excluir",
                erro,
            )

        if not excluido:
            return (
                False,
                "Motorista não encontrado ou já está inativo.",
            )

        return (
            True,
            "Motorista excluído com sucesso.",
        )

    def reativar(
        self,
        motorista_id: int,
    ) -> tuple[bool, str]:
        """Reativa um motorista desativado."""

        try:
            reativado = self.repository.reativar(
                motorista_id,
            )

        except Exception as erro:
            return self._erro_operacao(
                "reativar",
                erro,
            )

        if not reativado:
            return (
                False,
                "Motorista não encontrado ou já está ativo.",
            )

        return (
            True,
            "Motorista reativado com sucesso.",
        )

    # ==========================================================
    # CONTAGEM
    # ==========================================================

    def quantidade(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
    ) -> int:
        """Retorna a quantidade de motoristas."""

        return self.repository.quantidade(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
        )