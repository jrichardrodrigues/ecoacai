import re


class PhoneService:
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

    @staticmethod
    def somente_digitos(celular: str) -> str:
        return re.sub(r"\D", "", str(celular or ""))

    @classmethod
    def formatar(cls, celular: str) -> str:
        digitos = cls.somente_digitos(celular)[:11]

        if len(digitos) <= 2:
            return digitos

        if len(digitos) <= 7:
            return f"({digitos[:2]}) {digitos[2:]}"

        return (
            f"({digitos[:2]}) "
            f"{digitos[2:7]}-{digitos[7:]}"
        )

    @classmethod
    def validar(cls, celular: str) -> tuple[bool, str]:
        digitos = cls.somente_digitos(celular)

        if not digitos:
            return False, "Informe o celular/WhatsApp."

        if len(digitos) != 11:
            return False, "Informe DDD e celular com 11 dígitos."

        ddd = digitos[:2]
        numero = digitos[2:]

        if ddd not in cls.DDD_VALIDOS:
            return False, "DDD inválido."

        if not numero.startswith("9"):
            return False, "O celular deve começar com 9."

        if numero == numero[0] * len(numero):
            return False, "Número de celular inválido."

        return True, "Celular válido."