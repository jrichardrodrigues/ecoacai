from collections.abc import Callable
from datetime import datetime

import flet as ft

from components.dialogs.confirm_dialog import ConfirmDialog
from components.layout import BasePage
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from utils.messages import mostrar_erro, mostrar_sucesso


class SolicitacoesExcluidasView:
    """Lixeira das solicitações excluídas logicamente."""

    def __init__(
        self,
        page: ft.Page,
        controller: SolicitacaoColetaController | None = None,
        on_voltar: Callable[[], None] | None = None,
    ) -> None:
        self.page = page
        self.controller = (
            controller or SolicitacaoColetaController()
        )
        self.on_voltar = on_voltar

        self.lista = ft.Column(
            spacing=12,
        )

        self.total = ft.Text(
            "0 solicitações excluídas",
            size=14,
            color=ft.Colors.BLUE_GREY_700,
        )

        self._carregar()

    # ==========================================================
    # DADOS
    # ==========================================================

    def _carregar(self) -> None:
        solicitacoes = self.controller.listar_excluidas()

        self.lista.controls.clear()

        for dados in solicitacoes:
            self.lista.controls.append(
                self._criar_card(dados)
            )

        total = len(solicitacoes)

        self.total.value = (
            f"{total} "
            f"{'solicitação excluída' if total == 1 else 'solicitações excluídas'}"
        )

        if not solicitacoes:
            self.lista.controls.append(
                self._estado_vazio()
            )

    # ==========================================================
    # FORMATAÇÃO
    # ==========================================================

    @staticmethod
    def _formatar_data_hora(
        valor: str | None,
    ) -> str:
        if not valor:
            return "-"

        try:
            data = datetime.fromisoformat(valor)

            return data.strftime(
                "%d/%m/%Y às %H:%M"
            )
        except ValueError:
            return str(valor)

    @staticmethod
    def _formatar_status(
        status: str,
    ) -> str:
        return (
            str(status or "")
            .replace("_", " ")
            .title()
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

        status = self._formatar_status(
            str(dados.get("status") or "")
        )

        data_exclusao = self._formatar_data_hora(
            dados.get("data_hora_exclusao")
        )

        return ft.Card(
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=8,
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
                                    status,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),

                        ft.Divider(),

                        ft.Text(
                            f"Solicitante: {solicitante}"
                        ),

                        ft.Text(
                            "Excluída em: "
                            f"{data_exclusao}"
                        ),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.OutlinedButton(
                                    content="Restaurar",
                                    icon=ft.Icons.RESTORE_ROUNDED,
                                    on_click=(
                                        lambda _e,
                                        sid=solicitacao_id:
                                        self._confirmar_restauracao(
                                            sid
                                        )
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )

    # ==========================================================
    # RESTAURAÇÃO
    # ==========================================================

    def _confirmar_restauracao(
        self,
        solicitacao_id: int,
    ) -> None:
        dialogo = ConfirmDialog(
            page=self.page,
            titulo="Restaurar solicitação",
            mensagem=(
                "Deseja realmente restaurar esta solicitação?"
            ),
            texto_confirmar="Restaurar",
            texto_cancelar="Cancelar",
            cor_confirmar=ft.Colors.GREEN_700,
            icone=ft.Icons.RESTORE_ROUNDED,
            on_confirm=lambda: self._restaurar(
                solicitacao_id
            ),
        )

        dialogo.abrir()

    def _restaurar(
        self,
        solicitacao_id: int,
    ) -> None:
        sucesso, mensagem = self.controller.restaurar(
            solicitacao_id
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
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=10,
                controls=[
                    ft.Icon(
                        ft.Icons.DELETE_OUTLINE,
                        size=56,
                        color=ft.Colors.BLUE_GREY_400,
                    ),
                    ft.Text(
                        "A lixeira está vazia.",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Não há solicitações excluídas para restaurar.",
                        color=ft.Colors.BLUE_GREY_700,
                    ),
                ],
            ),
        )

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def build(self) -> ft.Control:
        botao_voltar = ft.OutlinedButton(
            content="Voltar",
            icon=ft.Icons.ARROW_BACK,
            on_click=(
                lambda _e: self.on_voltar()
                if self.on_voltar is not None
                else None
            ),
        )

        conteudo = ft.Column(
            spacing=16,
            controls=[
                ft.Row(
                    controls=[
                        botao_voltar,
                    ],
                ),
                self.total,
                self.lista,
            ],
        )

        return BasePage(
            title="Lixeira de Solicitações",
            subtitle=(
                "Consulte e restaure solicitações excluídas."
            ),
            content=conteudo,
            max_width=1100,
        )