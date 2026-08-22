from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.layout import BasePage
from components.dialogs import confirmar_exclusao

from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from utils.messages import mostrar_erro, mostrar_sucesso


class SolicitacoesGestorView:
    """Fila de solicitações de coleta recebidas pelo Gestor."""

    def __init__(
        self,
        page: ft.Page,
        controller: SolicitacaoColetaController | None = None,
        on_ver_detalhes: Callable[[int, str], None] | None = None,
        on_abrir_lixeira: Callable[[], None] | None = None,
        status_inicial: str | None = None,
        data_agendada_inicial: str | None = None,
        data_solicitacao_inicial: str | None = None,
        titulo: str = "Solicitações",
        subtitulo: str = "Analise as solicitações de coleta recebidas dos Geradores.",
    ) -> None:
        self.page = page
        self.controller = (
                controller or SolicitacaoColetaController()
        )

        self.status_inicial = status_inicial
        self.data_agendada_inicial = data_agendada_inicial
        self.data_solicitacao_inicial = data_solicitacao_inicial

        self.titulo = titulo
        self.subtitulo = subtitulo

        self.lista = ft.Column(
            spacing=12,
        )

        self.total = ft.Text(
            "0 solicitações",
            size=14,
            color=ft.Colors.BLUE_GREY_700,
        )

        self.on_ver_detalhes = on_ver_detalhes

        self.on_abrir_lixeira = on_abrir_lixeira

        self._carregar()

    # ==========================================================
    # FORMATAÇÃO
    # ==========================================================

    @staticmethod
    def _formatar_status(
        status: str,
    ) -> str:
        return (
            str(status or "")
            .replace("_", " ")
            .title()
        )

    @staticmethod
    def _formatar_residuo(
        tipo: str,
    ) -> str:
        tipos = {
            "CAROCO_ACAI": "Caroço de Açaí",
        }

        return tipos.get(
            tipo,
            tipo or "-",
        )

    @staticmethod
    def _formatar_quantidade(
            dados: dict,
    ) -> str:
        forma_acondicionamento = str(
            dados.get("forma_acondicionamento") or ""
        ).strip().upper()

        quantidade = int(
            dados.get("quantidade_prevista")
            or dados.get("quantidade_sacas_prevista")
            or 0
        )

        if forma_acondicionamento == "BAG":
            unidade_texto = (
                "Bag"
                if quantidade == 1
                else "Bags"
            )

            return (
                f"{quantidade} "
                f"{unidade_texto} (1 m³)"
            )

        if forma_acondicionamento == "SACA":
            unidade_texto = (
                "Saca"
                if quantidade == 1
                else "Sacas"
            )

            return (
                f"{quantidade} "
                f"{unidade_texto} (50 kg)"
            )

        return f"{quantidade} unidade(s)"

    # ==========================================================
    # DADOS
    # ==========================================================

    def _carregar(self) -> None:
        solicitacoes = self.controller.listar_operacional(
            status=self.status_inicial,
            data_agendada=self.data_agendada_inicial,
            data_inicial=self.data_solicitacao_inicial,
            data_final=self.data_solicitacao_inicial,
        )

        self.lista.controls.clear()

        for dados in solicitacoes:
            self.lista.controls.append(
                self._criar_card(dados)
            )

        total = len(solicitacoes)

        self.total.value = (
            f"{total} "
            f"{'solicitação' if total == 1 else 'solicitações'}"
        )

        if not solicitacoes:
            self.lista.controls.append(
                self._estado_vazio()
            )

    # ==========================================================
    # CARDS
    # ==========================================================

    def _criar_card(
        self,
        dados: dict,
    ) -> ft.Control:

        solicitacao_id = int(
            dados.get("id") or 0
        )

        codigo = (
            dados.get("codigo")
            or f"COL-{solicitacao_id:06d}"
        )

        solicitante = (
            dados.get("solicitante")
            or "Solicitante não identificado"
        )

        status = str(
            dados.get("status") or ""
        ).upper()

        botoes: list[ft.Control] = []

        if status == "SOLICITADA":
            botoes.append(
                ft.FilledButton(
                    content="Analisar",
                    icon=ft.Icons.RATE_REVIEW_OUTLINED,
                    on_click=lambda _e, sid=solicitacao_id: (
                        self._analisar(sid)
                    ),
                )
            )

            botoes.append(
                ft.TextButton(
                    content="Excluir",
                    icon=ft.Icons.DELETE_OUTLINE,
                    style=ft.ButtonStyle(
                        color=ft.Colors.RED_700,
                    ),
                    on_click=lambda _e, sid=solicitacao_id: (
                        self._excluir(sid)
                    ),
                )
            )

        if self.on_ver_detalhes is not None:
            botoes.append(
                ft.TextButton(
                    content="Ver detalhes",
                    icon=ft.Icons.VISIBILITY_OUTLINED,
                    on_click=lambda _e, sid=solicitacao_id, nome=solicitante: (
                        self.on_ver_detalhes(
                            sid,
                            nome,
                        )
                    ),
                )
            )

        return ft.Card(
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    codigo,
                                    size=17,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(
                                    expand=True,
                                ),
                                ft.Text(
                                    self._formatar_status(
                                        status
                                    ),
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),

                        ft.Divider(),

                        ft.Text(
                            f"Solicitante: {solicitante}"
                        ),

                        ft.Text(
                            "Tipo de resíduo: "
                            + self._formatar_residuo(
                                dados.get("tipo_residuo")
                            )
                        ),

                        ft.Text(
                            "Quantidade prevista: "
                            + self._formatar_quantidade(dados)
                        ),

                        ft.Text(
                            "Peso estimado: "
                            + self._formatar_peso_estimado(dados)
                        ),

                        ft.Text(
                            "Solicitada em: "
                            f"{dados.get('data_solicitacao') or '-'}"
                        ),

                        ft.Row(
                            controls=botoes,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=8,
                ),
            ),
        )

    def _excluir(
            self,
            solicitacao_id: int,
    ) -> None:
        """Solicita confirmação e exclui logicamente a solicitação."""

        def confirmar() -> None:
            sucesso, mensagem = self.controller.excluir(
                solicitacao_id
            )

            if sucesso:
                mostrar_sucesso(
                    self.page,
                    mensagem,
                )
                self._carregar()
            else:
                mostrar_erro(
                    self.page,
                    mensagem,
                )

        confirmar_exclusao(
            page=self.page,
            mensagem=(
                "Deseja realmente excluir esta solicitação?"
            ),
            on_confirm=confirmar,
        )

    @staticmethod
    def _formatar_peso_estimado(
            dados: dict,
    ) -> str:
        peso = float(
            dados.get("peso_estimado_kg") or 0
        )

        if peso <= 0:
            return "Não informado"

        if peso.is_integer():
            return f"{int(peso):,}".replace(",", ".") + " kg"

        return (
                f"{peso:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " kg"
        )

    # ==========================================================
    # AÇÕES
    # ==========================================================

    def _analisar(
        self,
        solicitacao_id: int,
    ) -> None:
        sucesso, mensagem, _solicitacao = (
            self.controller.analisar(
                solicitacao_id
            )
        )

        if not sucesso:
            mostrar_erro(
                self.page,
                mensagem,
            )
            return

        mostrar_sucesso(
            self.page,
            mensagem,
        )

        self._carregar()
        self.page.update()

    # ==========================================================
    # ESTADO VAZIO
    # ==========================================================

    @staticmethod
    def _estado_vazio() -> ft.Control:
        return ft.Container(
            padding=40,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.INBOX_OUTLINED,
                        size=56,
                        color=ft.Colors.BLUE_GREY_400,
                    ),
                    ft.Text(
                        "Nenhuma solicitação nesta data.",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Não há solicitações cadastradas hoje.",
                        color=ft.Colors.BLUE_GREY_700,
                    ),
                ],
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=10,
            ),
        )

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def build(self) -> ft.Control:

        botao_lixeira = ft.OutlinedButton(
            content="Lixeira",
            icon=ft.Icons.DELETE_OUTLINE,
            on_click=(
                lambda _e: self.on_abrir_lixeira()
                if self.on_abrir_lixeira is not None
                else None
            ),
        )

        conteudo = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        botao_lixeira,
                    ],
                ),
                self.total,
                self.lista,
            ],
            spacing=16,
        )

        return BasePage(
            title=self.titulo,
            subtitle=self.subtitulo,
            content=conteudo,
            max_width=1100,
        )