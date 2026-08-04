from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.layout import BasePage
from components.theme import Colors, Radius, Spacing
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from models import SessaoUsuario


class PortalGeradorView:
    """Portal principal do usuário Gerador."""

    def __init__(
        self,
        page: ft.Page,
        sessao: SessaoUsuario,
        on_nova_solicitacao: Callable[[], None],
        on_minhas_solicitacoes: Callable[[], None],
        on_sair: Callable[[], None] | None = None,
        controller: SolicitacaoColetaController | None = None,
    ) -> None:
        self.page = page
        self.sessao = sessao
        self._on_nova_solicitacao = on_nova_solicitacao
        self._on_minhas_solicitacoes = on_minhas_solicitacoes
        self._on_sair = on_sair
        self.controller = controller or SolicitacaoColetaController()

        self._validar_sessao()
        self._criar_controles()
        self._carregar_resumo()

    def _validar_sessao(self) -> None:
        if not self.sessao.eh_gerador:
            raise PermissionError(
                "O Portal do Gerador exige o perfil GERADOR."
            )

        if self.sessao.usuario.id is None:
            raise ValueError(
                "O usuário autenticado não possui identificador."
            )

        if self.sessao.organizacao is None:
            raise ValueError(
                "O usuário Gerador ainda não possui organização."
            )

        if self.sessao.organizacao.id is None:
            raise ValueError(
                "A organização autenticada não possui identificador."
            )

    @property
    def organizacao_id(self) -> int:
        organizacao = self.sessao.organizacao

        if organizacao is None or organizacao.id is None:
            raise RuntimeError(
                "A sessão não possui organização válida."
            )

        return organizacao.id

    @property
    def usuario_id(self) -> int:
        usuario_id = self.sessao.usuario.id

        if usuario_id is None:
            raise RuntimeError(
                "A sessão não possui usuário válido."
            )

        return usuario_id

    def _criar_controles(self) -> None:
        self.nome_organizacao = ft.Text(
            self.sessao.organizacao.nome,
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        self.saudacao = ft.Text(
            self._texto_saudacao(),
            size=15,
            color=Colors.TEXT_SECONDARY,
        )

        self.total_abertas = self._criar_indicador(
            titulo="Em aberto",
            valor="0",
            icone=ft.Icons.PENDING_ACTIONS_OUTLINED,
        )

        self.total_agendadas = self._criar_indicador(
            titulo="Agendadas",
            valor="0",
            icone=ft.Icons.EVENT_AVAILABLE_OUTLINED,
        )

        self.total_concluidas = self._criar_indicador(
            titulo="Concluídas",
            valor="0",
            icone=ft.Icons.CHECK_CIRCLE_OUTLINE,
        )

        self.ultima_solicitacao = ft.Text(
            "Nenhuma solicitação registrada.",
            size=14,
            color=Colors.TEXT_SECONDARY,
        )

        self.botao_nova_solicitacao = ft.FilledButton(
            content="Solicitar nova coleta",
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            on_click=self._abrir_nova_solicitacao,
        )

        self.botao_minhas_solicitacoes = ft.OutlinedButton(
            content="Minhas solicitações",
            icon=ft.Icons.FORMAT_LIST_BULLETED,
            on_click=self._abrir_minhas_solicitacoes,
        )

        self.botao_sair = ft.TextButton(
            content="Sair",
            icon=ft.Icons.LOGOUT,
            visible=self._on_sair is not None,
            on_click=self._sair,
        )

    @staticmethod
    def _criar_indicador(
        *,
        titulo: str,
        valor: str,
        icone: str,
    ) -> dict[str, ft.Control]:
        texto_valor = ft.Text(
            valor,
            size=28,
            weight=ft.FontWeight.BOLD,
        )

        controle = ft.Container(
            expand=True,
            padding=Spacing.MD,
            border_radius=Radius.MD,
            bgcolor=Colors.BACKGROUND,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icone,
                        size=30,
                        color=Colors.PRIMARY,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                titulo,
                                size=13,
                                color=Colors.TEXT_SECONDARY,
                            ),
                            texto_valor,
                        ],
                        spacing=2,
                        tight=True,
                    ),
                ],
                spacing=Spacing.MD,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        return {
            "controle": controle,
            "valor": texto_valor,
        }

    def _carregar_resumo(self) -> None:
        try:
            estatisticas = self.controller.obter_estatisticas(
                organizacao_id=self.organizacao_id,
            )

            abertas = int(
                estatisticas.get("pendentes", 0) or 0
            )
            agendadas = int(
                estatisticas.get("agendadas", 0) or 0
            )
            concluidas = int(
                estatisticas.get("concluidas", 0) or 0
            )

            self.total_abertas["valor"].value = str(abertas)
            self.total_agendadas["valor"].value = str(agendadas)
            self.total_concluidas["valor"].value = str(concluidas)

            ultimas = self.controller.listar_ultimas(
                limite=1,
                organizacao_id=self.organizacao_id,
            )

            if ultimas:
                ultima = ultimas[0]
                codigo = ultima.get("codigo") or "Sem código"
                status = str(
                    ultima.get("status") or ""
                ).replace("_", " ").title()
                data = (
                    ultima.get("data_solicitacao")
                    or "Data não informada"
                )

                self.ultima_solicitacao.value = (
                    f"{codigo} • {status} • {data}"
                )

        except Exception as erro:
            print(
                "Erro ao carregar o resumo do Portal do Gerador:",
                erro,
            )

            self.ultima_solicitacao.value = (
                "Não foi possível carregar o resumo das solicitações."
            )

    def _abrir_nova_solicitacao(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        self._on_nova_solicitacao()

    def _abrir_minhas_solicitacoes(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        self._on_minhas_solicitacoes()

    def _sair(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        if self._on_sair is not None:
            self._on_sair()

    def construir(self) -> ft.Control:
        cabecalho_organizacao = ft.Container(
            padding=Spacing.MD,
            border_radius=Radius.MD,
            bgcolor=Colors.BACKGROUND,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.DOMAIN_OUTLINED,
                        size=38,
                        color=Colors.PRIMARY,
                    ),
                    ft.Column(
                        controls=[
                            self.saudacao,
                            self.nome_organizacao,
                        ],
                        spacing=3,
                        tight=True,
                    ),
                    ft.Container(expand=True),
                    self.botao_sair,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        indicadores = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"xs": 12, "sm": 4},
                    content=self.total_abertas["controle"],
                ),
                ft.Container(
                    col={"xs": 12, "sm": 4},
                    content=self.total_agendadas["controle"],
                ),
                ft.Container(
                    col={"xs": 12, "sm": 4},
                    content=self.total_concluidas["controle"],
                ),
            ],
            spacing=Spacing.MD,
            run_spacing=Spacing.MD,
        )

        acoes = ft.Container(
            padding=Spacing.LG,
            border_radius=Radius.MD,
            bgcolor=Colors.BACKGROUND,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "O que deseja fazer?",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        (
                            "Solicite uma nova coleta ou acompanhe "
                            "as solicitações da sua organização."
                        ),
                        size=14,
                        color=Colors.TEXT_SECONDARY,
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"xs": 12, "sm": 6},
                                content=self.botao_nova_solicitacao,
                            ),
                            ft.Container(
                                col={"xs": 12, "sm": 6},
                                content=self.botao_minhas_solicitacoes,
                            ),
                        ],
                        spacing=Spacing.MD,
                        run_spacing=Spacing.MD,
                    ),
                ],
                spacing=Spacing.MD,
            ),
        )

        ultima_solicitacao = ft.Container(
            padding=Spacing.MD,
            border_radius=Radius.MD,
            bgcolor=Colors.BACKGROUND,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Última solicitação",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.ultima_solicitacao,
                ],
                spacing=Spacing.SM,
            ),
        )

        conteudo = ft.Column(
            controls=[
                cabecalho_organizacao,
                indicadores,
                acoes,
                ultima_solicitacao,
            ],
            spacing=Spacing.LG,
        )

        return BasePage(
            title="Portal do Gerador",
            subtitle=(
                "Solicite e acompanhe as coletas da sua organização."
            ),
            content=conteudo,
            max_width=1100,
        )

    def build(self) -> ft.Control:
        return self.construir()

    def _texto_saudacao(self) -> str:
        nome = str(
            self.sessao.usuario.nome or ""
        ).strip()

        primeiro_nome = (
            nome.split()[0]
            if nome
            else "Gerador"
        )

        return f"Olá, {primeiro_nome}!"
