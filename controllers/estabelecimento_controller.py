from models import Estabelecimento
from services import (
    EstabelecimentoService,
    EstabelecimentoValidationService,
)


class EstabelecimentoController:
    """Coordena as operações dos estabelecimentos."""

    def __init__(self) -> None:
        self.estabelecimento_service = EstabelecimentoService()

        self.validation_service = EstabelecimentoValidationService(
            self.estabelecimento_service,
        )

    def listar_estabelecimentos(
        self,
        pesquisa: str = "",
        somente_ativos: bool = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Estabelecimento]:
        """Lista os estabelecimentos."""

        return self.estabelecimento_service.listar(
            pesquisa=pesquisa,
            somente_ativos=somente_ativos,
            limite=limite,
            pagina=pagina,
        )

    def buscar_estabelecimento_por_id(
        self,
        estabelecimento_id: int,
    ) -> Estabelecimento | None:
        """Busca um estabelecimento pelo identificador."""

        return self.estabelecimento_service.buscar_por_id(
            estabelecimento_id,
        )

    def cadastrar_estabelecimento(
        self,
        dados: dict,
    ) -> tuple[bool, str]:
        """Valida e cadastra um estabelecimento."""

        sucesso, mensagem, dados_normalizados = (
            self.validation_service.validar(dados)
        )

        if not sucesso:
            return False, mensagem

        estabelecimento = Estabelecimento(
            nome=dados_normalizados["nome"],
            cpf=dados_normalizados["cpf"],
            email=dados_normalizados["email"],
            celular=dados_normalizados["celular"],
            endereco=dados_normalizados["endereco"],
            bairro=dados_normalizados["bairro"],
            setor=dados_normalizados["setor"],
        )

        return self.estabelecimento_service.cadastrar(
            estabelecimento,
        )

    def _atualizar_dados(
        self,
        estabelecimento: Estabelecimento,
        dados: dict,
    ) -> None:
        """Atualiza os dados de um estabelecimento."""

        estabelecimento.nome = dados["nome"]
        estabelecimento.cpf = dados["cpf"]
        estabelecimento.email = dados["email"]
        estabelecimento.celular = dados["celular"]
        estabelecimento.endereco = dados["endereco"]
        estabelecimento.bairro = dados["bairro"]
        estabelecimento.setor = dados["setor"]

    def atualizar_estabelecimento(
        self,
        estabelecimento_id: int,
        dados: dict,
    ) -> tuple[bool, str]:
        """Valida e atualiza um estabelecimento."""

        estabelecimento = (
            self.estabelecimento_service.buscar_por_id(
                estabelecimento_id,
            )
        )

        if estabelecimento is None:
            return False, "Estabelecimento não encontrado."

        sucesso, mensagem, dados_normalizados = (
            self.validation_service.validar(
                dados,
                ignorar_id=estabelecimento_id,
            )
        )

        if not sucesso:
            return False, mensagem

        self._atualizar_dados(
            estabelecimento,
            dados_normalizados,
        )

        return self.estabelecimento_service.atualizar(
            estabelecimento,
        )

    def quantidade_estabelecimentos(self) -> int:
        """Retorna a quantidade de estabelecimentos."""

        return self.estabelecimento_service.quantidade()

    def excluir_estabelecimento(
        self,
        estabelecimento_id: int,
    ) -> tuple[bool, str]:
        """Desativa um estabelecimento."""

        return self.estabelecimento_service.excluir(
            estabelecimento_id,
        )