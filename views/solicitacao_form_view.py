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

        self.estabelecimento = ft.Dropdown(
            label="Estabelecimento",
            hint_text="Selecione o estabelecimento",
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

        self.quantidade_sacas = ft.TextField(
            label="Quantidade de sacas",
            hint_text="Ex.: 10",
            value="1",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=True,
        )

        self.quantidade_kg = ft.TextField(
            label="Quantidade em kg",
            hint_text="Ex.: 250",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=True,
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

        self.motorista = ft.TextField(
            label="Motorista",
            hint_text="Nome do motorista",
            value="",
            border_radius=10,
            expand=True,
        )

        self.veiculo = ft.TextField(
            label="Veículo",
            hint_text="Placa ou identificação",
            value="",
            border_radius=10,
            expand=True,
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
                        "Selecione um estabelecimento.",
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

        self._carregar_solicitacao()

        self._atualizar_resumo_estabelecimento(
            self._obter_estabelecimento_selecionado_id(),
            atualizar_pagina=False,
        )

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

        self.quantidade_sacas.value = str(
            self.solicitacao.quantidade_sacas
        )

        self.quantidade_kg.value = str(
            self.solicitacao.quantidade_kg
        )

        data_agendada = self._converter_data(
            self.solicitacao.data_agendada
        )

        if data_agendada is not None:
            self.data_agendada.value = (
                data_agendada.strftime("%d/%m/%Y")
            )
        else:
            self.data_agendada.value = (
                    self.solicitacao.data_agendada or ""
            )

        self.motorista.value = (
                self.solicitacao.motorista or ""
        )

        self.veiculo.value = (
                self.solicitacao.veiculo or ""
        )

        self.observacao.value = (
                self.solicitacao.observacao or ""
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
                        "Selecione um estabelecimento.",
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
                "Estabelecimento não encontrado.",
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
                "Estabelecimento inválido.",
                color=ft.Colors.RED,
            )

            self.page.update()
            return

        self._atualizar_resumo_estabelecimento(
            estabelecimento_id=estabelecimento_id,
        )

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
        Lê, converte e valida os dados informados no formulário.

        Returns:
            Uma tupla contendo:
            - dicionário com os dados convertidos, quando válidos;
            - mensagem de erro, quando algum dado for inválido.
        """

        estabelecimento_valor = (
            self.estabelecimento.value
        )

        if not estabelecimento_valor:
            return (
                None,
                "Selecione um estabelecimento.",
            )

        try:
            estabelecimento_id = int(
                estabelecimento_valor
            )

        except (TypeError, ValueError):
            return (
                None,
                "Estabelecimento inválido.",
            )

        try:
            quantidade_sacas = int(
                self.quantidade_sacas.value or ""
            )

        except (TypeError, ValueError):
            return (
                None,
                "Quantidade de sacas inválida.",
            )

        if quantidade_sacas <= 0:
            return (
                None,
                "Informe pelo menos uma saca.",
            )

        quantidade_kg_texto = (
                self.quantidade_kg.value or "0"
        ).strip()

        try:
            quantidade_kg = float(
                quantidade_kg_texto.replace(",", ".")
            )

        except (TypeError, ValueError):
            return (
                None,
                "Quantidade em kg inválida.",
            )

        if quantidade_kg < 0:
            return (
                None,
                "A quantidade em kg não pode ser negativa.",
            )

        dados = {
            "estabelecimento_id": estabelecimento_id,
            "quantidade_sacas": quantidade_sacas,
            "quantidade_kg": quantidade_kg,
            "data_agendada": (
                    self.data_agendada.value or ""
            ).strip(),
            "motorista": (
                    self.motorista.value or ""
            ).strip(),
            "veiculo": (
                    self.veiculo.value or ""
            ).strip(),
            "observacao": (
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

        self.solicitacao.quantidade_sacas = (
            dados["quantidade_sacas"]
        )

        self.solicitacao.quantidade_kg = (
            dados["quantidade_kg"]
        )

        self.solicitacao.data_agendada = (
            dados["data_agendada"]
        )

        self.solicitacao.motorista = (
            dados["motorista"]
        )

        self.solicitacao.veiculo = (
            dados["veiculo"]
        )

        self.solicitacao.observacao = (
            dados["observacao"]
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

        sucesso, mensagem, _ = self.controller.criar(
            estabelecimento_id=dados[
                "estabelecimento_id"
            ],
            quantidade_sacas=dados[
                "quantidade_sacas"
            ],
            quantidade_kg=dados[
                "quantidade_kg"
            ],
            data_agendada=dados[
                "data_agendada"
            ],
            motorista=dados[
                "motorista"
            ],
            veiculo=dados[
                "veiculo"
            ],
            observacao=dados[
                "observacao"
            ],
        )

        return sucesso, mensagem

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
                        "Selecione o estabelecimento e informe "
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

                    ft.Row(
                        controls=[
                            self.quantidade_sacas,
                            self.quantidade_kg,
                        ],
                        spacing=15,
                    ),

                    ft.Row(
                        controls=[
                            self.data_agendada,
                        ],
                    ),

                    ft.Row(
                        controls=[
                            self.motorista,
                            self.veiculo,
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