def texto_limpo(valor: str) -> str:
    return str(valor or "").strip()


def titulo(valor: str) -> str:
    return texto_limpo(valor).title()


def somente_digitos(valor: str) -> str:
    return "".join(caractere for caractere in str(valor or "") if caractere.isdigit())