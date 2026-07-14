from utils.formatters import somente_digitos

from .base_validated_field import BaseValidatedField


class PhoneField(BaseValidatedField):
    DDD_VALIDOS = {
        "11", "12", "13", "14", "15", "16", "17", "18", "19",
        "21", "22", "24",
        "27", "28",
        "31", "32", "33", "34", "35", "37", "38",
        "41", "42", "43", "44", "45", "46",
        "47", "48", "49",
        "51", "53", "54", "55",
        "61", "62", "63", "64", "65", "66", "67", "68", "69",
        "71", "73", "74", "75", "77", "79",
        "81", "82", "83", "84", "85", "86", "87", "88", "89",
        "91", "92", "93", "94", "95", "96", "97", "98", "99",
    }

    def __init__(
            self,
            usuario_service=None,
            ignorar_id: int = 0,
    ):
        super().__init__(
            label="Celular/WhatsApp",
            hint_text="(91) 98888-7777",
            max_length=15,
        )

        self.usuario_service = usuario_service
        self.ignorar_id = ignorar_id

    @staticmethod
    def formatar(valor: str) -> str:
        digitos = somente_digitos(valor)[:11]

        if not digitos:
            return ""

        if len(digitos) <= 2:
            return f"({digitos}"

        if len(digitos) <= 6:
            return f"({digitos[:2]}) {digitos[2:]}"

        if len(digitos) <= 10:
            return (
                f"({digitos[:2]}) "
                f"{digitos[2:6]}-"
                f"{digitos[6:]}"
            )

        return (
            f"({digitos[:2]}) "
            f"{digitos[2:7]}-"
            f"{digitos[7:]}"
        )

    def validar(self):
        celular_formatado = self.formatar(self.value)

        if celular_formatado != self.control.value:
            self.control.value = celular_formatado
            self.value = celular_formatado

        digitos = somente_digitos(celular_formatado)

        if not digitos:
            self.limpar_mensagem()
            return

        if len(digitos) < 10:
            self.erro("Digite o DDD e o número completo.")
            return

        if len(digitos) not in (10, 11):
            self.erro("Número de telefone inválido.")
            return

        ddd = digitos[:2]
        numero = digitos[2:]

        if ddd not in self.DDD_VALIDOS:
            self.erro("DDD inválido.")
            return

        if numero == numero[0] * len(numero):
            self.erro("Número de telefone inválido.")
            return

        if len(numero) == 9:
            if not numero.startswith("9"):
                self.erro(
                    "Celular com 9 dígitos deve começar com 9."
                )
                return

        elif len(numero) == 8:
            if numero[0] not in ("2", "3", "4", "5"):
                self.erro("Número de telefone fixo inválido.")
                return

        if (
            self.usuario_service is not None
            and self.usuario_service.celular_existe(
                celular_formatado,
                ignorar_id=self.ignorar_id,
            )
        ):
            self.erro("Celular já cadastrado.")
            return

        self.sucesso("Número válido.")