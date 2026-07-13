import re


class EmailService:
    DOMINIOS_COMUNS = {
        "gmail.com",
        "hotmail.com",
        "outlook.com",
        "yahoo.com",
        "icloud.com",
        "live.com",
        "bol.com.br",
        "uol.com.br",
        "terra.com.br",
    }

    CORRECOES_DOMINIOS = {
        "gmail.con": "gmail.com",
        "gmai.com": "gmail.com",
        "gmial.com": "gmail.com",
        "gmail.co": "gmail.com",
        "hotmail.con": "hotmail.com",
        "hotmai.com": "hotmail.com",
        "hotmal.com": "hotmail.com",
        "outlook.con": "outlook.com",
        "outlok.com": "outlook.com",
        "yahoo.con": "yahoo.com",
        "icloud.con": "icloud.com",
    }

    @staticmethod
    def normalizar(email: str) -> str:
        return str(email or "").strip().lower()

    @classmethod
    def validar(cls, email: str) -> tuple[bool, str]:
        email = cls.normalizar(email)

        if not email:
            return False, "Informe o e-mail."

        if " " in email:
            return False, "O e-mail não pode conter espaços."

        if len(email) > 254:
            return False, "O e-mail é muito longo."

        if email.count("@") != 1:
            return False, "O e-mail deve conter um único @."

        usuario, dominio = email.rsplit("@", 1)

        if not usuario:
            return False, "Informe o nome antes do @."

        if not dominio:
            return False, "Informe o domínio depois do @."

        if len(usuario) > 64:
            return False, "A parte anterior ao @ é muito longa."

        if usuario.startswith(".") or usuario.endswith("."):
            return False, "O e-mail não pode começar ou terminar com ponto."

        if ".." in usuario:
            return False, "O e-mail não pode conter pontos consecutivos."

        padrao_usuario = r"^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+$"

        if not re.fullmatch(padrao_usuario, usuario, re.IGNORECASE):
            return False, "O e-mail contém caracteres inválidos."

        if dominio in cls.CORRECOES_DOMINIOS:
            sugestao = cls.CORRECOES_DOMINIOS[dominio]
            return False, f"Domínio possivelmente incorreto. Você quis dizer {sugestao}?"

        if "." not in dominio:
            return False, "O domínio deve possuir uma extensão, como .com."

        if dominio.startswith(".") or dominio.endswith("."):
            return False, "Domínio inválido."

        if ".." in dominio:
            return False, "O domínio não pode conter pontos consecutivos."

        partes_dominio = dominio.split(".")

        for parte in partes_dominio:
            if not parte:
                return False, "Domínio inválido."

            if parte.startswith("-") or parte.endswith("-"):
                return False, "Domínio inválido."

            if not re.fullmatch(r"[a-z0-9-]+", parte, re.IGNORECASE):
                return False, "O domínio contém caracteres inválidos."

        extensao = partes_dominio[-1]

        if len(extensao) < 2 or not extensao.isalpha():
            return False, "A extensão do domínio é inválida."

        return True, "E-mail com formato válido."