from __future__ import annotations

from datetime import date, datetime, time
from typing import Any, Callable

import flet as ft

from controllers.coletas_agendadas_controller import (
    ColetasAgendadasController,
)
from controllers.motorista_controller import MotoristaController
from controllers.veiculo_controller import VeiculoController
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)

from components.buttons import PrimaryButton, SecondaryButton
from components.responsive import (
    ResponsiveFilterBar,
    ResponsiveHeader,
)

from config.constants import StatusColeta


class ColetasAgendadasView:
    """
    Tela de gerenciamento da agenda de coletas.

    Esta primeira versão contém:
    - cabeçalho;
    - filtros;
    - indicadores;
    - tabela;
    - integração inicial com o Controller.
    """

    _STATUS_VALIDOS = {
        StatusColeta.SOLICITADA,
        StatusColeta.EM_ANALISE,
        StatusColeta.AGENDADA,
        StatusColeta.EM_DESLOCAMENTO,
        StatusColeta.EM_COLETA,
        StatusColeta.CONCLUIDA,
        StatusColeta.CANCELADA,
        StatusColeta.RECUSADA,
    }

    def __init__(
            self,
            page: ft.Page,
            controller: ColetasAgendadasController | None = None,
            on_visualizar_coleta: Callable[[dict], None] | None = None,
    ) -> None:
        self.page = page

        self.controller = (
            controller
            if controller is not None
            else ColetasAgendadasController()
        )

        self.on_visualizar_coleta = on_visualizar_coleta

        self.motorista_controller = MotoristaController()

        self.veiculo_controller = VeiculoController()

        self.solicitacao_controller = (
            SolicitacaoColetaController()
        )

        # Estado do diálogo de agendamento/reagendamento
        self.modo_dialog_agendamento = "AGENDAR"
        self.solicitacao_reagendamento_id: int | None = None

        self._construir_controles()
        self._construir_dialog_agendamento()
        self._construir_dialog_conclusao()
        self._construir_dialog_cancelamento()
        self._construir_dialog_recusa()

    # ==========================================================
    # CONSTRUÇÃO
    # ==========================================================

    def _construir_controles(self) -> None:
        """Cria os controles utilizados pela tela."""

        hoje = date.today()

        self.campo_data_inicial = ft.TextField(
            label="Data inicial",
            value=hoje.strftime("%d/%m/%Y"),
            width=150,
            dense=True,
            read_only=True,
            on_click=self._abrir_seletor_data_inicial,
        )

        self.campo_data_final = ft.TextField(
            label="Data final",
            value=hoje.strftime("%d/%m/%Y"),
            width=150,
            dense=True,
            read_only=True,
            on_click=self._abrir_seletor_data_final,
        )

        self.dropdown_status = ft.Dropdown(
            label="Status",
            width=180,
            dense=True,
            value="TODOS",
            options=[
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                ),
                ft.DropdownOption(
                    key=StatusColeta.SOLICITADA,
                    text="Solicitada",
                ),
                ft.DropdownOption(
                    key=StatusColeta.EM_ANALISE,
                    text="Em análise",
                ),
                ft.DropdownOption(
                    key=StatusColeta.AGENDADA,
                    text="Agendada",
                ),
                ft.DropdownOption(
                    key=StatusColeta.EM_DESLOCAMENTO,
                    text="Em deslocamento",
                ),
                ft.DropdownOption(
                    key=StatusColeta.EM_COLETA,
                    text="Em coleta",
                ),
                ft.DropdownOption(
                    key=StatusColeta.CONCLUIDA,
                    text="Concluída",
                ),
                ft.DropdownOption(
                    key=StatusColeta.CANCELADA,
                    text="Cancelada",
                ),
                ft.DropdownOption(
                    key=StatusColeta.RECUSADA,
                    text="Recusada",
                ),
            ],
        )

        self.dropdown_status.on_change = self._ao_alterar_status

        self.dropdown_motorista = ft.Dropdown(
            label="Motorista",
            dense=True,
            value="TODOS",
            width=220,
            options=[
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                ),
            ],
        )

        self.dropdown_veiculo = ft.Dropdown(
            label="Veículo",
            dense=True,
            value="TODOS",
            width=180,
            options=[
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                ),
            ],
        )

        self.texto_mensagem = ft.Text(
            value="",
            size=13,
        )

        self.texto_total_pendentes = self._criar_texto_total()
        self.texto_total_agendadas = self._criar_texto_total()
        self.texto_total_em_deslocamento = self._criar_texto_total()
        self.texto_total_em_coleta = self._criar_texto_total()
        self.texto_total_concluidas = self._criar_texto_total()
        self.texto_total_canceladas = self._criar_texto_total()

        self.cards_status: dict[str, ft.Container] = {}

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text("Código"),
                ),
                ft.DataColumn(
                    ft.Text("Solicitante"),
                ),
                ft.DataColumn(
                    ft.Text("Sacas"),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text("Bags"),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text("Motorista"),
                ),
                ft.DataColumn(
                    ft.Text("Veículo"),
                ),
                ft.DataColumn(
                    ft.Text("Agendamento"),
                ),
                ft.DataColumn(
                    ft.Text("Status"),
                ),
                ft.DataColumn(
                    ft.Text("Ações"),
                ),
            ],
            rows=[],
            heading_row_height=50,
            data_row_min_height=52,
            data_row_max_height=64,
            column_spacing=24,
            horizontal_margin=16,
        )

        self.indicador_carregamento = ft.ProgressRing(
            width=22,
            height=22,
            visible=False,
        )

    def _criar_filtros(self) -> ft.Control:
        """Cria a área de filtros."""

        botao_pesquisar = PrimaryButton(
            label="Pesquisar",
            icon=ft.Icons.SEARCH,
            on_click=self._pesquisar,
        )

        botao_limpar = SecondaryButton(
            label="Limpar",
            icon=ft.Icons.CLEAR,
            on_click=self._limpar_filtros,
        )

        linha_campos = ft.Row(
            controls=[
                self.campo_data_inicial,
                self.campo_data_final,
                self.dropdown_status,
                self.dropdown_motorista,
                self.dropdown_veiculo,
            ],
            spacing=12,
            run_spacing=12,
            wrap=True,
        )

        linha_botoes = ft.Row(
            controls=[
                botao_pesquisar,
                botao_limpar,
            ],
            spacing=12,
        )

        return ft.Column(
            controls=[
                linha_campos,
                linha_botoes,
            ],
            spacing=12,
        )

    def _construir_dialog_agendamento(self) -> None:
        """
        Cria os controles e o AlertDialog utilizado para agendar
        ou reagendar uma solicitação de coleta.
        """

        amanha = date.today().fromordinal(
            date.today().toordinal() + 1
        )

        self.dropdown_solicitacao_dialog = ft.Dropdown(
            label="Solicitação em análise",
            hint_text="Selecione uma solicitação",
            width=520,
            dense=True,
            options=[],
        )

        self.campo_data_agendamento = ft.TextField(
            label="Data",
            value=amanha.strftime("%d/%m/%Y"),
            width=210,
            dense=True,
            read_only=True,
            on_click=self._abrir_seletor_data,
        )

        self.botao_selecionar_data = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            tooltip="Selecionar data",
            on_click=self._abrir_seletor_data,
        )

        self.campo_hora_agendamento = ft.TextField(
            label="Hora",
            value="08:00",
            width=210,
            dense=True,
            read_only=True,
            on_click=self._abrir_seletor_hora,
        )

        self.botao_selecionar_hora = ft.IconButton(
            icon=ft.Icons.ACCESS_TIME,
            tooltip="Selecionar hora",
            on_click=self._abrir_seletor_hora,
        )

        self.dropdown_motorista_dialog = ft.Dropdown(
            label="Motorista",
            hint_text="Selecione um motorista",
            width=520,
            dense=True,
            options=[],
            on_select=self._ao_selecionar_motorista_dialog,
        )

        self.dropdown_veiculo_dialog = ft.Dropdown(
            label="Veículo",
            hint_text="Selecione um veículo",
            width=520,
            dense=True,
            options=[],
        )

        self.texto_mensagem_dialog = ft.Text(
            value="",
            size=13,
            color=ft.Colors.RED,
            visible=False,
        )

        self.indicador_dialog = ft.ProgressRing(
            width=22,
            height=22,
            visible=False,
        )

        self.botao_confirmar_agendamento = ft.FilledButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.EVENT_AVAILABLE,
                        size=18,
                    ),
                    ft.Text("Agendar"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._confirmar_agendamento,
        )

        self.botao_cancelar_agendamento = ft.OutlinedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CLOSE,
                        size=18,
                    ),
                    ft.Text("Cancelar"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._fechar_dialog_agendamento,
        )

        self.texto_instrucao_dialog = ft.Text(
            "Selecione uma solicitação em análise e informe "
            "os dados do agendamento.",
            size=13,
        )

        conteudo_dialog = ft.Column(
            controls=[
                self.texto_instrucao_dialog,
                self.dropdown_solicitacao_dialog,
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                self.campo_data_agendamento,
                                self.botao_selecionar_data,
                            ],
                            spacing=4,
                            tight=True,
                        ),
                        ft.Row(
                            controls=[
                                self.campo_hora_agendamento,
                                self.botao_selecionar_hora,
                            ],
                            spacing=4,
                            tight=True,
                        ),
                    ],
                    spacing=16,
                    wrap=True,
                ),
                self.dropdown_motorista_dialog,
                self.dropdown_veiculo_dialog,
                self.texto_mensagem_dialog,
            ],
            spacing=16,
            tight=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self.dialog_agendamento = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CALENDAR_MONTH,
                        size=24,
                    ),
                    ft.Text(
                        "Agendar coleta",
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=ft.Container(
                content=conteudo_dialog,
                width=540,
            ),
            actions=[
                self.indicador_dialog,
                self.botao_cancelar_agendamento,
                self.botao_confirmar_agendamento,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _construir_dialog_conclusao(self) -> None:
        """Cria o diálogo utilizado para concluir uma coleta."""

        self.solicitacao_conclusao_id: int | None = None

        self.texto_coleta_conclusao = ft.Text(
            "",
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        self.texto_previsto_conclusao = ft.Text(
            "",
            size=13,
        )

        self.campo_quantidade_coletada = ft.TextField(
            label="Quantidade coletada",
            width=250,
            dense=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._atualizar_peso_coletado,
        )

        self.campo_peso_coletado = ft.TextField(
            label="Peso coletado (kg)",
            width=250,
            dense=True,
            read_only=True,
        )

        self.campo_observacao_operacional = ft.TextField(
            label="Observação operacional",
            hint_text="Opcional",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=520,
        )

        self.texto_mensagem_conclusao = ft.Text(
            "",
            size=13,
            color=ft.Colors.RED,
            visible=False,
        )

        self.botao_confirmar_conclusao = ft.FilledButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE,
                        size=18,
                    ),
                    ft.Text("Concluir"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._confirmar_conclusao,
        )

        self.botao_cancelar_conclusao = ft.OutlinedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CLOSE,
                        size=18,
                    ),
                    ft.Text("Cancelar"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._fechar_dialog_conclusao,
        )

        self.dialog_conclusao = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE,
                        size=24,
                    ),
                    ft.Text(
                        "Concluir coleta",
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=ft.Container(
                width=540,
                content=ft.Column(
                    controls=[
                        self.texto_coleta_conclusao,
                        self.texto_previsto_conclusao,
                        ft.Row(
                            controls=[
                                self.campo_quantidade_coletada,
                                self.campo_peso_coletado,
                            ],
                            spacing=16,
                            wrap=True,
                        ),
                        self.campo_observacao_operacional,
                        self.texto_mensagem_conclusao,
                    ],
                    spacing=16,
                    tight=True,
                ),
            ),
            actions=[
                self.botao_cancelar_conclusao,
                self.botao_confirmar_conclusao,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _construir_dialog_cancelamento(self) -> None:
        """Cria o diálogo utilizado para cancelar uma coleta."""

        self.solicitacao_cancelamento_id: int | None = None

        self.texto_coleta_cancelamento = ft.Text(
            "",
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        self.campo_motivo_cancelamento = ft.TextField(
            label="Motivo do cancelamento",
            hint_text="Informe o motivo do cancelamento",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=520,
        )

        self.texto_mensagem_cancelamento = ft.Text(
            "",
            size=13,
            color=ft.Colors.RED,
            visible=False,
        )

        self.botao_cancelar_dialog_cancelamento = ft.OutlinedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CLOSE,
                        size=18,
                    ),
                    ft.Text("Voltar"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._fechar_dialog_cancelamento,
        )

        self.botao_confirmar_cancelamento = ft.FilledButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CANCEL,
                        size=18,
                    ),
                    ft.Text("Cancelar coleta"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._confirmar_cancelamento,
        )

        self.dialog_cancelamento = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CANCEL_OUTLINED,
                        size=24,
                    ),
                    ft.Text(
                        "Cancelar coleta",
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=ft.Container(
                width=540,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "A coleta permanecerá no histórico "
                            "com status Cancelada.",
                            size=13,
                        ),
                        self.texto_coleta_cancelamento,
                        self.campo_motivo_cancelamento,
                        self.texto_mensagem_cancelamento,
                    ],
                    spacing=16,
                    tight=True,
                ),
            ),
            actions=[
                self.botao_cancelar_dialog_cancelamento,
                self.botao_confirmar_cancelamento,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _construir_dialog_recusa(self) -> None:
        """Cria o diálogo utilizado para recusar uma solicitação."""

        self.solicitacao_recusa_id: int | None = None

        self.texto_coleta_recusa = ft.Text(
            "",
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        self.campo_motivo_recusa = ft.TextField(
            label="Motivo da recusa",
            hint_text="Informe o motivo da recusa",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=520,
        )

        self.texto_mensagem_recusa = ft.Text(
            "",
            size=13,
            color=ft.Colors.RED,
            visible=False,
        )

        self.botao_cancelar_dialog_recusa = ft.OutlinedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CLOSE,
                        size=18,
                    ),
                    ft.Text("Voltar"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._fechar_dialog_recusa,
        )

        self.botao_confirmar_recusa = ft.FilledButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.BLOCK,
                        size=18,
                    ),
                    ft.Text("Recusar solicitação"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._confirmar_recusa,
        )

        self.dialog_recusa = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.BLOCK,
                        size=24,
                    ),
                    ft.Text(
                        "Recusar solicitação",
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=ft.Container(
                width=540,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "A solicitação permanecerá no histórico "
                            "com status Recusada.",
                            size=13,
                        ),
                        self.texto_coleta_recusa,
                        self.campo_motivo_recusa,
                        self.texto_mensagem_recusa,
                    ],
                    spacing=16,
                    tight=True,
                ),
            ),
            actions=[
                self.botao_cancelar_dialog_recusa,
                self.botao_confirmar_recusa,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _fechar_dialog_cancelamento(
            self,
            _evento: ft.Event | None = None,
    ) -> None:
        """Fecha o diálogo de cancelamento."""

        self.page.pop_dialog()

        self.solicitacao_cancelamento_id = None

    def _confirmar_cancelamento(
            self,
            _evento: ft.Event,
    ) -> None:
        """Valida e confirma o cancelamento da coleta."""

        if self.solicitacao_cancelamento_id is None:
            self.texto_mensagem_cancelamento.value = (
                "Não foi possível identificar a coleta."
            )
            self.texto_mensagem_cancelamento.visible = True
            self._atualizar_pagina()
            return

        motivo = str(
            self.campo_motivo_cancelamento.value or ""
        ).strip()

        if not motivo:
            self.texto_mensagem_cancelamento.value = (
                "Informe o motivo do cancelamento."
            )
            self.texto_mensagem_cancelamento.visible = True
            self._atualizar_pagina()
            return

        resultado = self.controller.cancelar_coleta(
            solicitacao_id=self.solicitacao_cancelamento_id,
            motivo=motivo,
        )

        if resultado.falhou:
            self.texto_mensagem_cancelamento.value = (
                resultado.mensagem
            )
            self.texto_mensagem_cancelamento.visible = True
            self._atualizar_pagina()
            return

        self.page.pop_dialog()

        self.solicitacao_cancelamento_id = None

        self._processar_resultado_operacao(
            resultado
        )

    def _fechar_dialog_conclusao(
            self,
            _=None,
    ) -> None:
        """Fecha o diálogo de conclusão da coleta."""

        self.page.pop_dialog()

    def _confirmar_conclusao(
            self,
            _evento: ft.Event,
    ) -> None:
        """Valida e conclui a coleta com os dados informados."""

        if self.solicitacao_conclusao_id is None:
            self.texto_mensagem_conclusao.value = (
                "Não foi possível identificar a coleta."
            )
            self.texto_mensagem_conclusao.visible = True
            self._atualizar_pagina()
            return

        try:
            quantidade = int(
                str(
                    self.campo_quantidade_coletada.value
                    or ""
                ).strip()
            )
        except ValueError:
            self.texto_mensagem_conclusao.value = (
                "Informe uma quantidade coletada válida."
            )
            self.texto_mensagem_conclusao.visible = True
            self._atualizar_pagina()
            return

        try:
            peso = float(
                str(
                    self.campo_peso_coletado.value
                    or ""
                )
                .strip()
                .replace(",", ".")
            )
        except ValueError:
            self.texto_mensagem_conclusao.value = (
                "Informe um peso coletado válido."
            )
            self.texto_mensagem_conclusao.visible = True
            self._atualizar_pagina()
            return

        observacao = str(
            self.campo_observacao_operacional.value
            or ""
        ).strip()

        resultado = self.controller.concluir_coleta(
            solicitacao_id=self.solicitacao_conclusao_id,
            quantidade_coletada=quantidade,
            peso_coletado_kg=peso,
            observacao_operacional=observacao,
        )

        if resultado.falhou:
            self.texto_mensagem_conclusao.value = (
                resultado.mensagem
            )
            self.texto_mensagem_conclusao.visible = True
            self._atualizar_pagina()
            return

        self.page.pop_dialog()

        self.solicitacao_conclusao_id = None

        self._processar_resultado_operacao(
            resultado
        )

    ##################################################################################
    # EVENTOS
    ##################################################################################

    def _fechar_dialog_agendamento(
            self,
            _evento: ft.Event | None = None,
    ) -> None:
        """Fecha o diálogo de agendamento."""

        self.page.pop_dialog()

    def _confirmar_agendamento(
            self,
            _evento: ft.Event,
    ) -> None:
        """
        Confirma o agendamento da coleta.
        """

        if not self._validar_dialog_agendamento():
            return

        try:
            solicitacao_id = self._obter_solicitacao_id()
            motorista_id = self._obter_motorista_id()
            veiculo_id = self._obter_veiculo_id()
            data_hora = self._obter_data_hora_agendamento()

        except ValueError:
            self.texto_mensagem_dialog.value = (
                "Data ou hora inválida."
            )
            self.texto_mensagem_dialog.color = ft.Colors.RED
            self.texto_mensagem_dialog.visible = True
            self._atualizar_pagina()
            return

        self.indicador_dialog.visible = True
        self.botao_confirmar_agendamento.disabled = True

        resultado = self.controller.agendar(
            solicitacao_id=solicitacao_id,
            data_hora_agendada=data_hora,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
        )

        self.indicador_dialog.visible = False
        self.botao_confirmar_agendamento.disabled = False

        if resultado.falhou:
            self.texto_mensagem_dialog.value = resultado.mensagem
            self.texto_mensagem_dialog.color = ft.Colors.RED
            self.texto_mensagem_dialog.visible = True
            self._atualizar_pagina()
            return

        self.page.pop_dialog()

        self._mostrar_mensagem(
            resultado.mensagem,
            erro=False,
        )

        self._carregar_motoristas()
        self._carregar_veiculos()
        self.carregar_dados()

        self._atualizar_pagina()

    ##################################################################################

    def build(self) -> ft.Control:
        """Monta e retorna o conteúdo principal da tela."""

        conteudo = ft.Column(
            controls=[
                self._criar_cabecalho(),
                self._criar_filtros(),
                self._criar_dashboard(),
                self._criar_area_mensagem(),
                self._criar_tabela(),
            ],
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        controle = ft.Container(
            content=conteudo,
            padding=ft.Padding(
                left=24,
                top=22,
                right=24,
                bottom=24,
            ),
            expand=True,
        )

        self._carregar_motoristas()

        self._carregar_veiculos()

        self.carregar_dados()

        return controle

    def _criar_cabecalho(self) -> ft.Control:
        """Cria o cabeçalho da tela."""

        return ResponsiveHeader(
            title="Operação de Coletas",
            subtitle=(
                "Gerencie o fluxo operacional das coletas, "
                "do agendamento à conclusão."
            ),
            action_label="Agendar Coleta",
            action_icon=ft.Icons.ADD,
            on_action=self._nova_coleta,
        )

    def _criar_dashboard(self) -> ft.Control:
        """Cria os cards com os indicadores da agenda."""

        cards = [
            self._criar_card_indicador(
                titulo="Em análise",
                texto_total=self.texto_total_pendentes,
                icone=ft.Icons.PENDING_ACTIONS,
                status=StatusColeta.EM_ANALISE,
            ),
            self._criar_card_indicador(
                titulo="Agendadas",
                texto_total=self.texto_total_agendadas,
                icone=ft.Icons.EVENT_AVAILABLE,
                status=StatusColeta.AGENDADA,
            ),
            self._criar_card_indicador(
                titulo="Em deslocamento",
                texto_total=self.texto_total_em_deslocamento,
                icone=ft.Icons.LOCAL_SHIPPING_OUTLINED,
                status=StatusColeta.EM_DESLOCAMENTO,
            ),
            self._criar_card_indicador(
                titulo="Em coleta",
                texto_total=self.texto_total_em_coleta,
                icone=ft.Icons.LOCAL_SHIPPING,
                status=StatusColeta.EM_COLETA,
            ),
            self._criar_card_indicador(
                titulo="Concluídas",
                texto_total=self.texto_total_concluidas,
                icone=ft.Icons.CHECK_CIRCLE,
                status=StatusColeta.CONCLUIDA,
            ),
            self._criar_card_indicador(
                titulo="Canceladas",
                texto_total=self.texto_total_canceladas,
                icone=ft.Icons.CANCEL,
                status=StatusColeta.CANCELADA,
            ),
        ]

        return ft.Row(
            controls=cards,
            spacing=14,
            run_spacing=14,
            wrap=True,
        )

    def _criar_card_indicador(
            self,
            *,
            titulo: str,
            texto_total: ft.Text,
            icone: Any,
            status: str | None = None,
    ) -> ft.Control:
        """Cria um card de indicador clicável."""

        def ao_clicar(_e) -> None:
            if status is None:
                return

            self.dropdown_status.value = status
            self._atualizar_destaque_cards(status)
            self._pesquisar(None)

        card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            icone,
                            size=26,
                        ),
                        width=42,
                        height=42,
                        alignment=ft.Alignment.CENTER,
                        border_radius=10,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                titulo,
                                size=13,
                            ),
                            texto_total,
                        ],
                        spacing=2,
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=178,
            padding=12,
            border=ft.Border.all(
                width=1,
            ),
            border_radius=12,
            ink=True,
            on_click=(
                ao_clicar
                if status is not None
                else None
            ),
        )

        if status is not None:
            self.cards_status[status] = card

        return card

    def _ao_alterar_status(
            self,
            _evento: ft.Event,
    ) -> None:
        """Atualiza o destaque ao alterar o status no dropdown."""

        status = self._status_selecionado()

        self._atualizar_destaque_cards(status)

    def _atualizar_destaque_cards(
            self,
            status_selecionado: str | None,
    ) -> None:
        """Destaca visualmente o card do status selecionado."""

        for status, card in self.cards_status.items():
            selecionado = status == status_selecionado

            card.bgcolor = (
                ft.Colors.with_opacity(
                    0.08,
                    ft.Colors.BLUE_700,
                )
                if selecionado
                else None
            )

            card.border = ft.Border.all(
                width=2 if selecionado else 1,
                color=(
                    ft.Colors.BLUE_700
                    if selecionado
                    else ft.Colors.BLACK26
                ),
            )

        self._atualizar_pagina()

    def _criar_area_mensagem(self) -> ft.Control:
        """Cria a área de mensagens da tela."""

        return ft.Container(
            content=self.texto_mensagem,
            visible=True,
        )

    def _criar_tabela(self) -> ft.Control:
        """Cria a área responsiva da tabela."""

        cabecalho_tabela = ft.Row(
            controls=[
                ft.Text(
                    "Agenda de coletas",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    tooltip="Atualizar",
                    on_click=self._atualizar,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        tabela_com_rolagem = ft.Row(
            controls=[
                self.tabela,
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    cabecalho_tabela,
                    ft.Divider(),
                    tabela_com_rolagem,
                ],
                spacing=10,
            ),
            padding=16,
            border=ft.Border.all(
                width=1,
            ),
            border_radius=12,
            width=float("inf"),
        )

    @staticmethod
    def _criar_texto_total() -> ft.Text:
        """Cria o texto numérico de um indicador."""

        return ft.Text(
            value="0",
            size=24,
            weight=ft.FontWeight.BOLD,
        )

    def _abrir_seletor_data(
        self,
        _evento: ft.Event,
    ) -> None:
        """Abre o calendário para seleção da data."""

        hoje = date.today()

        seletor = ft.DatePicker(
            first_date=hoje,
            last_date=date(
                hoje.year + 2,
                12,
                31,
            ),
            on_change=self._ao_selecionar_data,
        )

        self.page.show_dialog(seletor)

    def _ao_selecionar_data(
            self,
            evento: ft.Event,
    ) -> None:
        """Atualiza o campo de data após a seleção."""

        valor = evento.control.value

        if valor is None:
            return

        self.campo_data_agendamento.value = (
            valor.strftime("%d/%m/%Y")
        )

        self._atualizar_pagina()

    def _abrir_seletor_hora(
            self,
            _evento: ft.Event,
    ) -> None:
        """Abre o seletor no horário atualmente informado."""

        try:
            hora_atual = datetime.strptime(
                self.campo_hora_agendamento.value,
                "%H:%M",
            ).time()
        except (ValueError, TypeError):
            hora_atual = time(8, 0)

        seletor = ft.TimePicker(
            value=hora_atual,
            hour_format=ft.TimePickerHourFormat.H24,
            on_change=self._ao_selecionar_hora,
        )

        self.page.show_dialog(seletor)

    def _ao_selecionar_hora(
            self,
            evento: ft.Event,
    ) -> None:
        """Atualiza o horário escolhido no formulário."""

        valor = evento.control.value

        if valor is None:
            return

        self.campo_hora_agendamento.value = (
            valor.strftime("%H:%M")
        )

        self._atualizar_pagina()

    # ==========================================================
    # CARREGAMENTO
    # ==========================================================

    def carregar_dados(self) -> None:
        """Carrega indicadores e registros iniciais."""

        self._definir_carregamento(True)

        try:
            self._carregar_dashboard()
            self._carregar_tabela()

        finally:
            self._definir_carregamento(False)

    def _carregar_dashboard(self) -> None:
        """Carrega os totais agrupados por status."""

        resultado = self.controller.total_por_status()

        if resultado.falhou:
            self._mostrar_mensagem(
                resultado.mensagem,
                erro=True,
            )
            return

        totais = resultado.dados or {}

        self.texto_total_pendentes.value = str(
            totais.get(StatusColeta.EM_ANALISE, 0)
        )

        self.texto_total_agendadas.value = str(
            totais.get(StatusColeta.AGENDADA, 0)
        )

        self.texto_total_em_deslocamento.value = str(
            totais.get(StatusColeta.EM_DESLOCAMENTO, 0)
        )

        self.texto_total_em_coleta.value = str(
            totais.get(StatusColeta.EM_COLETA, 0)
        )

        self.texto_total_concluidas.value = str(
            totais.get(StatusColeta.CONCLUIDA, 0)
        )

        self.texto_total_canceladas.value = str(
            totais.get(StatusColeta.CANCELADA, 0)
        )

    def _carregar_tabela(self) -> None:
        """Carrega a tabela aplicando os filtros atuais."""

        data_inicial = self._valor_texto(
            self.campo_data_inicial.value
        )

        data_final = self._valor_texto(
            self.campo_data_final.value
        )

        try:
            data_inicial = datetime.strptime(
                data_inicial,
                "%d/%m/%Y",
            ).strftime("%Y-%m-%d")

            data_final = datetime.strptime(
                data_final,
                "%d/%m/%Y",
            ).strftime("%Y-%m-%d")

        except ValueError:
            self._mostrar_mensagem(
                "Informe as datas no formato DD/MM/AAAA.",
                erro=True,
            )
            return

        status = self._status_selecionado()

        motorista_id = self._id_dropdown(
            self.dropdown_motorista.value
        )

        veiculo_id = self._id_dropdown(
            self.dropdown_veiculo.value
        )

        if data_inicial and data_final:
            resultado = self.controller.agenda_periodo(
                data_inicial=data_inicial,
                data_final=data_final,
                status=status,
                motorista_id=motorista_id,
                veiculo_id=veiculo_id,
            )

        else:
            resultado = self.controller.pesquisar(
                status=status,
                motorista_id=motorista_id,
                veiculo_id=veiculo_id,
            )

        if resultado.falhou:
            self.tabela.rows = []

            self._mostrar_mensagem(
                resultado.mensagem,
                erro=True,
            )
            return

        registros = resultado.dados or []

        self.tabela.rows = [
            self._criar_linha_tabela(registro)
            for registro in registros
        ]

        self._mostrar_mensagem(
            resultado.mensagem,
        )

    def _carregar_motoristas(self) -> None:
        """Carrega os motoristas ativos no dropdown."""

        try:
            motoristas = self.motorista_controller.listar_ativos()

            self.dropdown_motorista.options = [
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                )
            ]

            for motorista in motoristas:
                self.dropdown_motorista.options.append(
                    ft.DropdownOption(
                        key=str(motorista.id),
                        text=motorista.nome,
                    )
                )

            self.dropdown_motorista.value = "TODOS"

        except Exception as erro:
            self._mostrar_mensagem(
                f"Erro ao carregar motoristas: {erro}",
                erro=True,
            )

    def _carregar_veiculos(self) -> None:
        """Carrega os veículos disponíveis."""

        try:
            veiculos = self.veiculo_controller.listar_disponiveis()

            self.dropdown_veiculo.options = [
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                )
            ]

            for veiculo in veiculos:
                descricao = (
                    f"{veiculo.placa} • "
                    f"{veiculo.marca} {veiculo.modelo}"
                )

                self.dropdown_veiculo.options.append(
                    ft.DropdownOption(
                        key=str(veiculo.id),
                        text=descricao,
                    )
                )

            self.dropdown_veiculo.value = "TODOS"

        except Exception as erro:
            self._mostrar_mensagem(
                f"Erro ao carregar veículos: {erro}",
                erro=True,
            )

    def _carregar_solicitacoes_pendentes(self) -> None:
        """Carrega no diálogo somente as solicitações em ANÁLISE."""

        try:
            solicitacoes = (
                self.solicitacao_controller
                .listar_com_estabelecimento()
            )

            opcoes: list[ft.DropdownOption] = []

            for solicitacao in solicitacoes:
                status = str(
                    solicitacao.get("status") or ""
                ).strip().upper()

                if status != StatusColeta.EM_ANALISE:
                    continue

                solicitacao_id = solicitacao.get("id")

                if solicitacao_id is None:
                    continue

                codigo = str(
                    solicitacao.get("codigo") or "-"
                )

                solicitante = str(
                    solicitacao.get("solicitante")
                    or "Solicitante não identificado"
                )

                forma = str(
                    solicitacao.get("forma_acondicionamento") or ""
                ).strip().upper()

                quantidade = int(
                    solicitacao.get("quantidade_prevista", 0)
                    or 0
                )

                if forma == "BAG":
                    unidade = (
                        "Bag"
                        if quantidade == 1
                        else "Bags"
                    )

                    quantidade_texto = (
                        f"{quantidade} "
                        f"{unidade} (1 m³)"
                    )
                else:
                    unidade = (
                        "Saca"
                        if quantidade == 1
                        else "Sacas"
                    )

                    quantidade_texto = (
                        f"{quantidade} {unidade}"
                    )

                descricao = (
                    f"{codigo} • "
                    f"{solicitante} • "
                    f"{quantidade_texto}"
                )
                opcoes.append(
                    ft.DropdownOption(
                        key=str(solicitacao_id),
                        text=descricao,
                    )
                )

            self.dropdown_solicitacao_dialog.options = opcoes
            self.dropdown_solicitacao_dialog.value = None

            if not opcoes:
                self.texto_mensagem_dialog.value = (
                   "Não existem solicitações em análise "
                   "disponíveis para agendamento."
                )
                self.texto_mensagem_dialog.color = ft.Colors.ORANGE
                self.texto_mensagem_dialog.visible = True
            else:
                self.texto_mensagem_dialog.value = ""
                self.texto_mensagem_dialog.visible = False

        except Exception as erro:
            self.dropdown_solicitacao_dialog.options = []
            self.dropdown_solicitacao_dialog.value = None

            self.texto_mensagem_dialog.value = (
                f"Erro ao carregar solicitações: {erro}"
            )
            self.texto_mensagem_dialog.color = ft.Colors.RED
            self.texto_mensagem_dialog.visible = True

    def _carregar_motoristas_dialog(self) -> None:
        """
        Carrega os motoristas ativos no diálogo.
        """

        try:

            motoristas = (
                self.motorista_controller
                .listar_ativos()
            )

            opcoes: list[ft.DropdownOption] = []

            for motorista in motoristas:
                opcoes.append(
                    ft.DropdownOption(
                        key=str(motorista.id),
                        text=motorista.nome,
                    )
                )

            self.dropdown_motorista_dialog.options = opcoes

            self.dropdown_motorista_dialog.value = None

        except Exception as erro:

            self.dropdown_motorista_dialog.options = []

            self.texto_mensagem_dialog.value = (
                f"Erro ao carregar motoristas: {erro}"
            )

            self.texto_mensagem_dialog.color = ft.Colors.RED

            self.texto_mensagem_dialog.visible = True

    def _carregar_veiculos_dialog(
            self,
            motorista_id: int | None = None,
    ) -> None:
        """
        Carrega no diálogo somente os veículos vinculados
        ao motorista selecionado.
        """

        try:
            self.dropdown_veiculo_dialog.options = []
            self.dropdown_veiculo_dialog.value = None

            if motorista_id is None:
                self.dropdown_veiculo_dialog.hint_text = (
                    "Selecione primeiro um motorista"
                )
                return

            veiculos = (
                self.veiculo_controller
                .listar_por_motorista(motorista_id)
            )

            opcoes: list[ft.DropdownOption] = []

            for veiculo in veiculos:
                if not veiculo.ativo:
                    continue

                descricao = (
                    f"{veiculo.placa} • "
                    f"{veiculo.marca} "
                    f"{veiculo.modelo}"
                )

                opcoes.append(
                    ft.DropdownOption(
                        key=str(veiculo.id),
                        text=descricao,
                    )
                )

            self.dropdown_veiculo_dialog.options = opcoes

            if opcoes:
                self.dropdown_veiculo_dialog.hint_text = (
                    "Selecione um veículo"
                )
            else:
                self.dropdown_veiculo_dialog.hint_text = (
                    "Nenhum veículo vinculado ao motorista"
                )

        except Exception as erro:
            self.dropdown_veiculo_dialog.options = []
            self.dropdown_veiculo_dialog.value = None

            self.texto_mensagem_dialog.value = (
                f"Erro ao carregar veículos: {erro}"
            )
            self.texto_mensagem_dialog.color = ft.Colors.RED
            self.texto_mensagem_dialog.visible = True

    def _criar_linha_tabela(
        self,
        registro: dict,
    ) -> ft.DataRow:
        """Converte um registro em uma linha da tabela."""

        solicitacao_id = int(
            registro["id"]
        )

        codigo = str(
            registro.get("codigo") or "-"
        )

        solicitante = str(
            registro.get("solicitante")
            or registro.get("estabelecimento_nome")
            or "Solicitante não identificado"
        )

        forma = str(
            registro.get("forma_acondicionamento") or "SACA"
        ).strip().upper()

        quantidade = int(
            registro.get("quantidade_prevista") or 0
        )

        sacas = quantidade if forma == "SACA" else 0
        bags = quantidade if forma == "BAG" else 0

        motorista = str(
            registro.get("motorista_nome") or "Não definido"
        )

        placa = str(
            registro.get("veiculo_placa") or ""
        )

        marca = str(
            registro.get("veiculo_marca") or ""
        )

        modelo = str(
            registro.get("veiculo_modelo") or ""
        )

        descricao = " ".join(
            item
            for item in (
                marca,
                modelo,
            )
            if item
        )

        if placa and descricao:
            veiculo = f"{placa} • {descricao}"
        elif placa:
            veiculo = placa
        elif descricao:
            veiculo = descricao
        else:
            veiculo = "Não definido"

        data_hora = self._formatar_data_hora(
            registro.get("data_hora_agendada")
        )

        status = str(
            registro.get("status") or "-"
        )

        return ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(codigo),
                ),
                ft.DataCell(
                    ft.Text(solicitante),
                ),
                ft.DataCell(
                    ft.Text(str(sacas)),
                ),
                ft.DataCell(
                    ft.Text(str(bags)),
                ),
                ft.DataCell(
                    ft.Text(motorista),
                ),
                ft.DataCell(
                    ft.Text(veiculo),
                ),
                ft.DataCell(
                    ft.Text(data_hora),
                ),
                ft.DataCell(
                    self._criar_badge_status(status),
                ),
                ft.DataCell(
                    self._criar_menu_acoes(
                        solicitacao_id=solicitacao_id,
                        status=status,
                        data_hora_chegada=registro.get(
                            "data_hora_chegada"
                        ),
                    ),
                ),
            ],
        )

    def _criar_badge_status(
        self,
        status: str,
    ) -> ft.Control:
        """Cria o marcador visual de status."""

        texto = StatusColeta.descricao(
            status
        )

        return ft.Container(
            content=ft.Text(
                texto,
                size=12,
                weight=ft.FontWeight.BOLD,
            ),
            padding=ft.Padding(
                left=10,
                top=5,
                right=10,
                bottom=5,
            ),
            border=ft.Border.all(
                width=1,
            ),
            border_radius=20,
        )

    def _criar_menu_acoes(
            self,
            *,
            solicitacao_id: int,
            status: str,
            data_hora_chegada: str | None = None,
    ) -> ft.PopupMenuButton:
        """Cria o menu de ações permitido para cada status."""

        itens: list[ft.PopupMenuItem] = [
            ft.PopupMenuItem(
                content="Visualizar",
                on_click=lambda _:
                self._visualizar(solicitacao_id),
            ),
        ]

        if status == StatusColeta.EM_ANALISE:
            itens.extend([
                ft.PopupMenuItem(
                    content="Agendar",
                    on_click=lambda _:
                    self._agendar(solicitacao_id),
                ),
                ft.PopupMenuItem(
                    content="Recusar",
                    on_click=lambda _:
                    self._recusar(solicitacao_id),
                ),
            ])

        elif status == StatusColeta.AGENDADA:
            itens.extend([
                ft.PopupMenuItem(
                    content="Reagendar",
                    on_click=lambda _:
                    self._reagendar(solicitacao_id),
                ),
                ft.PopupMenuItem(
                    content="Iniciar deslocamento",
                    on_click=lambda _:
                    self._iniciar_deslocamento(solicitacao_id),
                ),
                ft.PopupMenuItem(
                    content="Cancelar",
                    on_click=lambda _:
                    self._cancelar(solicitacao_id),
                ),
            ])

        elif status == StatusColeta.EM_DESLOCAMENTO:
            itens.append(
                ft.PopupMenuItem(
                    content="Registrar chegada",
                    on_click=lambda _:
                    self._registrar_chegada(
                        solicitacao_id
                    ),
                )
            )

        elif status == StatusColeta.EM_COLETA:
            itens.append(
                ft.PopupMenuItem(
                    content="Concluir coleta",
                    on_click=lambda _:
                    self._concluir(
                        solicitacao_id
                    ),
                )
            )

        return ft.PopupMenuButton(
            icon=ft.Icons.MORE_VERT,
            items=itens,
        )

    # ==========================================================
    # EVENTOS
    # ==========================================================

    def _abrir_seletor_data_inicial(
            self,
            _evento: ft.Event,
    ) -> None:
        """Abre o calendário para selecionar a data inicial."""

        hoje = date.today()

        seletor = ft.DatePicker(
            first_date=date(2020, 1, 1),
            last_date=date(
                hoje.year + 2,
                12,
                31,
            ),
            on_change=self._ao_selecionar_data_inicial,
        )

        self.page.show_dialog(seletor)

    def _ao_selecionar_data_inicial(
            self,
            evento: ft.Event,
    ) -> None:
        """Atualiza o campo de data inicial."""

        valor = evento.control.value

        if valor is None:
            return

        self.campo_data_inicial.value = (
            valor.strftime("%d/%m/%Y")
        )

        self._atualizar_pagina()

    def _abrir_seletor_data_final(
            self,
            _evento: ft.Event,
    ) -> None:
        """Abre o calendário para selecionar a data final."""

        hoje = date.today()

        seletor = ft.DatePicker(
            first_date=date(2020, 1, 1),
            last_date=date(
                hoje.year + 2,
                12,
                31,
            ),
            on_change=self._ao_selecionar_data_final,
        )

        self.page.show_dialog(seletor)

    def _ao_selecionar_data_final(
            self,
            evento: ft.Event,
    ) -> None:
        """Atualiza o campo de data final."""

        valor = evento.control.value

        if valor is None:
            return

        self.campo_data_final.value = (
            valor.strftime("%d/%m/%Y")
        )

        self._atualizar_pagina()

    def _pesquisar(
        self,
        _evento: ft.Event,
    ) -> None:
        """Executa a pesquisa usando os filtros atuais."""

        self._definir_carregamento(True)

        try:
            self._carregar_tabela()

        finally:
            self._definir_carregamento(False)

        self._atualizar_pagina()

    def _limpar_filtros(
            self,
            _evento: ft.Event,
    ) -> None:
        """Restaura os filtros iniciais."""

        hoje = date.today().strftime("%d/%m/%Y")

        self.campo_data_inicial.value = hoje
        self.campo_data_final.value = hoje
        self.dropdown_status.value = "TODOS"
        self.dropdown_motorista.value = "TODOS"
        self.dropdown_veiculo.value = "TODOS"

        self.carregar_dados()

        self._atualizar_destaque_cards(None)

    def _atualizar(
        self,
        _evento: ft.Event,
    ) -> None:
        """Atualiza os dados da tela."""

        self.carregar_dados()
        self._atualizar_pagina()

    def _nova_coleta(
            self,
            _evento: ft.Event,
    ) -> None:
        """
        Abre o diálogo de agendamento.
        """

        self._abrir_dialog_agendamento()

    def _abrir_dialog_agendamento(
            self,
            solicitacao_id: int | None = None,
    ) -> None:
        """
        Abre o diálogo de agendamento.
        """

        self._carregar_solicitacoes_pendentes()

        self._carregar_motoristas_dialog()

        # self._carregar_veiculos_dialog()

        if solicitacao_id is not None:
            self.dropdown_solicitacao_dialog.value = (
                str(solicitacao_id)
            )
        else:
            self.dropdown_solicitacao_dialog.value = None

        self.campo_data_agendamento.value = (
            date.today().strftime("%d/%m/%Y")
        )

        self.campo_hora_agendamento.value = "08:00"

        self.dropdown_motorista_dialog.value = None

        self.dropdown_veiculo_dialog.value = None

        self.texto_mensagem_dialog.value = ""

        self.texto_mensagem_dialog.visible = False

        self.page.show_dialog(
            self.dialog_agendamento
        )

    def _visualizar(
            self,
            solicitacao_id: int,
    ) -> None:
        resultado = self.controller.obter_por_id(
            solicitacao_id
        )

        if resultado.falhou:
            self._mostrar_mensagem(
                resultado.mensagem,
                erro=True,
            )
        else:
            coleta = resultado.dados

            if self.on_visualizar_coleta is not None:
                self.on_visualizar_coleta(coleta)
                return

            self._mostrar_mensagem(
                "Não foi possível abrir os detalhes da coleta.",
                erro=True,
            )

        self._atualizar_pagina()

    def _agendar(
            self,
            solicitacao_id: int,
    ) -> None:
        """Abre o diálogo de agendamento para a solicitação selecionada."""

        self.modo_dialog_agendamento = "AGENDAR"
        self.solicitacao_reagendamento_id = None

        self._carregar_solicitacoes_pendentes()
        self._carregar_motoristas_dialog()

        self.dropdown_solicitacao_dialog.disabled = False

        self.dropdown_solicitacao_dialog.value = str(
            solicitacao_id
        )

        self.dropdown_motorista_dialog.value = None
        self.dropdown_veiculo_dialog.value = None

        self.texto_instrucao_dialog.value = (
            "Selecione uma solicitação em análise e informe "
            "os dados do agendamento."
        )

        self.texto_mensagem_dialog.value = ""
        self.texto_mensagem_dialog.visible = False

        self.indicador_dialog.visible = False
        self.botao_confirmar_agendamento.disabled = False

        self.page.show_dialog(
            self.dialog_agendamento
        )

    def _reagendar(
            self,
            solicitacao_id: int,
    ) -> None:
        """Abre o diálogo para reagendar uma coleta."""

        resultado = self.controller.obter_por_id(
            solicitacao_id
        )

        if resultado.falhou:
            self._mostrar_mensagem(
                resultado.mensagem,
                erro=True,
            )
            self._atualizar_pagina()
            return

        coleta = resultado.dados

        self.modo_dialog_agendamento = "REAGENDAR"
        self.solicitacao_reagendamento_id = solicitacao_id

        # Carrega os dados auxiliares do diálogo
        self._carregar_motoristas_dialog()

        # Preenche a solicitação atual
        self.dropdown_solicitacao_dialog.options = [
            ft.DropdownOption(
                key=str(solicitacao_id),
                text=(
                    f"{coleta['codigo']} • "
                    f"{coleta['estabelecimento_nome']}"
                ),
            )
        ]

        self.dropdown_solicitacao_dialog.value = str(
            solicitacao_id
        )

        self.dropdown_solicitacao_dialog.disabled = True

        # Preenche motorista atual
        motorista_id = coleta.get("motorista_id")

        if motorista_id is not None:
            self.dropdown_motorista_dialog.value = str(
                motorista_id
            )

            self._carregar_veiculos_dialog(
                motorista_id
            )

        # Preenche veículo atual
        veiculo_id = coleta.get("veiculo_id")

        if veiculo_id is not None:
            self.dropdown_veiculo_dialog.value = str(
                veiculo_id
            )

        # Preenche data e hora atuais
        data_hora = coleta.get("data_hora_agendada")

        if data_hora:
            try:
                data_agendada = datetime.fromisoformat(
                    data_hora
                )

                self.campo_data_agendamento.value = (
                    data_agendada.strftime("%d/%m/%Y")
                )

                self.campo_hora_agendamento.value = (
                    data_agendada.strftime("%H:%M")
                )

            except ValueError:
                pass

        # Ajusta o diálogo para reagendamento
        self.texto_instrucao_dialog.value = (
            "Altere os dados necessários para reagendar a coleta."
        )

        self.dialog_agendamento.title = ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.EVENT_REPEAT,
                    size=24,
                ),
                ft.Text(
                    "Reagendar coleta",
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=10,
        )

        self.botao_confirmar_agendamento.content = ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.EVENT_REPEAT,
                    size=18,
                ),
                ft.Text("Reagendar"),
            ],
            spacing=8,
            tight=True,
        )

        self.texto_mensagem_dialog.value = ""
        self.texto_mensagem_dialog.visible = False

        self.page.show_dialog(
            self.dialog_agendamento
        )

    def _iniciar_deslocamento(
            self,
            solicitacao_id: int,
    ) -> None:
        """Inicia o deslocamento para uma coleta agendada."""

        resultado = self.controller.iniciar_deslocamento(
            solicitacao_id
        )

        self._processar_resultado_operacao(
            resultado
        )

    def _registrar_chegada(
            self,
            solicitacao_id: int,
    ) -> None:
        """Registra a chegada da equipe ao local da coleta."""

        resultado = self.controller.registrar_chegada(
            solicitacao_id
        )

        self._processar_resultado_operacao(
            resultado
        )

    def _concluir(
            self,
            solicitacao_id: int,
    ) -> None:
        """Abre o diálogo para concluir uma coleta em andamento."""

        resultado = self.controller.obter_por_id(
            solicitacao_id
        )

        if resultado.falhou:
            self._mostrar_mensagem(
                resultado.mensagem,
                erro=True,
            )
            self._atualizar_pagina()
            return

        coleta = resultado.dados

        self.solicitacao_conclusao_id = solicitacao_id

        codigo = str(
            coleta.get("codigo") or "-"
        )

        solicitante = str(
            coleta.get("estabelecimento_nome")
            or "Solicitante não identificado"
        )

        forma = str(
            coleta.get("forma_acondicionamento")
            or "SACA"
        ).strip().upper()

        self.forma_acondicionamento_conclusao = forma

        quantidade_prevista = int(
            coleta.get("quantidade_prevista") or 0
        )

        peso_previsto = float(
            coleta.get("peso_estimado_kg") or 0
        )

        if forma == "BAG":
            unidade = (
                "Bag"
                if quantidade_prevista == 1
                else "Bags"
            )
        else:
            unidade = (
                "Saca"
                if quantidade_prevista == 1
                else "Sacas"
            )

        self.texto_coleta_conclusao.value = (
            f"{codigo} • {solicitante}"
        )

        self.texto_previsto_conclusao.value = (
            f"Previsto: "
            f"{quantidade_prevista} {unidade} • "
            f"{peso_previsto:,.0f} kg"
            .replace(",", ".")
        )

        # Sugere os valores previstos, mas permite alteração.
        self.campo_quantidade_coletada.value = str(
            quantidade_prevista
        )

        self.campo_peso_coletado.value = (
            f"{peso_previsto:.0f}"
            if peso_previsto > 0
            else ""
        )

        self.campo_observacao_operacional.value = ""

        self.texto_mensagem_conclusao.value = ""
        self.texto_mensagem_conclusao.visible = False

        self.page.show_dialog(
            self.dialog_conclusao
        )

    def _atualizar_peso_coletado(
            self,
            _evento: ft.Event,
    ) -> None:
        """Atualiza o peso coletado conforme a quantidade informada."""

        valor_quantidade = str(
            self.campo_quantidade_coletada.value or ""
        ).strip()

        if not valor_quantidade:
            self.campo_peso_coletado.value = ""
            self._atualizar_pagina()
            return

        try:
            quantidade = int(valor_quantidade)
        except ValueError:
            self.campo_peso_coletado.value = ""
            self._atualizar_pagina()
            return

        if quantidade < 0:
            self.campo_peso_coletado.value = ""
            self._atualizar_pagina()
            return

        forma = str(
            getattr(
                self,
                "forma_acondicionamento_conclusao",
                "SACA",
            )
        ).strip().upper()

        if forma == "BAG":
            peso_por_unidade = 1000
        else:
            peso_por_unidade = 50

        peso_total = quantidade * peso_por_unidade

        self.campo_peso_coletado.value = str(
            peso_total
        )

        self._atualizar_pagina()

    def _cancelar(
            self,
            solicitacao_id: int,
    ) -> None:
        """Abre o diálogo para cancelar uma coleta."""

        resultado = self.controller.obter_por_id(
            solicitacao_id
        )

        if resultado.falhou:
            self._mostrar_mensagem(
                resultado.mensagem,
                erro=True,
            )
            self._atualizar_pagina()
            return

        coleta = resultado.dados

        self.solicitacao_cancelamento_id = solicitacao_id

        codigo = str(
            coleta.get("codigo") or "-"
        )

        solicitante = str(
            coleta.get("estabelecimento_nome")
            or "Solicitante não identificado"
        )

        self.texto_coleta_cancelamento.value = (
            f"{codigo} • {solicitante}"
        )

        self.campo_motivo_cancelamento.value = ""

        self.texto_mensagem_cancelamento.value = ""
        self.texto_mensagem_cancelamento.visible = False

        self.page.show_dialog(
            self.dialog_cancelamento
        )

    def _recusar(
            self,
            solicitacao_id: int,
    ) -> None:
        """Abre o diálogo para recusar uma solicitação."""

        resultado = self.controller.obter_por_id(
            solicitacao_id
        )

        if resultado.falhou:
            self._mostrar_mensagem(
                resultado.mensagem,
                erro=True,
            )
            self._atualizar_pagina()
            return

        coleta = resultado.dados

        self.solicitacao_recusa_id = solicitacao_id

        codigo = str(
            coleta.get("codigo") or "-"
        )

        solicitante = str(
            coleta.get("estabelecimento_nome")
            or "Solicitante não identificado"
        )

        self.texto_coleta_recusa.value = (
            f"{codigo} • {solicitante}"
        )

        self.campo_motivo_recusa.value = ""

        self.texto_mensagem_recusa.value = ""
        self.texto_mensagem_recusa.visible = False

        self.page.show_dialog(
            self.dialog_recusa
        )

    def _confirmar_recusa(
            self,
            _evento: ft.Event,
    ) -> None:
        """Valida e confirma a recusa da solicitação."""

        if self.solicitacao_recusa_id is None:
            self.texto_mensagem_recusa.value = (
                "Não foi possível identificar a solicitação."
            )
            self.texto_mensagem_recusa.visible = True
            self._atualizar_pagina()
            return

        motivo = str(
            self.campo_motivo_recusa.value or ""
        ).strip()

        if not motivo:
            self.texto_mensagem_recusa.value = (
                "Informe o motivo da recusa."
            )
            self.texto_mensagem_recusa.visible = True
            self._atualizar_pagina()
            return

        resultado = self.controller.recusar_coleta(
            solicitacao_id=self.solicitacao_recusa_id,
            motivo=motivo,
        )

        if resultado.falhou:
            self.texto_mensagem_recusa.value = (
                resultado.mensagem
            )
            self.texto_mensagem_recusa.visible = True
            self._atualizar_pagina()
            return

        self.page.pop_dialog()

        self.solicitacao_recusa_id = None

        self._processar_resultado_operacao(
            resultado
        )

    def _fechar_dialog_recusa(
            self,
            _evento: ft.Event,
    ) -> None:
        """Fecha o diálogo de recusa."""

        self.page.pop_dialog()

        self.solicitacao_recusa_id = None
        self.campo_motivo_recusa.value = ""
        self.texto_mensagem_recusa.value = ""
        self.texto_mensagem_recusa.visible = False

        self._atualizar_pagina()

    def _processar_resultado_operacao(
            self,
            resultado: Any,
    ) -> None:
        """Atualiza a interface depois de uma operação."""

        if resultado.sucesso:
            self.carregar_dados()

        self._mostrar_mensagem(
            resultado.mensagem,
            erro=resultado.falhou,
        )

        self._atualizar_pagina()

    def _acao_pendente(
        self,
        nome_acao: str,
        solicitacao_id: int,
    ) -> None:
        """Informa que a ação depende do próximo formulário."""

        self._mostrar_mensagem(
            f"{nome_acao} coleta {solicitacao_id}: "
            "formulário será implementado na próxima etapa."
        )

        self._atualizar_pagina()

    def _ao_selecionar_motorista_dialog(
            self,
            _evento: ft.Event,
    ) -> None:
        """
        Atualiza os veículos conforme o motorista selecionado.
        """

        motorista_id = self._id_dropdown(
            self.dropdown_motorista_dialog.value
        )

        self._carregar_veiculos_dialog(
            motorista_id=motorista_id
        )

        self._atualizar_pagina()

    # ==========================================================
    # MÉTODOS VALIDAÇÕES
    # ==========================================================

    def _validar_dialog_agendamento(self) -> bool:
        """
        Valida os campos do diálogo de agendamento.
        """

        self.texto_mensagem_dialog.visible = False

        if not self.dropdown_solicitacao_dialog.value:
            self.texto_mensagem_dialog.value = (
                "Selecione uma solicitação."
            )

            self.texto_mensagem_dialog.color = ft.Colors.RED

            self.texto_mensagem_dialog.visible = True

            self._atualizar_pagina()

            return False

        if not self.campo_data_agendamento.value.strip():
            self.texto_mensagem_dialog.value = (
                "Informe a data."
            )

            self.texto_mensagem_dialog.color = ft.Colors.RED

            self.texto_mensagem_dialog.visible = True

            self._atualizar_pagina()

            return False

        if not self.campo_hora_agendamento.value.strip():
            self.texto_mensagem_dialog.value = (
                "Informe a hora."
            )

            self.texto_mensagem_dialog.color = ft.Colors.RED

            self.texto_mensagem_dialog.visible = True

            self._atualizar_pagina()

            return False

        if not self.dropdown_motorista_dialog.value:
            self.texto_mensagem_dialog.value = (
                "Selecione um motorista."
            )

            self.texto_mensagem_dialog.color = ft.Colors.RED

            self.texto_mensagem_dialog.visible = True

            self._atualizar_pagina()

            return False

        if not self.dropdown_veiculo_dialog.value:
            self.texto_mensagem_dialog.value = (
                "Selecione um veículo."
            )

            self.texto_mensagem_dialog.color = ft.Colors.RED

            self.texto_mensagem_dialog.visible = True

            self._atualizar_pagina()

            return False

        return True

    # ==========================================================
    # MÉTODOS AUXILIARES
    # ==========================================================

    def _definir_carregamento(
        self,
        carregando: bool,
    ) -> None:
        self.indicador_carregamento.visible = carregando

    def _mostrar_mensagem(
        self,
        mensagem: str,
        *,
        erro: bool = False,
    ) -> None:
        self.texto_mensagem.value = mensagem

        self.texto_mensagem.color = (
            ft.Colors.RED
            if erro
            else ft.Colors.GREEN
        )

    def _status_selecionado(self) -> str | None:
        status = self._valor_texto(
            self.dropdown_status.value
        )

        if status in {
            "",
            "TODOS",
        }:
            return None

        return status

    @staticmethod
    def _id_dropdown(
        valor: Any,
    ) -> int | None:
        if valor in {
            None,
            "",
            "TODOS",
        }:
            return None

        try:
            identificador = int(valor)

        except (
            TypeError,
            ValueError,
        ):
            return None

        return identificador if identificador > 0 else None

    @staticmethod
    def _valor_texto(
        valor: Any,
    ) -> str:
        if valor is None:
            return ""

        return str(valor).strip()

    @staticmethod
    def _formatar_data_hora(
        valor: Any,
    ) -> str:
        if not valor:
            return "Não agendada"

        texto = str(valor).strip()

        try:
            data_hora = datetime.strptime(
                texto,
                "%Y-%m-%d %H:%M:%S",
            )

        except ValueError:
            return texto

        return data_hora.strftime(
            "%d/%m/%Y %H:%M"
        )

    def _atualizar_pagina(self) -> None:
        try:
            self.page.update()

        except RuntimeError:
            # Pode ocorrer quando build() é executado antes
            # de o controle ser anexado à página.
            pass

    def _obter_solicitacao_id(self) -> int:
        """
        Retorna o ID da solicitação selecionada.
        """

        return int(
            self.dropdown_solicitacao_dialog.value
        )

    def _obter_motorista_id(self) -> int:
        """
        Retorna o ID do motorista selecionado.
        """

        return int(
            self.dropdown_motorista_dialog.value
        )

    def _obter_veiculo_id(self) -> int:
        """
        Retorna o ID do veículo selecionado.
        """

        return int(
            self.dropdown_veiculo_dialog.value
        )

    def _obter_data_hora_agendamento(self) -> str:
        """
        Converte a data e hora informadas no diálogo
        para o formato utilizado pelo banco.
        """

        data = self.campo_data_agendamento.value.strip()
        hora = self.campo_hora_agendamento.value.strip()

        data_hora = datetime.strptime(
            f"{data} {hora}",
            "%d/%m/%Y %H:%M"
        )

        return data_hora.strftime(
            "%Y-%m-%d %H:%M:%S"
        )