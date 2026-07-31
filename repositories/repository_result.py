from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RepositoryResult:
    """
    Resultado padronizado retornado pelos repositórios.

    Attributes:
        sucesso:
            Indica se a operação foi realizada com sucesso.

        mensagem:
            Mensagem amigável destinada ao Controller ou à View.

        dados:
            Objeto retornado pela operação.
            Pode ser um dict, list, dataclass ou None.
    """

    sucesso: bool
    mensagem: str = ""
    dados: Any = None

    @property
    def falhou(self) -> bool:
        """Retorna True quando a operação não foi bem-sucedida."""
        return not self.sucesso