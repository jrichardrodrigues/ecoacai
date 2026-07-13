import re

import httpx


class CepService:
    BASE_URL = "https://viacep.com.br/ws"

    @staticmethod
    def somente_digitos(cep: str) -> str:
        return re.sub(r"\D", "", str(cep or ""))

    @classmethod
    def formatar(cls, cep: str) -> str:
        digitos = cls.somente_digitos(cep)[:8]

        if len(digitos) <= 5:
            return digitos

        return f"{digitos[:5]}-{digitos[5:]}"

    @classmethod
    def validar_formato(cls, cep: str) -> tuple[bool, str]:
        digitos = cls.somente_digitos(cep)

        if not digitos:
            return False, "Informe o CEP."

        if len(digitos) != 8:
            return False, "O CEP deve possuir 8 números."

        return True, ""

    @classmethod
    def consultar(cls, cep: str) -> tuple[bool, str, dict]:
        valido, mensagem = cls.validar_formato(cep)

        if not valido:
            return False, mensagem, {}

        cep_normalizado = cls.somente_digitos(cep)
        url = f"{cls.BASE_URL}/{cep_normalizado}/json/"

        try:
            resposta = httpx.get(
                url,
                timeout=8.0,
                follow_redirects=True,
            )

            resposta.raise_for_status()
            dados = resposta.json()

        except httpx.TimeoutException:
            return (
                False,
                "A consulta do CEP demorou demais. Tente novamente.",
                {},
            )

        except httpx.HTTPError:
            return (
                False,
                "Não foi possível consultar o CEP no momento.",
                {},
            )

        except ValueError:
            return (
                False,
                "O serviço de CEP retornou uma resposta inválida.",
                {},
            )

        if dados.get("erro") is True:
            return False, "CEP não encontrado.", {}

        cidade = str(dados.get("localidade") or "").strip()
        uf = str(dados.get("uf") or "").strip().upper()

        # Proteção para respostas inconsistentes da API,
        # como CEP retornado com todos os campos vazios.
        if not cidade or not uf:
            return False, "CEP não encontrado.", {}

        endereco = {
            "cep": cls.formatar(
                dados.get("cep") or cep_normalizado
            ),
            "logradouro": str(
                dados.get("logradouro") or ""
            ).strip(),
            "complemento": str(
                dados.get("complemento") or ""
            ).strip(),
            "bairro": str(
                dados.get("bairro") or ""
            ).strip(),
            "cidade": cidade,
            "uf": uf,
        }

        return True, "CEP localizado.", endereco