from __future__ import annotations

from datetime import date, datetime
from typing import Any

import flet as ft

from controllers.coletas_agendadas_controller import (
    ColetasAgendadasController,
)
from controllers.motorista_controller import MotoristaController
from controllers.veiculo_controller import VeiculoController
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)


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

    _STATUS = (
        "PENDENTE",
        "AGENDADA",
        "EM_COLETA",
        "CONCLUIDA",
        "CANCELADA",
    )

    def __init__(
        self,
        page: ft.Page,
        controller: ColetasAgendadasController | None = None,
    ) -> None:
        self.page = page

        self.controller = (
            controller
            if controller is not None
            else ColetasAgendadasController()
        )

        self.motorista_controller = MotoristaController()

        self.veiculo_controller = VeiculoController()

        self.solicitacao_controller = (
            SolicitacaoColetaController()
        )

        self._construir_controles()
        self._construir_dialog_agendamento()

    # ==========================================================
    # CONSTRUÇÃO
    # ==========================================================

    def _construir_controles(self) -> None:
        """Cria os controles utilizados pela tela."""

        hoje = date.today().isoformat()

        self.campo_data_inicial = ft.TextField(
            label="Data inicial",
            hint_text="AAAA-MM-DD",
            value=hoje,
            width=170,
            dense=True,
        )

        self.campo_data_final = ft.TextField(
            label="Data final",
            hint_text="AAAA-MM-DD",
            value=hoje,
            width=170,
            dense=True,
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
                    key="PENDENTE",
                    text="Pendente",
                ),
                ft.DropdownOption(
                    key="AGENDADA",
                    text="Agendada",
                ),
                ft.DropdownOption(
                    key="EM_COLETA",
                    text="Em coleta",
                ),
                ft.DropdownOption(
                    key="CONCLUIDA",
                    text="Concluída",
                ),
                ft.DropdownOption(
                    key="CANCELADA",
                    text="Cancelada",
                ),
            ],
        )

        self.dropdown_motorista = ft.Dropdown(
            label="Motorista",
            width=220,
            dense=True,
            value="TODOS",
            options=[
                ft.DropdownOption(
                    key="TODOS",
                    text="Todos",
                ),
            ],
        )

        self.dropdown_veiculo = ft.Dropdown(
            label="Veículo",
            width=220,
            dense=True,
            value="TODOS",
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
        self.texto_total_em_coleta = self._criar_texto_total()
        self.texto_total_concluidas = self._criar_texto_total()
        self.texto_total_canceladas = self._criar_texto_total()

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text("Código"),
                ),
                ft.DataColumn(
                    ft.Text("Estabelecimento"),
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

    def _construir_dialog_agendamento(self) -> None:
        """
        Cria os controles e o AlertDialog utilizado para agendar
        ou reagendar uma solicitação de coleta.
        """

        amanha = date.today().fromordinal(
            date.today().toordinal() + 1
        )

        self.dropdown_solicitacao_dialog = ft.Dropdown(
            label="Solicitação pendente",
            hint_text="Selecione uma solicitação",
            width=520,
            dense=True,
            options=[],
        )

        self.campo_data_agendamento = ft.TextField(
            label="Data",
            hint_text="DD/MM/AAAA",
            value=amanha.strftime("%d/%m/%Y"),
            width=250,
            dense=True,
        )

        self.campo_hora_agendamento = ft.TextField(
            label="Hora",
            hint_text="HH:MM",
            value="08:00",
            width=250,
            dense=True,
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

        conteudo_dialog = ft.Column(
            controls=[
                ft.Text(
                    "Selecione uma solicitação pendente e informe "
                    "os dados do agendamento.",
                    size=13,
                ),
                self.dropdown_solicitacao_dialog,
                ft.Row(
                    controls=[
                        self.campo_data_agendamento,
                        self.campo_hora_agendamento,
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

        titulo = ft.Column(
            controls=[
                ft.Text(
                    "Coletas Agendadas",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Gerenciamento da agenda operacional de coletas.",
                    size=14,
                ),
            ],
            spacing=3,
        )

        botao_nova_coleta = ft.FilledButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.ADD,
                        size=18,
                    ),
                    ft.Text("Agendar Coleta"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._nova_coleta,
        )

        return ft.Row(
            controls=[
                titulo,
                botao_nova_coleta,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _criar_filtros(self) -> ft.Control:
        """Cria a barra de filtros."""

        botao_pesquisar = ft.FilledButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.SEARCH,
                        size=18,
                    ),
                    ft.Text("Pesquisar"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._pesquisar,
        )

        botao_limpar = ft.OutlinedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CLEAR,
                        size=18,
                    ),
                    ft.Text("Limpar"),
                ],
                spacing=8,
                tight=True,
            ),
            on_click=self._limpar_filtros,
        )

        linha_filtros = ft.Row(
            controls=[
                self.campo_data_inicial,
                self.campo_data_final,
                self.dropdown_status,
                self.dropdown_motorista,
                self.dropdown_veiculo,
                botao_pesquisar,
                botao_limpar,
                self.indicador_carregamento,
            ],
            spacing=12,
            run_spacing=12,
            wrap=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            content=linha_filtros,
            padding=16,
            border=ft.Border.all(
                width=1,
            ),
            border_radius=12,
        )

    def _criar_dashboard(self) -> ft.Control:
        """Cria os cards com os indicadores da agenda."""

        cards = [
            self._criar_card_indicador(
                titulo="Pendentes",
                texto_total=self.texto_total_pendentes,
                icone=ft.Icons.PENDING_ACTIONS,
            ),
            self._criar_card_indicador(
                titulo="Agendadas",
                texto_total=self.texto_total_agendadas,
                icone=ft.Icons.EVENT_AVAILABLE,
            ),
            self._criar_card_indicador(
                titulo="Em coleta",
                texto_total=self.texto_total_em_coleta,
                icone=ft.Icons.LOCAL_SHIPPING,
            ),
            self._criar_card_indicador(
                titulo="Concluídas",
                texto_total=self.texto_total_concluidas,
                icone=ft.Icons.CHECK_CIRCLE,
            ),
            self._criar_card_indicador(
                titulo="Canceladas",
                texto_total=self.texto_total_canceladas,
                icone=ft.Icons.CANCEL,
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
    ) -> ft.Control:
        """Cria um card de indicador."""

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            icone,
                            size=28,
                        ),
                        width=48,
                        height=48,
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
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=190,
            padding=16,
            border=ft.Border.all(
                width=1,
            ),
            border_radius=12,
        )

    def _criar_area_mensagem(self) -> ft.Control:
        """Cria a área de mensagens da tela."""

        return ft.Container(
            content=self.texto_mensagem,
            visible=True,
        )

    def _criar_tabela(self) -> ft.Control:
        """Cria a área da tabela."""

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
        )

    @staticmethod
    def _criar_texto_total() -> ft.Text:
        """Cria o texto numérico de um indicador."""

        return ft.Text(
            value="0",
            size=24,
            weight=ft.FontWeight.BOLD,
        )

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
            totais.get("PENDENTE", 0)
        )

        self.texto_total_agendadas.value = str(
            totais.get("AGENDADA", 0)
        )

        self.texto_total_em_coleta.value = str(
            totais.get("EM_COLETA", 0)
        )

        self.texto_total_concluidas.value = str(
            totais.get("CONCLUIDA", 0)
        )

        self.texto_total_canceladas.value = str(
            totais.get("CANCELADA", 0)
        )

    def _carregar_tabela(self) -> None:
        """Carrega a tabela aplicando os filtros atuais."""

        data_inicial = self._valor_texto(
            self.campo_data_inicial.value
        )

        data_final = self._valor_texto(
            self.campo_data_final.value
        )

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
        """
        Carrega no diálogo somente as solicitações
        que possuem status PENDENTE.
        """

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

                if status != "PENDENTE":
                    continue

                solicitacao_id = solicitacao.get("id")

                if solicitacao_id is None:
                    continue

                codigo = str(
                    solicitacao.get("codigo") or "-"
                )

                estabelecimento = str(
                    solicitacao.get("estabelecimento")
                    or "Estabelecimento não informado"
                )

                quantidade_sacas = int(
                    solicitacao.get(
                        "quantidade_sacas_prevista",
                        0,
                    )
                    or 0
                )

                unidade = (
                    "saca"
                    if quantidade_sacas == 1
                    else "sacas"
                )

                descricao = (
                    f"{codigo} • "
                    f"{estabelecimento} • "
                    f"{quantidade_sacas} {unidade}"
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
                    "Não existem solicitações pendentes "
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

        estabelecimento = str(
            registro.get("estabelecimento_nome") or "-"
        )

        motorista = str(
            registro.get("motorista_nome") or "Não definido"
        )

        placa = str(
            registro.get("veiculo_placa") or ""
        )

        modelo = str(
            registro.get("veiculo_modelo") or ""
        )

        veiculo = " ".join(
            item
            for item in (
                placa,
                modelo,
            )
            if item
        ) or "Não definido"

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
                    ft.Text(estabelecimento),
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
                    ),
                ),
            ],
        )

    def _criar_badge_status(
        self,
        status: str,
    ) -> ft.Control:
        """Cria o marcador visual de status."""

        texto = status.replace(
            "_",
            " ",
        ).title()

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
    ) -> ft.PopupMenuButton:
        """Cria o menu de ações permitido para cada status."""

        itens: list[ft.PopupMenuItem] = [
            ft.PopupMenuItem(
                content=ft.Text("Visualizar"),
                on_click=lambda _:
                self._visualizar(solicitacao_id),
            ),
        ]

        if status == "PENDENTE":
            itens.extend([
                ft.PopupMenuItem(
                    content=ft.Text("Agendar"),
                    on_click=lambda _:
                    self._agendar(solicitacao_id),
                ),
                ft.PopupMenuItem(
                    content=ft.Text("Cancelar"),
                    on_click=lambda _:
                    self._cancelar(solicitacao_id),
                ),
            ])

        elif status == "AGENDADA":
            itens.extend([
                ft.PopupMenuItem(
                    content=ft.Text("Reagendar"),
                    on_click=lambda _:
                    self._reagendar(solicitacao_id),
                ),
                ft.PopupMenuItem(
                    content=ft.Text("Iniciar coleta"),
                    on_click=lambda _:
                    self._iniciar(solicitacao_id),
                ),
                ft.PopupMenuItem(
                    content=ft.Text("Cancelar"),
                    on_click=lambda _:
                    self._cancelar(solicitacao_id),
                ),
            ])

        elif status == "EM_COLETA":
            itens.append(
                ft.PopupMenuItem(
                    content=ft.Text("Concluir coleta"),
                    on_click=lambda _:
                    self._concluir(solicitacao_id),
                )
            )

        return ft.PopupMenuButton(
            icon=ft.Icons.MORE_VERT,
            items=itens,
        )

    # ==========================================================
    # EVENTOS
    # ==========================================================

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

        hoje = date.today().isoformat()

        self.campo_data_inicial.value = hoje
        self.campo_data_final.value = hoje
        self.dropdown_status.value = "TODOS"
        self.dropdown_motorista.value = "TODOS"
        self.dropdown_veiculo.value = "TODOS"

        self.carregar_dados()
        self._atualizar_pagina()

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

            self._mostrar_mensagem(
                f"{coleta['codigo']} — "
                f"{coleta['estabelecimento_nome']} — "
                f"{coleta['status']}"
            )

        self._atualizar_pagina()

    def _agendar(
        self,
        solicitacao_id: int,
    ) -> None:
        self._acao_pendente(
            "Agendar",
            solicitacao_id,
        )

    def _reagendar(
        self,
        solicitacao_id: int,
    ) -> None:
        self._acao_pendente(
            "Reagendar",
            solicitacao_id,
        )

    def _iniciar(
        self,
        solicitacao_id: int,
    ) -> None:
        resultado = self.controller.iniciar_coleta(
            solicitacao_id
        )

        self._processar_resultado_operacao(
            resultado
        )

    def _concluir(
        self,
        solicitacao_id: int,
    ) -> None:
        resultado = self.controller.concluir_coleta(
            solicitacao_id
        )

        self._processar_resultado_operacao(
            resultado
        )

    def _cancelar(
        self,
        solicitacao_id: int,
    ) -> None:
        resultado = self.controller.cancelar_coleta(
            solicitacao_id
        )

        self._processar_resultado_operacao(
            resultado
        )

    def _processar_resultado_operacao(
        self,
        resultado: Any,
    ) -> None:
        """Atualiza a interface depois de uma operação."""

        self._mostrar_mensagem(
            resultado.mensagem,
            erro=resultado.falhou,
        )

        if resultado.sucesso:
            self.carregar_dados()

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