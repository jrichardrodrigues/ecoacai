from __future__ import annotations

from datetime import datetime
from typing import Callable

import flet as ft

from components.layout import BasePage
from models import SolicitacaoColeta


class MinhasSolicitacoesView:
    """Lista as solicitações de coleta do Gerador."""

    def __init__(
        self,
        *,
        solicitacoes: list[SolicitacaoColeta],
        on_voltar: Callable[[], None],
        on_nova_solicitacao: Callable[[], None],
        on_ver_detalhes: Callable[[SolicitacaoColeta], None],
    ) -> None:
        self.solicitacoes = solicitacoes
        self.on_voltar = on_voltar
        self.on_nova_solicitacao = on_nova_solicitacao
        self.on_ver_detalhes = on_ver_detalhes

    @staticmethod
    def _formatar_status(status: str) -> str:
        return str(status or "").replace("_", " ").title()

    @staticmethod
    def _formatar_quantidade(
        solicitacao: SolicitacaoColeta,
    ) -> str:
        forma = str(
            solicitacao.forma_acondicionamento or ""
        ).strip().upper()

        quantidade = solicitacao.quantidade_prevista

        if forma == "BAG":
            unidade = "Bag" if quantidade == 1 else "Bags"
            return f"{quantidade} {unidade} (1 m³)"

        unidade = "Saca" if quantidade == 1 else "Sacas"
        return f"{quantidade} {unidade}"

    @staticmethod
    def _formatar_tipo_residuo(tipo_residuo: str) -> str:
        tipos = {
            "CAROCO_ACAI": "Caroço de Açaí",
        }

        return tipos.get(
            tipo_residuo,
            tipo_residuo,
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

    def _construir_card(
        self,
        solicitacao: SolicitacaoColeta,
    ) -> ft.Control:
        quantidade_texto = self._formatar_quantidade(
            solicitacao
        )

        tipo_residuo_texto = self._formatar_tipo_residuo(
            solicitacao.tipo_residuo
        )

        data_texto = self._formatar_data(
            solicitacao.data_solicitacao
        )

        return ft.Card(
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
                                ft.TextButton(
                                    content="Ver detalhes",
                                    icon=ft.Icons.VISIBILITY_OUTLINED,
                                    on_click=lambda _e, s=solicitacao: (
                                        self.on_ver_detalhes(s)
                                    ),
                                ),
                                ft.Text(
                                    self._formatar_status(
                                        solicitacao.status
                                    ),
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                        ft.Text(
                            "Tipo de resíduo: "
                            f"{tipo_residuo_texto}"
                        ),
                        ft.Text(
                            "Quantidade prevista: "
                            f"{quantidade_texto}"
                        ),
                        ft.Text(
                            f"Solicitada em: {data_texto}"
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

    def _construir_estado_vazio(self) -> ft.Control:
        return ft.Container(
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
                        on_click=lambda _e: (
                            self.on_nova_solicitacao()
                        ),
                    ),
                ],
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=12,
            ),
        )

    def build(self) -> ft.Control:
        cards: list[ft.Control] = [
            self._construir_card(solicitacao)
            for solicitacao in self.solicitacoes
        ]

        if not cards:
            cards.append(
                self._construir_estado_vazio()
            )

        conteudo = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            content="Voltar ao portal",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _e: self.on_voltar(),
                        ),
                        ft.Container(expand=True),
                        ft.FilledButton(
                            content="Nova solicitação",
                            icon=ft.Icons.ADD,
                            on_click=lambda _e: (
                                self.on_nova_solicitacao()
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    "Total de solicitações: "
                    f"{len(self.solicitacoes)}"
                ),
                ft.Column(
                    controls=cards,
                    spacing=12,
                ),
            ],
            spacing=16,
        )

        return BasePage(
            title="Minhas Solicitações",
            subtitle=(
                "Acompanhe as solicitações de coleta "
                "da sua organização."
            ),
            content=conteudo,
            max_width=1000,
        )