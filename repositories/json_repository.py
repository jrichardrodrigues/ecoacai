import json
from pathlib import Path


class JsonRepository:

    def __init__(self):

        self.arquivo = Path("data/database.json")

        self._criar_banco()

    def _criar_banco(self):

        if not self.arquivo.exists():

            self.arquivo.parent.mkdir(exist_ok=True)

            with open(self.arquivo, "w", encoding="utf8") as f:

                json.dump(
                    {
                        "usuarios": [],
                        "solicitacoes": []
                    },
                    f,
                    indent=4,
                    ensure_ascii=False
                )

    def carregar(self):

        with open(self.arquivo, "r", encoding="utf8") as f:

            return json.load(f)

    def salvar(self, dados):

        with open(self.arquivo, "w", encoding="utf8") as f:

            json.dump(
                dados,
                f,
                indent=4,
                ensure_ascii=False
            )