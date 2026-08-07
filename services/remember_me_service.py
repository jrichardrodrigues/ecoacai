from __future__ import annotations

import json

from config.settings import DATA_DIR


class RememberMeService:
    """Gerencia a preferência local 'Lembrar-me'."""

    ARQUIVO = DATA_DIR / "remember_me.json"

    @classmethod
    def carregar_cpf(cls) -> str:
        if not cls.ARQUIVO.exists():
            return ""

        try:
            dados = json.loads(
                cls.ARQUIVO.read_text(encoding="utf-8")
            )

            return str(
                dados.get("cpf") or ""
            ).strip()

        except (OSError, ValueError, TypeError):
            return ""

    @classmethod
    def salvar_cpf(
        cls,
        cpf: str,
    ) -> None:
        cls.ARQUIVO.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cls.ARQUIVO.write_text(
            json.dumps(
                {
                    "cpf": cpf,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    @classmethod
    def limpar(cls) -> None:
        try:
            cls.ARQUIVO.unlink(
                missing_ok=True,
            )
        except OSError:
            pass