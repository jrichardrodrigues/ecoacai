import re


class CpfService:

    @staticmethod
    def limpar(cpf: str) -> str:
        return re.sub(r"\D", "", cpf or "")

    @staticmethod
    def remover_formatacao(cpf: str) -> str:
        return "".join(filter(str.isdigit, cpf))

    @staticmethod
    def formatar(cpf: str) -> str:
        cpf = CpfService.limpar(cpf)[:11]

        if len(cpf) <= 3:
            return cpf

        if len(cpf) <= 6:
            return f"{cpf[:3]}.{cpf[3:]}"

        if len(cpf) <= 9:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"

        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @staticmethod
    def validar(cpf: str) -> bool:
        cpf = CpfService.limpar(cpf)

        if len(cpf) != 11:
            return False

        if cpf == cpf[0] * 11:
            return False

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        digito1 = 0 if resto == 10 else resto

        if digito1 != int(cpf[9]):
            return False

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        digito2 = 0 if resto == 10 else resto

        return digito2 == int(cpf[10])

