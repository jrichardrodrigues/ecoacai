import re

from .base_validated_field import BaseValidatedField


class NameField(BaseValidatedField):

    PALAVRAS_MINUSCULAS = {
        "e",
        "da",
        "das",
        "de",
        "do",
        "dos",
        "del",
        "della",
        "di",
        "van",
        "von",
    }

    def __init__(
            self,
            on_change=None,
    ):
        super().__init__(
            label="Nome do Proprietário/Responsável",
            hint_text="Digite o nome completo",
            max_length=80,
            on_change=on_change,
        )

    @staticmethod
    def normalizar_espacos(valor: str) -> str:
        return " ".join(str(valor or "").split())

    @staticmethod
    def formatar_nome(valor: str) -> str:
        valor = NameField.normalizar_espacos(valor)

        palavras_formatadas = []

        for indice, palavra in enumerate(valor.split()):
            palavra_minuscula = palavra.lower()

            if (
                    indice > 0
                    and palavra_minuscula
                    in NameField.PALAVRAS_MINUSCULAS
            ):
                palavras_formatadas.append(
                    palavra_minuscula
                )
            else:
                palavras_formatadas.append(
                    palavra_minuscula.capitalize()
                )

        return " ".join(palavras_formatadas)

    def validar(self):
        nome = self.normalizar_espacos(self.value)

        if not nome:
            self.limpar_mensagem()
            return

        if any(caractere.isdigit() for caractere in nome):
            self.erro("O nome não pode conter números.")
            return

        padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$"

        if not re.fullmatch(padrao, nome):
            self.erro("O nome contém caracteres inválidos.")
            return

        if len(nome) < 5:
            self.erro("Digite um nome com pelo menos 5 caracteres.")
            return

        palavras = nome.split()

        if len(palavras) < 2:
            self.erro("Informe o nome e o sobrenome.")
            return

        for palavra in palavras:

            palavra = palavra.lower()

            if palavra in NameField.PALAVRAS_MINUSCULAS:
                continue

            if len(palavra) < 2:
                self.erro(
                    "Há uma palavra muito curta no nome."
                )
                return

        self.sucesso("Nome válido.")

    def _ao_sair(self, e):
        self.value = e.control.value or ""

        nome_formatado = self.formatar_nome(self.value)

        self.value = nome_formatado
        self.control.value = nome_formatado

        self.validar()
        self._atualizar()