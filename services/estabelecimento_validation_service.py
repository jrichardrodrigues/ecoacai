from services.cpf_service import CpfService
from services.email_service import EmailService
from utils.formatters import somente_digitos
from utils.validators import campo_obrigatorio


class EstabelecimentoValidationService:
    """Valida e normaliza dados de estabelecimentos."""

    CAMPOS_OBRIGATORIOS = {
        "nome": "Nome/Responsável",
        "cpf": "CPF",
        "email": "E-mail",
        "celular": "Celular",
        "endereco": "Endereço",
        "bairro": "Bairro",
        "setor": "Setor",
    }

    def __init__(
        self,
        estabelecimento_service,
    ) -> None:
        self.estabelecimento_service = estabelecimento_service

    def validar(
        self,
        dados: dict,
        ignorar_id: int | None = None,
    ) -> tuple[bool, str, dict]:
        """Valida e normaliza os dados recebidos."""

        dados_normalizados = self._normalizar_dados(dados)

        sucesso, mensagem = (
            self._validar_campos_obrigatorios(
                dados_normalizados,
            )
        )

        if not sucesso:
            return False, mensagem, {}

        sucesso, mensagem = self._validar_cpf(
            dados_normalizados["cpf"],
            ignorar_id,
        )

        if not sucesso:
            return False, mensagem, {}

        sucesso, mensagem = self._validar_email(
            dados_normalizados["email"],
            ignorar_id,
        )

        if not sucesso:
            return False, mensagem, {}

        sucesso, mensagem = self._validar_celular(
            dados_normalizados["celular"],
            ignorar_id,
        )

        if not sucesso:
            return False, mensagem, {}

        return (
            True,
            "Dados válidos.",
            dados_normalizados,
        )

    def _normalizar_dados(
        self,
        dados: dict,
    ) -> dict[str, str]:
        return {
            "nome": str(
                dados.get("nome") or "",
            ).strip(),
            "cpf": CpfService.formatar(
                dados.get("cpf") or "",
            ),
            "email": EmailService.normalizar(
                dados.get("email") or "",
            ),
            "celular": str(
                dados.get("celular") or "",
            ).strip(),
            "endereco": str(
                dados.get("endereco") or "",
            ).strip(),
            "bairro": str(
                dados.get("bairro") or "",
            ).strip(),
            "setor": str(
                dados.get("setor") or "",
            ).strip(),
        }

    def _validar_campos_obrigatorios(
        self,
        dados: dict[str, str],
    ) -> tuple[bool, str]:
        for campo, nome_amigavel in (
            self.CAMPOS_OBRIGATORIOS.items()
        ):
            if not campo_obrigatorio(
                dados.get(campo),
            ):
                return (
                    False,
                    f"O campo '{nome_amigavel}' é obrigatório.",
                )

        return True, ""

    def _validar_cpf(
        self,
        cpf: str,
        ignorar_id: int | None,
    ) -> tuple[bool, str]:
        if not CpfService.validar(cpf):
            return False, "CPF inválido."

        if self.estabelecimento_service.cpf_existe(
            cpf,
            ignorar_id=ignorar_id,
        ):
            return False, "CPF já cadastrado."

        return True, ""

    def _validar_email(
        self,
        email: str,
        ignorar_id: int | None,
    ) -> tuple[bool, str]:
        email_valido, mensagem = EmailService.validar(
            email,
        )

        if not email_valido:
            return False, mensagem

        if self.estabelecimento_service.email_existe(
            email,
            ignorar_id=ignorar_id,
        ):
            return False, "E-mail já cadastrado."

        return True, ""

    def _validar_celular(
        self,
        celular: str,
        ignorar_id: int | None,
    ) -> tuple[bool, str]:
        digitos = somente_digitos(celular)

        if len(digitos) not in (10, 11):
            return (
                False,
                "Informe um celular válido com DDD.",
            )

        ddd = digitos[:2]
        numero = digitos[2:]

        ddds_validos = {
            "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "21", "22", "24", "27", "28",
            "31", "32", "33", "34", "35", "37", "38",
            "41", "42", "43", "44", "45", "46", "47",
            "48", "49", "51", "53", "54", "55", "61",
            "62", "63", "64", "65", "66", "67", "68",
            "69", "71", "73", "74", "75", "77", "79",
            "81", "82", "83", "84", "85", "86", "87",
            "88", "89", "91", "92", "93", "94", "95",
            "96", "97", "98", "99",
        }

        if ddd not in ddds_validos:
            return False, "DDD inválido."

        if (
            len(numero) == 9
            and not numero.startswith("9")
        ):
            return (
                False,
                "Celular com 9 dígitos deve começar com 9.",
            )

        if (
            len(numero) == 8
            and numero[0] not in ("2", "3", "4", "5")
        ):
            return False, "Número de telefone fixo inválido."

        if numero == numero[0] * len(numero):
            return False, "Número de telefone inválido."

        if self.estabelecimento_service.celular_existe(
            celular,
            ignorar_id=ignorar_id,
        ):
            return False, "Celular já cadastrado."

        return True, ""