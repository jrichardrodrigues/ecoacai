from __future__ import annotations

import flet as ft

from config import APP_NAME, COR_FUNDO
from controllers.auth_controller import AuthController
from controllers.organizacao_controller import OrganizacaoController
from models import Organizacao, SessaoUsuario
from repositories.sqlite_database import SQLiteDatabase
from services.sessao_service import SessaoService
from views.assistente_configuracao_inicial_view import (
    AssistenteConfiguracaoInicialView,
)
from views.cadastro_usuario_view import CadastroUsuarioView
from views.home_view import construir_interface
from views.login_view import LoginView


def main(page: ft.Page) -> None:
    """Inicializa e controla o fluxo principal da aplicação."""

    # ==========================================================
    # BANCO DE DADOS
    # ==========================================================

    SQLiteDatabase().inicializar()

    # ==========================================================
    # CONFIGURAÇÃO DA PÁGINA
    # ==========================================================

    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COR_FUNDO
    page.padding = 0

    # ==========================================================
    # SERVIÇOS E CONTROLLERS COMPARTILHADOS
    # ==========================================================

    # Deve existir apenas uma instância de SessaoService durante
    # toda a execução da aplicação.
    sessao_service = SessaoService()

    auth_controller = AuthController(
        sessao_service=sessao_service,
    )

    organizacao_controller = OrganizacaoController(
        sessao_service=sessao_service,
    )

    # ==========================================================
    # PORTAL DO GERADOR
    # ==========================================================

    def abrir_portal_gerador(
        organizacao: Organizacao | None = None,
    ) -> None:
        """
        Abre temporariamente a interface principal existente.

        O parâmetro organizacao permite que este método seja usado
        diretamente como callback do assistente de configuração.
        """

        page.clean()

        construir_interface(page)

        page.update()

    # ==========================================================
    # FLUXO APÓS O LOGIN
    # ==========================================================

    def abrir_area_principal(
        sessao: SessaoUsuario,
    ) -> None:
        """
        Decide o destino do usuário após a autenticação.

        Geradores sem organização são encaminhados ao Assistente
        de Configuração Inicial.
        """

        page.clean()

        if (
            sessao.eh_gerador
            and not sessao.possui_organizacao
        ):
            assistente_view = (
                AssistenteConfiguracaoInicialView(
                    page=page,
                    controller=organizacao_controller,
                    on_configuracao_concluida=(
                        abrir_portal_gerador
                    ),
                )
            )

            page.add(
                assistente_view.build()
            )
            page.update()
            return

        # Por enquanto, os usuários que já possuem organização
        # e os gestores continuam utilizando a interface atual.
        abrir_portal_gerador()

    # ==========================================================
    # LOGIN
    # ==========================================================

    def abrir_login(
        evento: ft.ControlEvent | None = None,
    ) -> None:
        """Abre a tela de autenticação."""

        page.clean()

        login_view = LoginView(
            page=page,
            auth_controller=auth_controller,
            on_login_sucesso=abrir_area_principal,
            on_criar_conta=abrir_criar_conta,
            on_esqueci_senha=abrir_recuperacao_senha,
        )

        page.add(
            login_view.build()
        )

        page.update()

    # ==========================================================
    # CRIAÇÃO DE CONTA
    # ==========================================================

    def abrir_criar_conta(
        evento: ft.ControlEvent | None = None,
    ) -> None:
        """Abre a tela pública de criação de conta."""

        page.clean()

        cadastro_view = CadastroUsuarioView(
            page=page,
            on_voltar_login=abrir_login,
        )

        page.add(
            cadastro_view.build()
        )

        page.update()

    # ==========================================================
    # RECUPERAÇÃO DE SENHA
    # ==========================================================

    def abrir_recuperacao_senha(
        evento: ft.ControlEvent,
    ) -> None:
        """Fluxo temporário de recuperação de senha."""

        print(
            "Abrir recuperação de senha"
        )

    # ==========================================================
    # INÍCIO DA APLICAÇÃO
    # ==========================================================

    abrir_login()


if __name__ == "__main__":
    ft.run(
        main=main,
    )