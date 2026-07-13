import re


def email_valido(email: str) -> bool:
    padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(padrao, email or ""))


def campo_obrigatorio(valor: str) -> bool:
    return bool(str(valor or "").strip())


def numero_inteiro_positivo(valor) -> bool:
    try:
        return int(valor) > 0
    except (TypeError, ValueError):
        return False