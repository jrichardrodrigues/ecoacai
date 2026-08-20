from __future__ import annotations

from datetime import datetime
from typing import Any, Callable

import flet as ft

from config.constants import StatusColeta


class DetalheColetaView:
    """Exibe os detalhes operacionais de uma coleta."""

    def __init__(
        self,
        page: ft.Page,
        coleta: dict[str, Any],
        on_voltar: Callable[[], None],
    ) -> None:
        self.page = page
        self.coleta = coleta
        self.on_voltar = on_voltar

    def construir(self) -> ft.Control:
        """Constrói e retorna a tela de detalhes da coleta."""

        controles = [
            self._cabecalho(),
            ft.Divider(),
            self._barra_superior(),
            ft.Divider(),
            self._secao_identificacao(),
            ft.Divider(),
            self._secao_solicitacao(),
            ft.Divider(),
            self._secao_operacao(),
            ft.Divider(),
            self._secao_execucao(),
        ]

        status = self._texto(
            self.coleta.get("status"),
            "",
        ).strip().upper()

        if status == StatusColeta.CANCELADA:
            controles.extend(
                [
                    ft.Divider(),
                    self._secao_cancelamento(),
                ]
            )

        elif status == StatusColeta.RECUSADA:
            controles.extend(
                [
                    ft.Divider(),
                    self._secao_recusa(),
                ]
            )

        conteudo = ft.Column(
            controls=controles,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )

        card = ft.Container(
            width=900,
            padding=32,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(
                    0.10,
                    ft.Colors.BLACK,
                ),
                offset=ft.Offset(0, 2),
            ),
            content=conteudo,
        )

        return ft.Container(
            expand=True,
            padding=24,
            bgcolor=ft.Colors.GREY_50,
            alignment=ft.Alignment.TOP_CENTER,
            content=card,
        )

    def build(self) -> ft.Control:
        """Mantém compatibilidade com locais que utilizam build()."""

        return self.construir()

    def _cabecalho(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text(
                    "Detalhes da Coleta",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Consulte as informações da operação e "
                    "o histórico da coleta.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
            ],
            spacing=4,
        )

    def _barra_superior(self) -> ft.Control:
        return ft.Row(
            controls=[
                ft.OutlinedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.ARROW_BACK,
                                size=18,
                            ),
                            ft.Text("Voltar"),
                        ],
                        spacing=8,
                        tight=True,
                    ),
                    on_click=self._voltar,
                ),
                ft.Container(expand=True),
                ft.Text(
                    self._descricao_status(),
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _secao_identificacao(self) -> ft.Control:
        return ft.Column(
            controls=[
                self._titulo_secao("Identificação"),
                self._linha_dado(
                    "Coleta",
                    self._texto(
                        self.coleta.get("codigo"),
                        "-",
                    ),
                ),
                self._linha_dado(
                    "Status",
                    self._descricao_status(),
                ),
                self._linha_dado(
                    "Prioridade",
                    self._formatar_texto_codigo(
                        self.coleta.get("prioridade")
                    ),
                ),
            ],
            spacing=12,
        )

    def _secao_solicitacao(self) -> ft.Control:
        return ft.Column(
            controls=[
                self._titulo_secao("Solicitação"),
                self._linha_dado(
                    "Solicitante",
                    self._texto(
                        self.coleta.get(
                            "estabelecimento_nome"
                        ),
                        "Solicitante não identificado",
                    ),
                ),
                self._linha_dado(
                    "Tipo de resíduo",
                    self._formatar_tipo_residuo(
                        self.coleta.get("tipo_residuo")
                    ),
                ),
                self._linha_dado(
                    "Acondicionamento",
                    self._formatar_acondicionamento(),
                ),
                self._linha_dado(
                    "Peso estimado",
                    self._formatar_peso(
                        self.coleta.get(
                            "peso_estimado_kg"
                        )
                    ),
                ),
                self._linha_dado(
                    "Operação prevista",
                    self._formatar_tipo_operacao(
                        self.coleta.get("tipo_operacao")
                    ),
                ),
                self._linha_dado(
                    "Solicitada em",
                    self._formatar_data_hora(
                        self.coleta.get(
                            "data_solicitacao"
                        )
                    ),
                ),
                self._linha_dado(
                    "Observação do solicitante",
                    self._texto(
                        self.coleta.get(
                            "observacao_cliente"
                        ),
                        "Nenhuma observação informada.",
                    ),
                ),
            ],
            spacing=12,
        )

    def _secao_operacao(self) -> ft.Control:
        return ft.Column(
            controls=[
                self._titulo_secao("Operação"),
                self._linha_dado(
                    "Motorista",
                    self._texto(
                        self.coleta.get(
                            "motorista_nome"
                        ),
                        "Não informado",
                    ),
                ),
                self._linha_dado(
                    "Veículo",
                    self._formatar_veiculo(),
                ),
                self._linha_dado(
                    "Agendamento",
                    self._formatar_data_hora(
                        self.coleta.get(
                            "data_hora_agendada"
                        )
                    ),
                ),
                self._linha_dado(
                    "Início da coleta",
                    self._formatar_data_hora(
                        self.coleta.get(
                            "data_hora_inicio"
                        )
                    ),
                ),
                self._linha_dado(
                    "Chegada",
                    self._formatar_data_hora(
                        self.coleta.get(
                            "data_hora_chegada"
                        )
                    ),
                ),
                self._linha_dado(
                    "Conclusão",
                    self._formatar_data_hora(
                        self.coleta.get(
                            "data_hora_conclusao"
                        )
                    ),
                ),
            ],
            spacing=12,
        )

    def _secao_execucao(self) -> ft.Control:
        return ft.Column(
            controls=[
                self._titulo_secao("Execução"),
                self._linha_dado(
                    "Quantidade coletada",
                    self._formatar_quantidade_coletada(),
                ),
                self._linha_dado(
                    "Peso coletado",
                    self._formatar_peso(
                        self.coleta.get(
                            "quantidade_kg_coletado"
                        )
                    ),
                ),
                self._linha_dado(
                    "Observação operacional",
                    self._texto(
                        self.coleta.get(
                            "observacao_operacional"
                        ),
                        "Nenhuma observação registrada.",
                    ),
                ),
            ],
            spacing=12,
        )

    def _secao_cancelamento(self) -> ft.Control:
        """Exibe os dados de cancelamento da coleta."""

        return ft.Column(
            controls=[
                self._titulo_secao("Cancelamento"),
                self._linha_dado(
                    "Motivo",
                    self._texto(
                        self.coleta.get("motivo_cancelamento"),
                        "Não informado",
                    ),
                ),
                self._linha_dado(
                    "Cancelada em",
                    self._formatar_data_hora(
                        self.coleta.get(
                            "data_hora_cancelamento"
                        )
                    ),
                ),
            ],
            spacing=12,
        )

    def _secao_recusa(self) -> ft.Control:
        """Exibe os dados da recusa da solicitação."""

        return ft.Column(
            controls=[
                self._titulo_secao("Recusa"),
                self._linha_dado(
                    "Motivo",
                    self._texto(
                        self.coleta.get("motivo_recusa"),
                        padrao="Não informado",
                    ),
                ),
                self._linha_dado(
                    "Recusada em",
                    self._formatar_data_hora(
                        self.coleta.get(
                            "data_hora_recusa"
                        )
                    ),
                ),
            ],
            spacing=12,
        )

    @staticmethod
    def _titulo_secao(titulo: str) -> ft.Control:
        return ft.Text(
            titulo,
            size=17,
            weight=ft.FontWeight.BOLD,
        )

    @staticmethod
    def _linha_dado(
        rotulo: str,
        valor: str,
    ) -> ft.Control:
        return ft.Row(
            controls=[
                ft.Container(
                    width=190,
                    content=ft.Text(
                        rotulo,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                ft.Text(
                    valor,
                    selectable=True,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _voltar(
        self,
        _evento: ft.Event,
    ) -> None:
        self.on_voltar()

    def _descricao_status(self) -> str:
        status = self._texto(
            self.coleta.get("status"),
            "",
        )

        if not status:
            return "Não informado"

        try:
            return StatusColeta.descricao(status)
        except Exception:
            return self._formatar_texto_codigo(status)

    def _formatar_acondicionamento(self) -> str:
        forma = self._texto(
            self.coleta.get("forma_acondicionamento"),
            "",
        ).strip().upper()

        quantidade = self._inteiro(
            self.coleta.get("quantidade_prevista")
        )

        if forma == "BAG":
            unidade = "Bag" if quantidade == 1 else "Bags"
            return f"{quantidade} {unidade} (1 m³)"

        unidade = "Saca" if quantidade == 1 else "Sacas"
        return f"{quantidade} {unidade}"

    def _formatar_quantidade_coletada(self) -> str:
        forma = self._texto(
            self.coleta.get("forma_acondicionamento"),
            "",
        ).strip().upper()

        quantidade = self._inteiro(
            self.coleta.get(
                "quantidade_sacas_coletada"
            )
        )

        if quantidade <= 0:
            return "Não registrada"

        if forma == "BAG":
            unidade = "Bag" if quantidade == 1 else "Bags"
            return f"{quantidade} {unidade}"

        unidade = "Saca" if quantidade == 1 else "Sacas"
        return f"{quantidade} {unidade}"

    def _formatar_veiculo(self) -> str:
        placa = self._texto(
            self.coleta.get("veiculo_placa"),
            "",
        ).strip()

        marca = self._texto(
            self.coleta.get("veiculo_marca"),
            "",
        ).strip()

        modelo = self._texto(
            self.coleta.get("veiculo_modelo"),
            "",
        ).strip()

        if placa and (marca or modelo):
            descricao = " ".join(
                parte
                for parte in [marca, modelo]
                if parte
            )
            return f"{placa} • {descricao}"

        partes = [
            parte
            for parte in [placa, marca, modelo]
            if parte
        ]

        return " ".join(partes) or "Não informado"

    @staticmethod
    def _formatar_tipo_residuo(
        valor: Any,
    ) -> str:
        texto = str(valor or "").strip().upper()

        descricoes = {
            "CAROCO_ACAI": "Caroço de Açaí",
        }

        return descricoes.get(
            texto,
            DetalheColetaView._formatar_texto_codigo(
                texto
            ),
        )

    @staticmethod
    def _formatar_tipo_operacao(
        valor: Any,
    ) -> str:
        texto = str(valor or "").strip().upper()

        descricoes = {
            "MUNCK": "Caminhão Munck",
            "MANUAL": "Coleta manual",
        }

        return descricoes.get(
            texto,
            DetalheColetaView._formatar_texto_codigo(
                texto
            ),
        )

    @staticmethod
    def _formatar_data_hora(
        valor: Any,
    ) -> str:
        texto = str(valor or "").strip()

        if not texto:
            return "Não registrado"

        formatos = (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M",
        )

        for formato in formatos:
            try:
                data_hora = datetime.strptime(
                    texto,
                    formato,
                )
                return data_hora.strftime(
                    "%d/%m/%Y %H:%M"
                )
            except ValueError:
                continue

        return texto

    @staticmethod
    def _formatar_peso(
        valor: Any,
    ) -> str:
        try:
            peso = float(valor or 0)
        except (TypeError, ValueError):
            return "Não registrado"

        if peso <= 0:
            return "Não registrado"

        return (
            f"{peso:,.0f} kg"
            .replace(",", ".")
        )

    @staticmethod
    def _formatar_texto_codigo(
        valor: Any,
    ) -> str:
        texto = str(valor or "").strip()

        if not texto:
            return "Não informado"

        return texto.replace("_", " ").title()

    @staticmethod
    def _texto(
        valor: Any,
        padrao: str,
    ) -> str:
        texto = str(valor or "").strip()
        return texto or padrao

    @staticmethod
    def _inteiro(
        valor: Any,
    ) -> int:
        try:
            return int(valor or 0)
        except (TypeError, ValueError):
            return 0
