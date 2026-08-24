from __future__ import annotations

from typing import Any

import flet as ft

from components.layout import BasePage
from config import APP_NAME, COR_FUNDO
from controllers.auth_controller import AuthController
from controllers.organizacao_controller import OrganizacaoController
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from models import Organizacao, SessaoUsuario
from repositories.sqlite_database import SQLiteDatabase
from services.sessao_service import SessaoService
from views.assistente_configuracao_inicial_view import (
    AssistenteConfiguracaoInicialView,
)
from views.cadastro_usuario_view import CadastroUsuarioView
from views.home_view import construir_interface
from views.login_view import LoginView
from views.nova_solicitacao_view import NovaSolicitacaoView
from views.portal_gerador_view import PortalGeradorView
from views.recuperar_senha_view import RecuperarSenhaView
from views.minhas_solicitacoes_view import MinhasSolicitacoesView
from views.detalhe_solicitacao_view import DetalheSolicitacaoView
from views.zelurbis_home_view import ZelurbisHomeView

def main(page: ft.Page) -> None:

    SQLiteDatabase().inicializar()

    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COR_FUNDO
    page.padding = 0

    page.window.width = 1280
    page.window.height = 850
    page.window.min_width = 1000
    page.window.min_height = 600

    sessao_service = SessaoService()

    auth_controller = AuthController(
        sessao_service=sessao_service,
    )

    organizacao_controller = OrganizacaoController(
        sessao_service=sessao_service,
    )

    solicitacao_controller = SolicitacaoColetaController()

    def exibir(controle: ft.Control) -> None:

        page.clean()
        page.add(controle)
        page.update()

    def obter_sessao_atual() -> SessaoUsuario:
        """Retorna a sessão autenticada atual."""

        return sessao_service.exigir_sessao()

    def formatar_status(status: str) -> str:
        return str(status or "").replace("_", " ").title()

    class NavegacaoGerador:
        """
        Adaptador temporário utilizado pela NovaSolicitacaoView.

        A View atual procura page.navigation_controller depois
        de cadastrar uma solicitação.
        """

        def ir_para(
            self,
            destino: str,
        ) -> None:
            rotas = {
                "portal_gerador": abrir_portal_gerador,
                "nova_solicitacao": abrir_nova_solicitacao,
                "minhas_solicitacoes": abrir_minhas_solicitacoes,
            }

            acao = rotas.get(
                str(destino or "").strip().lower()
            )

            if acao is None:
                return

            acao()

    page.navigation_controller = NavegacaoGerador()

    def abrir_portal_gerador(
        organizacao: Organizacao | None = None,
    ) -> None:
        """
        Abre o Portal do Gerador.

        O parâmetro organizacao permite usar esta função como
        callback do Assistente de Configuração Inicial.
        """

        sessao = obter_sessao_atual()

        portal = PortalGeradorView(
            page=page,
            sessao=sessao,
            controller=solicitacao_controller,
            on_nova_solicitacao=abrir_nova_solicitacao,
            on_minhas_solicitacoes=abrir_minhas_solicitacoes,
            on_sair=sair,
        )

        exibir(portal.build())

    def abrir_nova_solicitacao() -> None:
        """Abre o formulário simplificado do Gerador."""

        sessao = obter_sessao_atual()

        if sessao.organizacao is None:
            abrir_assistente_configuracao()
            return

        organizacao_id = sessao.organizacao.id
        usuario_id = sessao.usuario.id

        if organizacao_id is None or usuario_id is None:
            raise RuntimeError(
                "A sessão não possui usuário e organização válidos."
            )

        view = NovaSolicitacaoView(
            page=page,
            organizacao_id=organizacao_id,
            usuario_id=usuario_id,
        )

        exibir(view.build())

    def abrir_detalhe_solicitacao(
            solicitacao,
    ) -> None:
        """Abre os detalhes de uma solicitação do Gerador."""

        view = DetalheSolicitacaoView(
            solicitacao=solicitacao,
            on_voltar=abrir_minhas_solicitacoes,
        )

        exibir(view.build())

    def abrir_minhas_solicitacoes() -> None:
        """Lista as solicitações da organização autenticada."""

        sessao = obter_sessao_atual()

        if sessao.organizacao is None:
            abrir_assistente_configuracao()
            return

        organizacao_id = sessao.organizacao.id

        if organizacao_id is None:
            raise RuntimeError(
                "A organização da sessão não possui identificador."
            )

        solicitacoes = solicitacao_controller.listar_por_organizacao(
            organizacao_id=organizacao_id,
        )

        view = MinhasSolicitacoesView(
            solicitacoes=solicitacoes,
            on_voltar=abrir_portal_gerador,
            on_nova_solicitacao=abrir_nova_solicitacao,
            on_ver_detalhes=abrir_detalhe_solicitacao,
        )

        exibir(view.build())

    def abrir_assistente_configuracao() -> None:
        sessao = obter_sessao_atual()

        assistente = AssistenteConfiguracaoInicialView(
            page=page,
            controller=organizacao_controller,
            sessao=sessao,
            on_configuracao_concluida=abrir_portal_gerador,
        )

        exibir(assistente.build())

    def abrir_home_zelurbis(
            sessao: SessaoUsuario | None = None,
    ) -> None:
        """Abre a Home principal da Plataforma ZELURBIS."""

        page.appbar = None

        view = ZelurbisHomeView(
            page=page,
            sessao=sessao,
            on_acessar_ecoacai=abrir_area_gestor,
            on_sair=sair,
        )

        exibir(
            view.build()
        )

    def abrir_area_gestor() -> None:
        """Abre o módulo operacional ECOAÇAÍ."""

        page.clean()

        construir_interface(
            page,
            on_voltar_zelurbis=abrir_home_zelurbis,
        )

        page.update()

    def abrir_area_principal(
        sessao: SessaoUsuario,
    ) -> None:
        """Direciona cada perfil para sua área."""

        if sessao.eh_gerador:
            if not sessao.possui_organizacao:
                abrir_assistente_configuracao()
                return

            abrir_portal_gerador()
            return

        if sessao.eh_gestor:
            abrir_home_zelurbis(
                sessao
            )
            return

        if sessao.eh_empresa_parceira:
            # Portal específico será criado posteriormente.
            abrir_area_gestor()
            return

        auth_controller.sair()
        abrir_login()

    def abrir_login(
            evento: Any = None,
    ) -> None:

        login_view = LoginView(
            page=page,
            auth_controller=auth_controller,
            on_login_sucesso=abrir_area_principal,
            on_criar_conta=abrir_criar_conta,
            on_esqueci_senha=abrir_recuperacao_senha,
        )

        controle = login_view.build()

        exibir(controle)

    def sair(
            evento: Any = None,
    ) -> None:
        """Encerra a sessão e retorna ao login."""

        auth_controller.sair()
        abrir_login()

    def abrir_criar_conta(
        evento: ft.ControlEvent | None = None,
    ) -> None:
        """Abre a tela pública de criação de conta."""

        cadastro_view = CadastroUsuarioView(
            page=page,
            on_voltar_login=abrir_login,
        )

        exibir(cadastro_view.build())

    def abrir_recuperacao_senha(
            evento: ft.ControlEvent | None = None,
    ) -> None:
        """Abre a tela de recuperação de senha."""

        view = RecuperarSenhaView(
            page=page,
            auth_controller=auth_controller,
            on_voltar=abrir_login,
        )

        exibir(view.build())



    # abrir_login()
    abrir_home_zelurbis()

if __name__ == "__main__":
    ft.run(
        main=main,
    )
