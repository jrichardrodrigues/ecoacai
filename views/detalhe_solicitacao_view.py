from __future__ import annotations

from datetime import datetime
from collections.abc import Callable

import flet as ft

from components.layout import BasePage
from models import SolicitacaoColeta


class DetalheSolicitacaoView:
    """Exibe os detalhes de uma solicitação do Gerador."""

    def __init__(
        self,
        *,
        solicitacao: SolicitacaoColeta,
        on_voltar: Callable[[], None],
    ) -> None:
        self.solicitacao = solicitacao
        self.on_voltar = on_voltar

    @staticmethod
    def _formatar_status(status: str) -> str:
        return str(status or "").replace("_", " ").title()

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

    def _formatar_quantidade(self) -> str:
        quantidade = self.solicitacao.quantidade_prevista

        forma = str(
            self.solicitacao.forma_acondicionamento or ""
        ).strip().upper()

        if forma == "BAG":
            unidade = "Bag" if quantidade == 1 else "Bags"
            return f"{quantidade} {unidade} (1 m³)"

        unidade = "Saca" if quantidade == 1 else "Sacas"
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
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def build(self) -> ft.Control:
        solicitacao = self.solicitacao

        conteudo = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            content="Voltar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _e: self.on_voltar(),
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
                    f"{solicitacao.peso_estimado_kg:,.0f} kg".replace(
                        ",",
                        ".",
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
                    "Observações",
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
            ],
            spacing=16,
        )

        return BasePage(
            title="Detalhes da Solicitação",
            subtitle=(
                "Consulte as informações da solicitação de coleta."
            ),
            content=conteudo,
            max_width=900,
        )