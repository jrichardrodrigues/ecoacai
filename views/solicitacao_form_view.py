from collections.abc import Callable
from datetime import datetime

import flet as ft

from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from utils.messages import (
    mostrar_erro,
    mostrar_sucesso,
)
from controllers.motorista_controller import MotoristaController
from controllers.veiculo_controller import VeiculoController


class SolicitacaoFormView:
    """Formulário para criar ou editar uma solicitação de coleta."""

    def __init__(
        self,
        page: ft.Page,
        solicitacao=None,
        estabelecimento_id: int | None = None,
        on_cancelar: Callable[[], None] | None = None,
        on_salvar_sucesso: Callable[[], None] | None = None,
    ) -> None:
        self.page = page

        self.on_cancelar = on_cancelar
        self.on_salvar_sucesso = on_salvar_sucesso

        self.solicitacao = solicitacao
        self.estabelecimento_id = estabelecimento_id

        self.controller = SolicitacaoColetaController()
        self.estabelecimento_controller = (
            EstabelecimentoController()
        )

        self.estabelecimentos = (
            self.estabelecimento_controller
            .listar_estabelecimentos()
        )

        self.motorista_controller = MotoristaController()
        self.veiculo_controller = VeiculoController()

        self.motoristas = self.motorista_controller.listar_ativos()
        self.veiculos = self.veiculo_controller.listar_ativos()

        self.estabelecimento = ft.Dropdown(
            label="Solicitante",
            hint_text="Selecione o solicitante",
            expand=True,
            border_radius=10,
            options=[
                ft.dropdown.Option(
                    key=str(item.id),
                    text=item.nome,
                )
                for item in self.estabelecimentos
                if item.id is not None
            ],
        )

        self.estabelecimento.on_change = (
            self.ao_selecionar_estabelecimento
        )

        self.forma_acondicionamento = ft.Dropdown(
            label="Forma de acondicionamento",
            value="SACA",
            border_radius=10,
            expand=True,
            options=[
                ft.dropdown.Option(
                    key="SACA",
                    text="Sacas (50 kg)",
                ),
                ft.dropdown.Option(
                    key="BAG",
                    text="Bags (1 m³)",
                ),
            ],
            on_select=self.ao_selecionar_forma_acondicionamento,
        )

        self.quantidade_sacas_prevista = ft.TextField(
            label="Quantidade de sacas",
            hint_text="Ex.: 10",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=True,
            on_change=self.ao_alterar_quantidade,
        )

        self.quantidade_kg_previsto = ft.TextField(
            label="Quantidade em kg",
            hint_text="Ex.: 250",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=True,
            read_only=True,
        )

        self.seletor_data = ft.DatePicker(
            entry_mode=ft.DatePickerEntryMode.CALENDAR,
            date_picker_mode=ft.DatePickerMode.DAY,
            help_text="Selecione a data da coleta",
            cancel_text="Cancelar",
            confirm_text="Confirmar",
            on_change=self.ao_selecionar_data,
        )

        self.data_agendada = ft.TextField(
            label="Data da coleta",
            hint_text="dd/mm/aaaa",
            value="",
            read_only=True,
            border_radius=10,
            expand=True,
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                tooltip="Selecionar data",
                on_click=self.abrir_calendario,
            ),
        )

        self.motorista = ft.Dropdown(
            label="Motorista",
            hint_text="Selecione o motorista",
            border_radius=10,
            expand=True,
            options=[
                ft.dropdown.Option(
                    key=str(motorista.id),
                    text=motorista.nome,
                )
                for motorista in self.motoristas
                if motorista.id is not None
            ],
        )

        self.motorista.on_select = self.ao_selecionar_motorista

        self.veiculo = ft.Dropdown(
            label="Veículo",
            hint_text="Selecione o veículo",
            border_radius=10,
            expand=True,
            options=[
                ft.dropdown.Option(
                    key=str(veiculo.id),
                    text=f"{veiculo.marca} {veiculo.modelo} • {veiculo.placa}",
                )
                for veiculo in self.veiculos
                if veiculo.id is not None
            ],
        )

        self.observacao = ft.TextField(
            label="Observação",
            hint_text="Informações adicionais sobre a coleta",
            value="",
            multiline=True,
            min_lines=4,
            max_lines=6,
            border_radius=10,
        )

        self.resumo_estabelecimento = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Selecione um solicitante.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                spacing=5,
            ),
            padding=12,
            border_radius=10,
            bgcolor=ft.Colors.GREY_100,
            visible=True,
        )

        self.status_titulo = ft.Text(
            "Status da Solicitação",
            weight=ft.FontWeight.BOLD,
            size=15,
        )

        self.status_texto = ft.Text(
            "PENDENTE",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.AMBER_900,
        )

        self.status_container = ft.Container(
            expand=True,
            padding=12,
            border_radius=10,
            bgcolor=ft.Colors.AMBER_50,
            content=ft.Column(
                controls=[
                    self.status_titulo,
                    self.status_texto,
                ],
                spacing=5,
            ),
        )

        self.botao_operacao = ft.FilledButton(
            content="Agendar Coleta",
            icon=ft.Icons.CALENDAR_MONTH,
            visible=False,
            expand=True,
            on_click=self.executar_operacao,
        )

        self._carregar_solicitacao()

        self._atualizar_resumo_estabelecimento(
            self._obter_estabelecimento_selecionado_id(),
            atualizar_pagina=False,
        )

        self._atualizar_status_visual()
        self._atualizar_campos()

    def _carregar_solicitacao(self) -> None:
        """
        Preenche os campos do formulário.

        Quando existe uma solicitação, carrega seus dados para edição.
        Quando não existe, mantém os valores iniciais do novo cadastro.
        """

        if self.solicitacao is None:
            if self.estabelecimento_id is not None:
                self.estabelecimento.value = str(
                    self.estabelecimento_id
                )

            return

        self.estabelecimento.value = str(
            self.solicitacao.estabelecimento_id
        )

        self.quantidade_sacas_prevista.value = str(
            self.solicitacao.quantidade_sacas_prevista
        )

        self.quantidade_kg_previsto.value = str(
            self.solicitacao.quantidade_kg_previsto
        )

        data_agendada = self._converter_data(
            self.solicitacao.data_hora_agendada
        )

        if data_agendada is not None:
            self.data_agendada.value = (
                data_agendada.strftime("%d/%m/%Y")
            )
        else:
            self.data_agendada.value = (
                    self.solicitacao.data_hora_agendada or ""
            )

        self.motorista.value = (
            str(self.solicitacao.motorista_id)
            if self.solicitacao.motorista_id is not None
            else None
        )

        self.veiculo.value = (
            str(self.solicitacao.veiculo_id)
            if self.solicitacao.veiculo_id is not None
            else None
        )

        self.observacao.value = (
                self.solicitacao.observacao_cliente or ""
        )

    def _obter_estabelecimento_selecionado_id(
        self,
    ) -> int | None:
        """
        Retorna o ID do estabelecimento inicialmente selecionado.

        Na edição, utiliza o estabelecimento da solicitação.
        No cadastro, utiliza o ID recebido pelo construtor.
        """

        if self.solicitacao is not None:
            return self.solicitacao.estabelecimento_id

        return self.estabelecimento_id

    def _atualizar_resumo_estabelecimento(
        self,
        estabelecimento_id: int | None,
        atualizar_pagina: bool = True,
    ) -> None:
        """
        Atualiza o resumo do estabelecimento selecionado.

        Args:
            estabelecimento_id:
                ID do estabelecimento que deverá ser exibido.

            atualizar_pagina:
                Define se a página deve ser atualizada após
                a alteração do conteúdo.
        """

        if estabelecimento_id is None:
            self.resumo_estabelecimento.content = ft.Column(
                controls=[
                    ft.Text(
                        "Selecione um solicitante.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                spacing=5,
            )

            if atualizar_pagina:
                self.page.update()

            return

        estabelecimento = next(
            (
                item
                for item in self.estabelecimentos
                if item.id == estabelecimento_id
            ),
            None,
        )

        if estabelecimento is None:
            self.resumo_estabelecimento.content = ft.Text(
                "Solicitante não encontrado.",
                color=ft.Colors.RED,
            )

            if atualizar_pagina:
                self.page.update()

            return

        self.resumo_estabelecimento.content = ft.Column(
            controls=[
                ft.Text(
                    estabelecimento.nome,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    f"Bairro: {estabelecimento.bairro}",
                ),
                ft.Text(
                    f"Setor: {estabelecimento.setor}",
                ),
                ft.Text(
                    f"Celular: {estabelecimento.celular}",
                ),
            ],
            spacing=5,
        )

        if atualizar_pagina:
            self.page.update()

    def _atualizar_status_visual(self) -> None:
        """Atualiza o painel visual de status da solicitação."""

        # Nova solicitação ainda não possui operação disponível.
        if self.solicitacao is None:
            self.botao_operacao.visible = False

            self.status_texto.value = "🟡 PENDENTE"
            self.status_texto.color = ft.Colors.AMBER_900
            self.status_container.bgcolor = ft.Colors.AMBER_50

            return

        status = self.solicitacao.status

        self.botao_operacao.visible = True

        if status == "PENDENTE":
            self.status_texto.value = "🟡 PENDENTE"
            self.status_texto.color = ft.Colors.AMBER_900
            self.status_container.bgcolor = ft.Colors.AMBER_50

            self.botao_operacao.content = "Agendar Coleta"
            self.botao_operacao.icon = ft.Icons.CALENDAR_MONTH

        elif status == "AGENDADA":
            self.status_texto.value = "🟢 AGENDADA"
            self.status_texto.color = ft.Colors.GREEN_800
            self.status_container.bgcolor = ft.Colors.GREEN_50

            self.botao_operacao.content = "Iniciar Deslocamento"
            self.botao_operacao.icon = ft.Icons.LOCAL_SHIPPING

        elif status == "EM_DESLOCAMENTO":
            self.status_texto.value = "🚛 EM DESLOCAMENTO"
            self.status_texto.color = ft.Colors.BLUE_800
            self.status_container.bgcolor = ft.Colors.BLUE_50

            self.botao_operacao.content = "Cheguei ao Solicitante"
            self.botao_operacao.icon = ft.Icons.LOCATION_ON

        elif status == "EM_COLETA":
            self.status_texto.value = "♻️ EM COLETA"
            self.status_texto.color = ft.Colors.ORANGE_900
            self.status_container.bgcolor = ft.Colors.ORANGE_50

            self.botao_operacao.content = "Concluir Coleta"
            self.botao_operacao.icon = ft.Icons.CHECK_CIRCLE

        elif status == "CONCLUÍDA":
            self.status_texto.value = "✅ CONCLUÍDA"
            self.status_texto.color = ft.Colors.TEAL_800
            self.status_container.bgcolor = ft.Colors.TEAL_50

            self.botao_operacao.visible = False

        else:
            self.status_texto.value = status
            self.status_texto.color = ft.Colors.GREY_800
            self.status_container.bgcolor = ft.Colors.GREY_100

            self.botao_operacao.visible = False

    def _atualizar_campos(self) -> None:
        """Habilita ou bloqueia os campos conforme o status."""

        # Nova solicitação
        if self.solicitacao is None:
            for campo in (
                    self.estabelecimento,
                    self.quantidade_sacas_prevista,
                    self.quantidade_kg_previsto,
                    self.data_agendada,
                    self.motorista,
                    self.veiculo,
                    self.observacao,
            ):
                campo.disabled = False

            return

        status = self.solicitacao.status

        # Todos habilitados
        for campo in (
                self.estabelecimento,
                self.quantidade_sacas_prevista,
                self.quantidade_kg_previsto,
                self.data_agendada,
                self.motorista,
                self.veiculo,
                self.observacao,
        ):
            campo.disabled = False

        # AGENDADA
        if status == "AGENDADA":
            self.estabelecimento.disabled = True
            self.quantidade_sacas_prevista.disabled = True
            self.quantidade_kg_previsto.disabled = True

        # EM_DESLOCAMENTO
        elif status == "EM_DESLOCAMENTO":
            self.estabelecimento.disabled = True
            self.quantidade_sacas_prevista.disabled = True
            self.quantidade_kg_previsto.disabled = True
            self.data_agendada.disabled = True
            self.motorista.disabled = True
            self.veiculo.disabled = True

        # CONCLUÍDA
        elif status == "CONCLUÍDA":
            for campo in (
                    self.estabelecimento,
                    self.quantidade_sacas_prevista,
                    self.quantidade_kg_previsto,
                    self.data_agendada,
                    self.motorista,
                    self.veiculo,
                    self.observacao,
            ):
                campo.disabled = True

    @staticmethod
    def _converter_data(
            valor: str | None,
    ) -> datetime | None:
        """
        Converte uma data textual para datetime.

        Formatos aceitos:
        - dd/mm/aaaa
        - ddmmaaaa
        - aaaa-mm-dd
        """

        texto = (valor or "").strip()

        if not texto:
            return None

        formatos = (
            "%d/%m/%Y",
            "%d%m%Y",
            "%Y-%m-%d",
        )

        for formato in formatos:
            try:
                return datetime.strptime(
                    texto,
                    formato,
                )

            except ValueError:
                continue

        return None

    def ao_alterar_quantidade(
            self,
            _evento: ft.Event,
    ) -> None:
        """Calcula automaticamente o peso previsto."""

        texto = str(
            self.quantidade_sacas_prevista.value or ""
        ).strip()

        if not texto:
            self.quantidade_kg_previsto.value = "0"
            self.quantidade_kg_previsto.update()
            return

        try:
            quantidade = int(texto)

        except ValueError:
            self.quantidade_kg_previsto.value = "0"
            self.quantidade_kg_previsto.update()
            return

        forma = str(
            self.forma_acondicionamento.value or "SACA"
        ).strip().upper()

        peso_unitario = (
            1000
            if forma == "BAG"
            else 50
        )

        self.quantidade_kg_previsto.value = str(
            quantidade * peso_unitario
        )

        self.quantidade_kg_previsto.update()

    def ao_selecionar_forma_acondicionamento(
            self,
            _evento: ft.Event,
    ) -> None:
        """Atualiza os campos conforme a forma de acondicionamento."""

        forma = str(
            self.forma_acondicionamento.value or "SACA"
        ).strip().upper()

        if forma == "BAG":
            self.quantidade_sacas_prevista.label = (
                "Quantidade de bags"
            )
            self.quantidade_sacas_prevista.hint_text = (
                "Ex.: 2"
            )

        else:
            self.quantidade_sacas_prevista.label = (
                "Quantidade de sacas"
            )
            self.quantidade_sacas_prevista.hint_text = (
                "Ex.: 10"
            )

        # Limpa os valores ao trocar a forma de acondicionamento
        self.quantidade_sacas_prevista.value = "0"
        self.quantidade_kg_previsto.value = "0"

        self.quantidade_sacas_prevista.update()
        self.quantidade_kg_previsto.update()

    def abrir_calendario(
            self,
            e: ft.ControlEvent,
    ) -> None:
        """Abre o calendário da data de coleta."""

        data_atual = self._converter_data(
            self.data_agendada.value
        )

        if data_atual is not None:
            self.seletor_data.value = data_atual

        self.page.show_dialog(
            self.seletor_data
        )

    def ao_selecionar_data(
            self,
            e: ft.ControlEvent,
    ) -> None:
        """Exibe no formulário a data escolhida."""

        data_selecionada = self.seletor_data.value

        if data_selecionada is None:
            return

        self.data_agendada.value = (
            data_selecionada.strftime("%d/%m/%Y")
        )

        self.data_agendada.update()

    def ao_selecionar_estabelecimento(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Atualiza o resumo do estabelecimento selecionado."""

        valor = e.control.value

        if not valor:
            self._atualizar_resumo_estabelecimento(
                estabelecimento_id=None,
            )
            return

        try:
            estabelecimento_id = int(valor)

        except (TypeError, ValueError):
            self.resumo_estabelecimento.content = ft.Text(
                "Solicitante inválido.",
                color=ft.Colors.RED,
            )

            self.page.update()
            return

        self._atualizar_resumo_estabelecimento(
            estabelecimento_id=estabelecimento_id,
        )

    def ao_selecionar_motorista(
            self,
            e: ft.ControlEvent,
    ) -> None:
        """Atualiza a lista de veículos do motorista."""

        motorista_id = e.control.value

        if not motorista_id:
            return

        veiculos = self.veiculo_controller.listar_por_motorista(
            int(motorista_id)
        )

        self.veiculo.options = [
            ft.dropdown.Option(
                key=str(veiculo.id),
                text=(
                    f"{veiculo.marca} "
                    f"{veiculo.modelo} • "
                    f"{veiculo.placa}"
                ),
            )
            for veiculo in veiculos
            if veiculo.id is not None
        ]

        if len(veiculos) == 1:
            self.veiculo.value = str(veiculos[0].id)
        else:
            self.veiculo.value = None

        self.veiculo.update()

    def cancelar(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Retorna para a lista de solicitações."""

        if self.on_cancelar is not None:
            self.on_cancelar()

    def _obter_dados_formulario(
            self,
    ) -> tuple[dict | None, str | None]:
        """
        Lê, converte e valida os dados da solicitação.

        O agendamento operacional — data, motorista e veículo —
        é definido posteriormente pelo Gestor.
        """

        estabelecimento_valor = (
            self.estabelecimento.value
        )

        if not estabelecimento_valor:
            return (
                None,
                "Selecione um solicitante.",
            )

        try:
            estabelecimento_id = int(
                estabelecimento_valor
            )

        except (TypeError, ValueError):
            return (
                None,
                "Solicitante inválido.",
            )

        try:
            quantidade_sacas_prevista = int(
                self.quantidade_sacas_prevista.value or ""
            )

        except (TypeError, ValueError):
            return (
                None,
                "Quantidade de sacas inválida.",
            )

        if quantidade_sacas_prevista <= 0:
            return (
                None,
                "Informe pelo menos uma saca.",
            )

        quantidade_kg_previsto_texto = (
                self.quantidade_kg_previsto.value or "0"
        ).strip()

        try:
            quantidade_kg_previsto = float(
                quantidade_kg_previsto_texto.replace(
                    ",",
                    ".",
                )
            )

        except (TypeError, ValueError):
            return (
                None,
                "Quantidade em kg inválida.",
            )

        if quantidade_kg_previsto < 0:
            return (
                None,
                "A quantidade em kg não pode ser negativa.",
            )

        dados = {
            "estabelecimento_id": estabelecimento_id,
            "quantidade_sacas_prevista": (
                quantidade_sacas_prevista
            ),
            "quantidade_kg_previsto": (
                quantidade_kg_previsto
            ),
            "observacao_cliente": (
                    self.observacao.value or ""
            ).strip(),
        }

        return dados, None

    def _atualizar_solicitacao(
            self,
            dados: dict,
    ) -> tuple[bool, str]:
        """Atualiza a solicitação existente com os dados do formulário."""

        if self.solicitacao is None:
            return (
                False,
                "Solicitação não disponível para atualização.",
            )

        self.solicitacao.estabelecimento_id = (
            dados["estabelecimento_id"]
        )

        self.solicitacao.quantidade_sacas_prevista = (
            dados["quantidade_sacas_prevista"]
        )

        self.solicitacao.quantidade_kg_previsto = (
            dados["quantidade_kg_previsto"]
        )

        self.solicitacao.data_hora_agendada = (
            dados["data_hora_agendada"]
        )

        self.solicitacao.motorista_id = (
            dados["motorista_id"]
        )

        self.solicitacao.veiculo_id = (
            dados["veiculo_id"]
        )

        self.solicitacao.observacao_cliente = (
            dados["observacao_cliente"]
        )

        sucesso, mensagem, _ = (
            self.controller.atualizar(
                self.solicitacao
            )
        )

        return sucesso, mensagem

    def _criar_solicitacao(
            self,
            dados: dict,
    ) -> tuple[bool, str]:
        """Cadastra uma nova solicitação com os dados do formulário."""

        quantidade_prevista = int(
            dados.get("quantidade_prevista")
            or dados.get("quantidade_sacas_prevista")
            or 0
        )

        forma_acondicionamento = str(
            dados.get("forma_acondicionamento")
            or "SACA"
        ).strip().upper()

        sucesso, mensagem, _ = self.controller.criar(
            quantidade_prevista=quantidade_prevista,
            forma_acondicionamento=forma_acondicionamento,
            estabelecimento_id=dados.get(
                "estabelecimento_id"
            ),
            observacao_cliente=dados.get(
                "observacao_cliente"
            ) or "",
        )

        return sucesso, mensagem

    def executar_operacao(
            self,
            e: ft.ControlEvent,
    ) -> None:
        """Executa a próxima operação da solicitação."""

        if self.solicitacao is None:
            return

        sucesso, mensagem, solicitacao = (
            self.controller.alterar_status(
                self.solicitacao.id
            )
        )

        if not sucesso:
            mostrar_erro(
                self.page,
                mensagem,
            )
            return

        self.solicitacao = solicitacao

        self._atualizar_status_visual()
        self._atualizar_campos()

        self.page.update()

        mostrar_sucesso(
            self.page,
            mensagem,
        )

    def salvar(
            self,
            e: ft.ControlEvent,
    ) -> None:
        """Salva uma nova solicitação ou atualiza uma existente."""

        dados, mensagem_erro = (
            self._obter_dados_formulario()
        )

        if dados is None:
            mostrar_erro(
                self.page,
                mensagem_erro
                or "Não foi possível validar os dados.",
            )
            return

        if self.solicitacao is None:
            sucesso, mensagem = (
                self._criar_solicitacao(
                    dados
                )
            )

        else:
            sucesso, mensagem = (
                self._atualizar_solicitacao(
                    dados
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

        if self.on_salvar_sucesso is not None:
            self.on_salvar_sucesso()

    def build(self) -> ft.Control:
        """Constrói o formulário."""

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        (
                            "Editar Solicitação"
                            if self.solicitacao
                            else "Nova Solicitação de Coleta"
                        ),
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Selecione o solicitante e informe "
                        "os dados previstos para a coleta.",
                        size=15,
                    ),
                    ft.Divider(),

                    ft.Row(
                        controls=[
                            self.estabelecimento,
                        ],
                    ),

                    self.resumo_estabelecimento,

                    self.status_container,

                    ft.Row(
                        controls=[
                            self.botao_operacao,
                        ],
                    ),

                    ft.Row(
                        controls=[
                            self.forma_acondicionamento,
                        ],
                        spacing=15,
                    ),

                    ft.Row(
                        controls=[
                            self.quantidade_sacas_prevista,
                            self.quantidade_kg_previsto,
                        ],
                        spacing=15,
                    ),

                    self.observacao,

                    ft.Divider(),

                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content="Cancelar",
                                icon=ft.Icons.ARROW_BACK,
                                on_click=self.cancelar,
                            ),
                            ft.ElevatedButton(
                                content=(
                                    "Atualizar Solicitação"
                                    if self.solicitacao
                                    else "Salvar Solicitação"
                                ),
                                icon=ft.Icons.SAVE,
                                on_click=self.salvar,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            ),
            padding=0,
            expand=True,
        )