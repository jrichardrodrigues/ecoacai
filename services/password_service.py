import re

from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)


class PasswordService:
    """
    Valida, gera e verifica hashes de senha usando Argon2.
    """

    def __init__(self):
        self._hasher = PasswordHasher()

    @staticmethod
    def validar_regra(senha: str) -> tuple[bool, str]:
        senha = str(senha or "")

        if len(senha) < 9:
            return False, "A senha deve possuir pelo menos 9 caracteres."

        if not re.search(r"[A-Z]", senha):
            return False, "A senha deve conter pelo menos uma letra maiúscula."

        if not re.search(r"[a-z]", senha):
            return False, "A senha deve conter pelo menos uma letra minúscula."

        if not re.search(r"\d", senha):
            return False, "A senha deve conter pelo menos um número."

        if not re.search(r"[^A-Za-z0-9]", senha):
            return False, "A senha deve conter pelo menos um caractere especial."

        if any(caractere.isspace() for caractere in senha):
            return False, "A senha não pode conter espaços."

        return True, "Senha válida."

    @classmethod
    def validar_confirmacao(
        cls,
        senha: str,
        confirmar_senha: str,
    ) -> tuple[bool, str]:
        valida, mensagem = cls.validar_regra(senha)

        if not valida:
            return False, mensagem

        if senha != confirmar_senha:
            return False, "As senhas não coincidem."

        return True, "Senha válida."

    def gerar_hash(self, senha: str) -> str:
        valida, mensagem = self.validar_regra(senha)

        if not valida:
            raise ValueError(mensagem)

        return self._hasher.hash(senha)

    def verificar(self, senha: str, senha_hash: str) -> bool:
        if not senha or not senha_hash:
            return False

        try:
            return self._hasher.verify(
                senha_hash,
                senha,
            )

        except (
            VerifyMismatchError,
            VerificationError,
            InvalidHashError,
        ):
            return False

    def precisa_rehash(self, senha_hash: str) -> bool:
        try:
            return self._hasher.check_needs_rehash(senha_hash)

        except InvalidHashError:
            return True