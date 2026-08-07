from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

import flet as ft

from components.layout import BasePage
from models import SolicitacaoColeta


class DetalheSolicitacaoGestorView:
    """Exibe os detalhes operacionais de uma solicitação para o Gestor."""

    def __init__(
            self,
            *,
            solicitacao: SolicitacaoColeta,
            solicitante: str = "",
            on_voltar: Callable[[], None],
            on_agendar: Callable[[SolicitacaoColeta], None] | None = None,
    ) -> None:
        self.solicitacao = solicitacao
        self.solicitante = (
            solicitante.strip()
            or "Solicitante não identificado"
        )
        self.on_voltar = on_voltar
        self.on_agendar = on_agendar

    # ==========================================================
    # FORMATAÇÃO
    # ==========================================================

    @staticmethod
    def _formatar_status(status: str) -> str:
        return (
            str(status or "")
            .replace("_", " ")
            .title()
        )

    @staticmethod
    def _formatar_tipo_residuo(tipo_residuo: str) -> str:
        tipos = {
            "CAROCO_ACAI": "Caroço de Açaí",
        }

        return tipos.get(
            tipo_residuo,
            tipo_residuo or "-",
        )

    @staticmethod
    def _formatar_data(valor: str | None) -> str:
        if not valor:
            return "-"

        try:
            return datetime.fromisoformat(valor).strftime(
                "%d/%m/%Y %H:%M"
            )
        except (ValueError, TypeError):
            return valor

    def _formatar_quantidade(self) -> str:
        quantidade = self.solicitacao.quantidade_prevista

        forma = str(
            self.solicitacao.forma_acondicionamento or ""
        ).strip().upper()

        if forma == "BAG":
            unidade = (
                "Bag"
                if quantidade == 1
                else "Bags"
            )

            return (
                f"{quantidade} "
                f"{unidade} (1 m³)"
            )

        unidade = (
            "Saca"
            if quantidade == 1
            else "Sacas"
        )

        return f"{quantidade} {unidade}"

    def _formatar_operacao(self) -> str:
        tipo = str(
            self.solicitacao.tipo_operacao or ""
        ).strip().upper()

        if tipo == "MUNCK":
            return "Caminhão Munck"

        if tipo == "MANUAL":
            return "Coleta manual"

        return tipo or "-"

    @staticmethod
    def _linha(
        titulo: str,
        valor: str,
    ) -> ft.Control:
        return ft.Row(
            controls=[
                ft.Text(
                    titulo,
                    width=190,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    valor,
                    expand=True,
                ),
            ],
            vertical_alignment=(
                ft.CrossAxisAlignment.START
            ),
        )

    # ==========================================================
    # AÇÕES DISPONÍVEIS
    # ==========================================================

    def _construir_acoes(self) -> ft.Control:
        status = str(
            self.solicitacao.status or ""
        ).strip().upper()

        botoes: list[ft.Control] = []

        if status == "EM_ANALISE":
            botoes.extend(
                [
                    ft.FilledButton(
                        content="Agendar coleta",
                        icon=ft.Icons.EVENT_AVAILABLE_OUTLINED,
                        disabled=self.on_agendar is None,
                        on_click=(
                            lambda _e: self.on_agendar(self.solicitacao)
                            if self.on_agendar
                            else None
                        ),
                    ),
                    ft.OutlinedButton(
                        content="Recusar solicitação",
                        icon=ft.Icons.CANCEL_OUTLINED,
                        disabled=True,
                    ),
                ]
            )

        elif status == "AGENDADA":
            botoes.extend(
                [
                    ft.FilledButton(
                        content="Iniciar deslocamento",
                        icon=ft.Icons.LOCAL_SHIPPING_OUTLINED,
                        disabled=True,
                    ),
                    ft.OutlinedButton(
                        content="Cancelar coleta",
                        icon=ft.Icons.CANCEL_OUTLINED,
                        disabled=True,
                    ),
                ]
            )

        elif status == "EM_DESLOCAMENTO":
            botoes.append(
                ft.FilledButton(
                    content="Iniciar coleta",
                    icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
                    disabled=True,
                )
            )

        elif status == "EM_COLETA":
            botoes.append(
                ft.FilledButton(
                    content="Concluir coleta",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    disabled=True,
                )
            )

        if not botoes:
            return ft.Container(
                content=ft.Text(
                    "Nenhuma ação disponível "
                    "para o status atual.",
                    color=ft.Colors.BLUE_GREY_700,
                )
            )

        return ft.Row(
            controls=botoes,
            alignment=ft.MainAxisAlignment.END,
            spacing=12,
            wrap=True,
        )

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def build(self) -> ft.Control:
        solicitacao = self.solicitacao

        conteudo = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            content="Voltar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _e: (
                                self.on_voltar()
                            ),
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            self._formatar_status(
                                solicitacao.status
                            ),
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),

                ft.Divider(),

                self._linha(
                    "Solicitação",
                    solicitacao.numero,
                ),

                self._linha(
                    "Solicitante",
                    self.solicitante,
                ),

                self._linha(
                    "Tipo de resíduo",
                    self._formatar_tipo_residuo(
                        solicitacao.tipo_residuo
                    ),
                ),

                self._linha(
                    "Acondicionamento",
                    self._formatar_quantidade(),
                ),

                self._linha(
                    "Peso estimado",
                    (
                        f"{solicitacao.peso_estimado_kg:,.0f} kg"
                        .replace(",", ".")
                    ),
                ),

                self._linha(
                    "Operação prevista",
                    self._formatar_operacao(),
                ),

                self._linha(
                    "Solicitada em",
                    self._formatar_data(
                        solicitacao.data_solicitacao
                    ),
                ),

                self._linha(
                    "Prioridade",
                    self._formatar_status(
                        solicitacao.prioridade
                    ),
                ),

                ft.Divider(),

                ft.Text(
                    "Observações do Gerador",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(
                    padding=16,
                    border_radius=10,
                    bgcolor=ft.Colors.GREY_100,
                    content=ft.Text(
                        solicitacao.observacao_cliente
                        or "Nenhuma observação informada."
                    ),
                ),

                ft.Divider(),

                ft.Text(
                    "Ações da solicitação",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),

                self._construir_acoes(),
            ],
            spacing=16,
        )

        return BasePage(
            title="Detalhes da Solicitação",
            subtitle=(
                "Analise as informações e acompanhe "
                "o fluxo operacional da coleta."
            ),
            content=conteudo,
            max_width=900,
        )