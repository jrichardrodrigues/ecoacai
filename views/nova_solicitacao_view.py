from __future__ import annotations

import flet as ft

from components.layout import BasePage
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from models.solicitacao_coleta import (
    FORMA_BAG,
    FORMA_SACA,
    TIPO_RESIDUO_CAROCO_ACAI,
)
from utils.messages import mostrar_erro, mostrar_sucesso


class NovaSolicitacaoView:
    """
    Tela simplificada para o Gerador solicitar uma coleta.

    O Gerador informa apenas os dados relacionados ao resíduo.
    Motorista, veículo e agendamento serão definidos pelo Gestor.
    """

    PESO_MEDIO_SACA_KG = 50
    PESO_MEDIO_BAG_KG = 1000

    def __init__(
        self,
        page: ft.Page,
        organizacao_id: int,
        usuario_id: int,
        controller: SolicitacaoColetaController | None = None,
    ) -> None:
        self.page = page
        self.organizacao_id = organizacao_id
        self.usuario_id = usuario_id

        self.controller = (
            controller or SolicitacaoColetaController()
        )

        self._criar_controles()
        self._atualizar_resumo()

    # ==========================================================
    # CONTROLES
    # ==========================================================

    def _criar_controles(self) -> None:
        self.tipo_residuo = ft.Dropdown(
            label="Tipo de resíduo",
            hint_text="Selecione o tipo de resíduo",
            value=TIPO_RESIDUO_CAROCO_ACAI,
            options=[
                ft.dropdown.Option(
                    key=TIPO_RESIDUO_CAROCO_ACAI,
                    text="Caroço de Açaí",
                ),
            ],
            border_radius=10,
            expand=True,
        )

        self.forma_acondicionamento = ft.RadioGroup(
            value=FORMA_SACA,
            on_change=self._ao_alterar_dados,
            content=ft.Column(
                controls=[
                    ft.Radio(
                        value=FORMA_SACA,
                        label="Sacas",
                    ),
                    ft.Radio(
                        value=FORMA_BAG,
                        label="Bags (1 m³)",
                    ),
                ],
                spacing=6,
            ),
        )

        self.quantidade = ft.TextField(
            label="Quantidade prevista",
            hint_text="Ex.: 10",
            value="1",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=True,
            on_change=self._ao_alterar_dados,
        )

        self.texto_peso = ft.Text(
            value="Peso estimado: 50 kg",
            size=16,
            weight=ft.FontWeight.BOLD,
        )

        self.texto_operacao = ft.Text(
            value="Operação prevista: Coleta manual",
            size=15,
        )

        self.texto_orientacao = ft.Text(
            value=(
                "As sacas podem ser carregadas manualmente "
                "pela equipe de coleta."
            ),
            size=13,
            color=ft.Colors.BLUE_GREY_700,
        )

        self.icone_operacao = ft.Icon(
            ft.Icons.PERSON_OUTLINE,
            size=34,
            color=ft.Colors.GREEN_700,
        )

        self.resumo_operacional = ft.Container(
            padding=16,
            border_radius=10,
            bgcolor=ft.Colors.BLUE_50,
            content=ft.Row(
                controls=[
                    self.icone_operacao,
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Resumo operacional",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_GREY_800,
                            ),
                            self.texto_peso,
                            self.texto_operacao,
                            self.texto_orientacao,
                        ],
                        spacing=4,
                        expand=True,
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )

        self.observacao = ft.TextField(
            label="Observações",
            hint_text=(
                "Informe detalhes que possam ajudar "
                "na preparação da coleta."
            ),
            multiline=True,
            min_lines=4,
            max_lines=6,
            border_radius=10,
        )

        self.indicador = ft.ProgressRing(
            width=22,
            height=22,
            visible=False,
        )

        self.botao_solicitar = ft.FilledButton(
            content="Solicitar coleta",
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            on_click=self._salvar,
        )

        self.botao_voltar = ft.OutlinedButton(
            content="Voltar",
            icon=ft.Icons.ARROW_BACK,
            on_click=self._voltar,
        )

    # ==========================================================
    # RESUMO OPERACIONAL
    # ==========================================================

    def _ao_alterar_dados(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        self._atualizar_resumo()

    def _obter_quantidade_para_resumo(self) -> int:
        """Lê a quantidade sem exibir mensagens durante a digitação."""

        texto = str(self.quantidade.value or "").strip()

        try:
            quantidade = int(texto)
        except (TypeError, ValueError):
            return 0

        return max(0, quantidade)

    def _atualizar_resumo(self) -> None:
        quantidade = self._obter_quantidade_para_resumo()

        forma = str(
            self.forma_acondicionamento.value
            or FORMA_SACA
        ).strip().upper()

        if forma == FORMA_BAG:
            peso_estimado = (
                quantidade * self.PESO_MEDIO_BAG_KG
            )
            operacao = "Caminhão Munck"
            orientacao = (
                "A coleta em Bags exige veículo equipado "
                "com Munck."
            )
            icone = ft.Icons.LOCAL_SHIPPING_OUTLINED
            cor_icone = ft.Colors.BLUE_700
            cor_fundo = ft.Colors.BLUE_50
        else:
            peso_estimado = (
                quantidade * self.PESO_MEDIO_SACA_KG
            )
            operacao = "Coleta manual"
            orientacao = (
                "As sacas podem ser carregadas manualmente "
                "pela equipe de coleta."
            )
            icone = ft.Icons.PERSON_OUTLINE
            cor_icone = ft.Colors.GREEN_700
            cor_fundo = ft.Colors.GREEN_50

        self.texto_peso.value = (
            "Peso estimado: "
            f"{self._formatar_numero(peso_estimado)} kg"
        )

        self.texto_operacao.value = (
            f"Operação prevista: {operacao}"
        )

        self.texto_orientacao.value = orientacao
        self.icone_operacao.icon = icone
        self.icone_operacao.color = cor_icone
        self.resumo_operacional.bgcolor = cor_fundo

        self._atualizar_pagina()

    @staticmethod
    def _formatar_numero(valor: int | float) -> str:
        """Formata números com separador de milhar brasileiro."""

        return f"{valor:,.0f}".replace(",", ".")

    # ==========================================================
    # VALIDAÇÃO
    # ==========================================================

    def _obter_quantidade(self) -> int | None:
        texto = str(
            self.quantidade.value or ""
        ).strip()

        if not texto:
            mostrar_erro(
                self.page,
                "Informe a quantidade prevista.",
            )
            return None

        try:
            quantidade = int(texto)

        except (TypeError, ValueError):
            mostrar_erro(
                self.page,
                "A quantidade informada é inválida.",
            )
            return None

        if quantidade <= 0:
            mostrar_erro(
                self.page,
                "A quantidade deve ser maior que zero.",
            )
            return None

        return quantidade

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def _salvar(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        quantidade = self._obter_quantidade()

        if quantidade is None:
            return

        tipo_residuo = str(
            self.tipo_residuo.value
            or TIPO_RESIDUO_CAROCO_ACAI
        ).strip().upper()

        forma_acondicionamento = str(
            self.forma_acondicionamento.value
            or FORMA_SACA
        ).strip().upper()

        observacao = str(
            self.observacao.value or ""
        ).strip()

        self._definir_carregamento(True)

        try:
            sucesso, mensagem, _solicitacao = (
                self.controller.criar(
                    quantidade_prevista=quantidade,
                    forma_acondicionamento=(
                        forma_acondicionamento
                    ),
                    organizacao_id=self.organizacao_id,
                    usuario_criacao_id=self.usuario_id,
                    tipo_residuo=tipo_residuo,
                    origem="GERADOR",
                    observacao_cliente=observacao,
                )
            )

        except Exception as erro:
            print(
                "Erro ao solicitar coleta:",
                erro,
            )

            sucesso = False
            mensagem = (
                "Não foi possível registrar a solicitação."
            )

        finally:
            self._definir_carregamento(False)

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

        self._abrir_minhas_solicitacoes()

    # ==========================================================
    # NAVEGAÇÃO
    # ==========================================================

    def _voltar(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        navigation_controller = getattr(
            self.page,
            "navigation_controller",
            None,
        )

        if navigation_controller is not None:
            navigation_controller.ir_para(
                "portal_gerador"
            )

    def _abrir_minhas_solicitacoes(self) -> None:
        navigation_controller = getattr(
            self.page,
            "navigation_controller",
            None,
        )

        if navigation_controller is not None:
            navigation_controller.ir_para(
                "minhas_solicitacoes"
            )

    # ==========================================================
    # ESTADO VISUAL
    # ==========================================================

    def _definir_carregamento(
        self,
        carregando: bool,
    ) -> None:
        self.indicador.visible = carregando
        self.botao_solicitar.disabled = carregando
        self.botao_voltar.disabled = carregando

        self._atualizar_pagina()

    def _atualizar_pagina(self) -> None:
        try:
            self.page.update()
        except RuntimeError:
            pass

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def construir(self) -> ft.Control:
        formulario = ft.Container(
            padding=24,
            border_radius=12,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Dados da coleta",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        (
                            "Informe como o resíduo está "
                            "acondicionado e a quantidade disponível."
                        ),
                        size=14,
                    ),
                    ft.Divider(),
                    self.tipo_residuo,
                    ft.Text(
                        "Forma de acondicionamento",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.forma_acondicionamento,
                    self.quantidade,
                    self.resumo_operacional,
                    self.observacao,
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self.botao_voltar,
                            ft.Container(
                                expand=True,
                            ),
                            self.indicador,
                            self.botao_solicitar,
                        ],
                        vertical_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        spacing=12,
                    ),
                ],
                spacing=16,
            ),
        )

        return BasePage(
            title="Solicitar Coleta",
            subtitle=(
                "Registre uma nova solicitação para "
                "a sua organização."
            ),
            content=formulario,
            max_width=850,
        )

    def build(self) -> ft.Control:
        """Mantém compatibilidade com o padrão das Views."""

        return self.construir()
