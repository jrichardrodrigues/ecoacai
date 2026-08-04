from __future__ import annotations

from models import Organizacao, Perfil, Usuario
from models.sessao_usuario import SessaoUsuario
from repositories import PerfilRepository, UsuarioRepository
from repositories.organizacao_repository import OrganizacaoRepository


class SessaoService:
    """
    Gerencia a sessão do usuário autenticado.

    A sessão mantém em memória:
    - o usuário autenticado;
    - o perfil de acesso;
    - a organização vinculada, quando existir.
    """

    def __init__(
        self,
        usuario_repository: UsuarioRepository | None = None,
        perfil_repository: PerfilRepository | None = None,
        organizacao_repository: OrganizacaoRepository | None = None,
    ) -> None:
        self.usuario_repository = (
            usuario_repository or UsuarioRepository()
        )
        self.perfil_repository = (
            perfil_repository or PerfilRepository()
        )
        self.organizacao_repository = (
            organizacao_repository or OrganizacaoRepository()
        )

        self._sessao_atual: SessaoUsuario | None = None

    # ==========================================================
    # ABERTURA DA SESSÃO
    # ==========================================================

    def abrir_sessao(
        self,
        usuario: Usuario,
    ) -> SessaoUsuario:
        """
        Cria a sessão completa a partir do usuário autenticado.

        O perfil é obrigatório.
        A organização poderá ser nula durante o primeiro acesso
        do Gerador.
        """

        if usuario.id is None:
            raise ValueError(
                "O usuário autenticado não possui identificador."
            )

        if usuario.perfil_id is None:
            raise ValueError(
                "O usuário autenticado não possui perfil vinculado."
            )

        perfil = self.perfil_repository.buscar_por_id(
            usuario.perfil_id
        )

        if perfil is None:
            raise ValueError(
                "O perfil vinculado ao usuário não foi encontrado."
            )

        if not perfil.ativo:
            raise ValueError(
                "O perfil vinculado ao usuário está desativado."
            )

        organizacao: Organizacao | None = None

        if usuario.organizacao_id is not None:
            organizacao = (
                self.organizacao_repository.buscar_por_id(
                    usuario.organizacao_id
                )
            )

            if organizacao is None:
                raise ValueError(
                    "A organização vinculada ao usuário "
                    "não foi encontrada."
                )

            if not organizacao.ativo:
                raise ValueError(
                    "A organização vinculada ao usuário "
                    "está desativada."
                )

        self._sessao_atual = SessaoUsuario(
            usuario=usuario,
            perfil=perfil,
            organizacao=organizacao,
        )

        return self._sessao_atual

    # ==========================================================
    # CONSULTA DA SESSÃO
    # ==========================================================

    def obter_sessao(self) -> SessaoUsuario | None:
        """Retorna a sessão autenticada atual."""

        return self._sessao_atual

    def exigir_sessao(self) -> SessaoUsuario:
        """
        Retorna a sessão atual.

        Lança erro quando não existe usuário autenticado.
        """

        if self._sessao_atual is None:
            raise RuntimeError(
                "Nenhum usuário está autenticado."
            )

        return self._sessao_atual

    def esta_autenticado(self) -> bool:
        """Informa se existe uma sessão autenticada."""

        return self._sessao_atual is not None

    def obter_usuario(self) -> Usuario | None:
        """Retorna o usuário da sessão atual."""

        if self._sessao_atual is None:
            return None

        return self._sessao_atual.usuario

    def obter_perfil(self) -> Perfil | None:
        """Retorna o perfil da sessão atual."""

        if self._sessao_atual is None:
            return None

        return self._sessao_atual.perfil

    def obter_organizacao(self) -> Organizacao | None:
        """Retorna a organização da sessão atual."""

        if self._sessao_atual is None:
            return None

        return self._sessao_atual.organizacao

    # ==========================================================
    # ATUALIZAÇÃO DA SESSÃO
    # ==========================================================

    def recarregar_sessao(self) -> SessaoUsuario:
        """
        Recarrega usuário, perfil e organização diretamente
        do banco de dados.
        """

        sessao = self.exigir_sessao()

        usuario_id = sessao.usuario.id

        if usuario_id is None:
            raise RuntimeError(
                "O usuário da sessão não possui identificador."
            )

        usuario_atualizado = (
            self.usuario_repository.buscar_por_id(
                usuario_id
            )
        )

        if usuario_atualizado is None:
            self.encerrar_sessao()

            raise RuntimeError(
                "O usuário da sessão não foi encontrado."
            )

        return self.abrir_sessao(
            usuario_atualizado
        )

    def atualizar_organizacao(
        self,
        organizacao: Organizacao,
    ) -> SessaoUsuario:
        """
        Atualiza a organização da sessão.

        Este método será utilizado após o Gerador concluir
        o Assistente de Configuração Inicial.
        """

        sessao = self.exigir_sessao()

        if organizacao.id is None:
            raise ValueError(
                "A organização não possui identificador."
            )

        usuario_id = sessao.usuario.id

        if usuario_id is None:
            raise RuntimeError(
                "O usuário da sessão não possui identificador."
            )

        vinculado = (
            self.usuario_repository.alterar_organizacao(
                usuario_id=usuario_id,
                organizacao_id=organizacao.id,
            )
        )

        if not vinculado:
            raise RuntimeError(
                "Não foi possível vincular a organização "
                "ao usuário autenticado."
            )

        return self.recarregar_sessao()

    def atualizar_perfil(
        self,
        perfil: Perfil,
    ) -> SessaoUsuario:
        """Atualiza o perfil do usuário autenticado."""

        sessao = self.exigir_sessao()

        if perfil.id is None:
            raise ValueError(
                "O perfil não possui identificador."
            )

        usuario_id = sessao.usuario.id

        if usuario_id is None:
            raise RuntimeError(
                "O usuário da sessão não possui identificador."
            )

        atualizado = self.usuario_repository.alterar_perfil(
            usuario_id=usuario_id,
            perfil_id=perfil.id,
        )

        if not atualizado:
            raise RuntimeError(
                "Não foi possível atualizar o perfil "
                "do usuário autenticado."
            )

        return self.recarregar_sessao()

    # ==========================================================
    # VERIFICAÇÕES DE PERFIL
    # ==========================================================

    def possui_perfil(
        self,
        codigo_perfil: str,
    ) -> bool:
        """Verifica o perfil da sessão pelo código oficial."""

        sessao = self._sessao_atual

        if sessao is None:
            return False

        codigo_normalizado = str(
            codigo_perfil or ""
        ).strip().upper()

        return (
            sessao.perfil.codigo.upper()
            == codigo_normalizado
        )

    def eh_gestor(self) -> bool:
        """Informa se o usuário autenticado é Gestor."""

        return self.possui_perfil("GESTOR")

    def eh_gerador(self) -> bool:
        """Informa se o usuário autenticado é Gerador."""

        return self.possui_perfil("GERADOR")

    def eh_empresa_parceira(self) -> bool:
        """Informa se o usuário pertence a uma Empresa Parceira."""

        return self.possui_perfil(
            "EMPRESA_PARCEIRA"
        )

    def possui_organizacao(self) -> bool:
        """Informa se a sessão possui organização vinculada."""

        return (
            self._sessao_atual is not None
            and self._sessao_atual.organizacao is not None
        )

    # ==========================================================
    # ENCERRAMENTO
    # ==========================================================

    def encerrar_sessao(self) -> None:
        """Remove todos os dados da sessão atual."""

        self._sessao_atual = None