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

        cards: list[ft.Control] = []

        for solicitacao in solicitacoes:
            forma = str(
                solicitacao.forma_acondicionamento or ""
            ).strip().upper()

            if forma == "BAG":
                quantidade_texto = (
                    f"{solicitacao.quantidade_prevista} "
                    f"{'Bag' if solicitacao.quantidade_prevista == 1 else 'Bags'} "
                    "(1 m³)"
                )
            else:
                quantidade_texto = (
                    f"{solicitacao.quantidade_prevista} "
                    f"{'Saca' if solicitacao.quantidade_prevista == 1 else 'Sacas'}"
                )

            # Nome amigável do tipo de resíduo
            tipos_residuo = {
                "CAROCO_ACAI": "Caroço de Açaí",
            }

            tipo_residuo_texto = tipos_residuo.get(
                solicitacao.tipo_residuo,
                solicitacao.tipo_residuo,
            )

            # Data amigável
            data_solicitacao_texto = solicitacao.data_solicitacao or "-"

            if data_solicitacao_texto != "-":
                try:
                    from datetime import datetime

                    data_solicitacao_texto = datetime.fromisoformat(
                        data_solicitacao_texto
                    ).strftime("%d/%m/%Y %H:%M")
                except (ValueError, TypeError):
                    pass

            cards.append(
                ft.Card(
                    content=ft.Container(
                        padding=16,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            solicitacao.numero,
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Container(expand=True),
                                        ft.Text(
                                            formatar_status(
                                                solicitacao.status
                                            ),
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    f"Tipo de resíduo: {tipo_residuo_texto}"
                                ),
                                ft.Text(
                                    f"Quantidade prevista: {quantidade_texto}"
                                ),
                                ft.Text(
                                    f"Solicitada em: {data_solicitacao_texto}"
                                ),
                                ft.Text(
                                    solicitacao.observacao_cliente,
                                    visible=bool(
                                        solicitacao.observacao_cliente
                                    ),
                                ),
                            ],
                            spacing=8,
                        ),
                    ),
                )
            )

        if not cards:
            cards.append(
                ft.Container(
                    padding=32,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        controls=[
                            ft.Icon(
                                ft.Icons.INBOX_OUTLINED,
                                size=56,
                            ),
                            ft.Text(
                                "Nenhuma solicitação registrada.",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.FilledButton(
                                content="Solicitar primeira coleta",
                                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                on_click=(
                                    lambda _e:
                                    abrir_nova_solicitacao()
                                ),
                            ),
                        ],
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        spacing=12,
                    ),
                )
            )

        conteudo = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            content="Voltar ao portal",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=(
                                lambda _e:
                                abrir_portal_gerador()
                            ),
                        ),
                        ft.Container(expand=True),
                        ft.FilledButton(
                            content="Nova solicitação",
                            icon=ft.Icons.ADD,
                            on_click=(
                                lambda _e:
                                abrir_nova_solicitacao()
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    f"Total de solicitações: {len(solicitacoes)}",
                ),
                ft.Column(
                    controls=cards,
                    spacing=12,
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )

        tela = BasePage(
            title="Minhas Solicitações",
            subtitle=(
                "Acompanhe as solicitações de coleta "
                "da sua organização."
            ),
            content=conteudo,
            max_width=1000,
        )

        exibir(tela)

    def abrir_assistente_configuracao() -> None:
        sessao = obter_sessao_atual()

        assistente = AssistenteConfiguracaoInicialView(
            page=page,
            controller=organizacao_controller,
            sessao=sessao,
            on_configuracao_concluida=abrir_portal_gerador,
        )

        exibir(assistente.build())

    def abrir_area_gestor() -> None:
        """Mantém o Gestor na interface administrativa atual."""

        page.clean()
        construir_interface(page)
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
            abrir_area_gestor()
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



    abrir_login()


if __name__ == "__main__":
    ft.run(
        main=main,
    )
