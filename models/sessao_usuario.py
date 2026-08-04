from dataclasses import dataclass

from models.organizacao import Organizacao
from models.perfil import Perfil
from models.usuario import Usuario


@dataclass
class SessaoUsuario:
    """Representa o contexto completo do usuário autenticado."""

    usuario: Usuario
    perfil: Perfil
    organizacao: Organizacao | None = None

    @property
    def possui_organizacao(self) -> bool:
        return self.organizacao is not None

    @property
    def eh_gestor(self) -> bool:
        return self.perfil.codigo == "GESTOR"

    @property
    def eh_gerador(self) -> bool:
        return self.perfil.codigo == "GERADOR"

    @property
    def eh_empresa_parceira(self) -> bool:
        return self.perfil.codigo == "EMPRESA_PARCEIRA"