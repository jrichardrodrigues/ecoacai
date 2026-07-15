from collections.abc import Callable

import flet as ft

from models import SolicitacaoColeta


CORES_STATUS = {
    "PENDENTE": ft.Colors.AMBER,
    "AGENDADA": ft.Colors.BLUE,
    "EM_COLETA": ft.Colors.ORANGE,
    "CONCLUIDA": ft.Colors.GREEN,
}


class SolicitacaoCard(ft.Card):
    """Card reutilizável para exibir uma solicitação de coleta."""

    def __init__(
        self,
        solicitacao: SolicitacaoColeta,
        nome_estabelecimento: str,
        on_editar: Callable[[ft.ControlEvent], None] | None = None,
        on_status: Callable[[ft.ControlEvent], None] | None = None,
        on_maps: Callable[[ft.ControlEvent], None] | None = None,
        on_whatsapp: Callable[[ft.ControlEvent], None] | None = None,
    ) -> None:
        cor_status = CORES_STATUS.get(
            solicitacao.status,
            ft.Colors.GREY,
        )

        prioridade = str(
            solicitacao.prioridade or "NORMAL"
        ).upper()

        controles_cabecalho: list[ft.Control] = [
            ft.Text(
                solicitacao.numero,
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
        ]

        if prioridade == "URGENTE":
            controles_cabecalho.append(
                ft.Container(
                    bgcolor=ft.Colors.RED,
                    border_radius=16,
                    padding=6,
                    content=ft.Text(
                        "URGENTE",
                        size=11,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
            )

        controles_cabecalho.append(
            ft.Container(
                bgcolor=cor_status,
                border_radius=16,
                padding=8,
                content=ft.Text(
                    solicitacao.status.replace("_", " "),
                    size=12,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
            ),
        )

        detalhes: list[ft.Control] = [
            ft.Text(
                nome_estabelecimento,
                size=16,
                weight=ft.FontWeight.W_500,
            ),
            ft.Text(
                f"📦 {solicitacao.quantidade_sacas} sacas",
            ),
            ft.Text(
                f"⚖ {solicitacao.quantidade_kg:.1f} kg",
            ),
        ]

        if solicitacao.data_agendada:
            detalhes.append(
                ft.Text(
                    f"📅 Agendada: {solicitacao.data_agendada}",
                ),
            )

        if solicitacao.observacao:
            detalhes.append(
                ft.Text(
                    solicitacao.observacao,
                    italic=True,
                    color=ft.Colors.GREY_700,
                ),
            )

        botoes: list[ft.Control] = []

        if on_maps is not None:
            botoes.append(
                ft.IconButton(
                    icon=ft.Icons.MAP_OUTLINED,
                    tooltip="Abrir no Google Maps",
                    on_click=on_maps,
                ),
            )

        if on_whatsapp is not None:
            botoes.append(
                ft.IconButton(
                    icon=ft.Icons.CHAT_OUTLINED,
                    tooltip="Abrir WhatsApp",
                    on_click=on_whatsapp,
                ),
            )

        if on_editar is not None:
            botoes.append(
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    tooltip="Editar solicitação",
                    on_click=on_editar,
                ),
            )

        if on_status is not None:
            botoes.append(
                ft.IconButton(
                    icon=ft.Icons.SYNC_ALT,
                    tooltip="Alterar status",
                    on_click=on_status,
                ),
            )

        conteudo = ft.Column(
            controls=[
                ft.Row(
                    controls=controles_cabecalho,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                *detalhes,
                ft.Row(
                    controls=botoes,
                    alignment=ft.MainAxisAlignment.END,
                    spacing=4,
                ),
            ],
            spacing=10,
        )

        super().__init__(
            elevation=2,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=8,
                        bgcolor=cor_status,
                    ),
                    ft.Container(
                        content=conteudo,
                        padding=15,
                        expand=True,
                    ),
                ],
                spacing=0,
            ),
        )