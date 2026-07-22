from models import Estabelecimento
from repositories.estabelecimento_repository import (
    EstabelecimentoRepository,
)


class EstabelecimentoService:
    """Regras de negócio relacionadas aos estabelecimentos."""

    def __init__(
        self,
        repository: EstabelecimentoRepository | None = None,
    ) -> None:
        self.repository = (
            repository
            or EstabelecimentoRepository()
        )

    def _erro_operacao(
            self,
            operacao: str,
            erro: Exception,
    ) -> tuple[bool, str]:
        """Padroniza o tratamento de erros inesperados."""

        print(
            f"Erro inesperado ao {operacao} estabelecimento:",
            erro,
        )

        return (
            False,
            f"Não foi possível {operacao} o estabelecimento.",
        )

    def listar(
        self,
        pesquisa: str = "",
        somente_ativos: bool = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Estabelecimento]:
        """Retorna estabelecimentos com filtros opcionais."""

        return self.repository.listar(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
            limite=limite,
            pagina=pagina,
        )

    def buscar_por_id(
        self,
        estabelecimento_id: int,
    ) -> Estabelecimento | None:
        """Busca um estabelecimento pelo identificador."""

        return self.repository.buscar_por_id(
            estabelecimento_id,
        )

    def buscar_por_cpf(
        self,
        cpf: str,
    ) -> Estabelecimento | None:
        """Busca um estabelecimento pelo CPF."""

        return self.repository.buscar_por_cpf(
            cpf,
        )

    def cpf_existe(
        self,
        cpf: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe estabelecimento com o CPF."""

        return self.repository.cpf_existe(
            cpf,
            ignorar_id=ignorar_id,
        )

    def email_existe(
        self,
        email: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe estabelecimento com o e-mail."""

        return self.repository.email_existe(
            email,
            ignorar_id=ignorar_id,
        )

    def celular_existe(
        self,
        celular: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe estabelecimento com o celular."""

        return self.repository.celular_existe(
            celular,
            ignorar_id=ignorar_id,
        )

    def cadastrar(
        self,
        estabelecimento: Estabelecimento,
    ) -> tuple[bool, str]:
        """Cadastra um novo estabelecimento."""

        try:
            self.repository.cadastrar(
                estabelecimento,
            )

        except ValueError as erro:
            return False, str(erro)


        except Exception as erro:

            return self._erro_operacao(

                "cadastrar",

                erro,

            )

        return (
            True,
            "Estabelecimento cadastrado com sucesso.",
        )

    def atualizar(
        self,
        estabelecimento: Estabelecimento,
    ) -> tuple[bool, str]:
        """Atualiza um estabelecimento existente."""

        try:
            self.repository.atualizar(
                estabelecimento,
            )

        except ValueError as erro:
            return False, str(erro)


        except Exception as erro:

            return self._erro_operacao(

                "atualizar",

                erro,

            )

        return (
            True,
            "Estabelecimento atualizado com sucesso.",
        )

    def excluir(
        self,
        estabelecimento_id: int,
    ) -> tuple[bool, str]:
        """Realiza exclusão lógica do estabelecimento."""

        try:
            excluido = self.repository.excluir(
                estabelecimento_id,
            )


        except Exception as erro:

            return self._erro_operacao(

                "excluir",

                erro,

            )

        if not excluido:
            return (
                False,
                "Estabelecimento não encontrado.",
            )

        return (
            True,
            "Estabelecimento excluído com sucesso.",
        )

    def reativar(
        self,
        estabelecimento_id: int,
    ) -> tuple[bool, str]:
        """Reativa um estabelecimento desativado."""

        try:
            reativado = self.repository.reativar(
                estabelecimento_id,
            )


        except Exception as erro:

            return self._erro_operacao(

                "reativar",

                erro,

            )

        if not reativado:
            return (
                False,
                "Estabelecimento não encontrado "
                "ou já está ativo.",
            )

        return (
            True,
            "Estabelecimento reativado com sucesso.",
        )

    def quantidade(
        self,
        pesquisa: str = "",
        somente_ativos: bool = True,
    ) -> int:
        """Retorna a quantidade de estabelecimentos."""

        return self.repository.quantidade(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
        )