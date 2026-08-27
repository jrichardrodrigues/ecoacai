from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path

import flet as ft

from components.buttons import PrimaryButton, SecondaryButton
from components.layout import PageHeader
from config.constants import BAIRROS_SETORES, SETORES

from services.relatorio_service import RelatorioService
from services.relatorio_pdf_service import RelatorioPdfService


class RelatoriosView:
    """Tela de consulta e geração de relatórios de coletas."""

    ITENS_POR_PAGINA = 2

    def __init__(
            self,
            page: ft.Page,
    ) -> None:
        self.page = page
        self.relatorio_service = RelatorioService()
        self.relatorio_pdf_service = RelatorioPdfService()

        self.pagina_atual = 1
        self.total_paginas = 1
        self.registros_relatorio: list[dict] = []
        self.resumo_relatorio: dict = {}

        # ======================================================
        # FILTROS
        # ======================================================

        self.setor_dropdown = ft.Dropdown(
            label="Setor",
            hint_text="Selecione o setor",
            width=220,
            options=[
                ft.DropdownOption(
                    key=setor,
                    text=setor,
                )
                for setor in SETORES
            ],
            on_select=self._ao_alterar_setor,
        )

        self.bairro_dropdown = ft.Dropdown(
            label="Bairro",
            hint_text="Todos os bairros",
            width=280,
            disabled=True,
            options=[],
        )

        self.data_inicial_field = ft.TextField(
            label="Data inicial",
            hint_text="dd/mm/aaaa",
            width=180,
            read_only=True,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self._abrir_data_inicial,
            always_call_on_tap=True,
        )

        self.data_final_field = ft.TextField(
            label="Data final",
            hint_text="dd/mm/aaaa",
            width=180,
            read_only=True,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self._abrir_data_final,
            always_call_on_tap=True,
        )

        self.botao_pesquisar = PrimaryButton(
            label="Pesquisar",
            icon=ft.Icons.SEARCH,
            on_click=self._ao_pesquisar,
        )

        self.botao_limpar = SecondaryButton(
            label="Limpar",
            icon=ft.Icons.CLEAR,
            on_click=self._limpar_filtros,
        )

        self.botao_gerar_pdf = PrimaryButton(
            label="Gerar PDF",
            icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
            on_click=self._gerar_pdf,
            disabled=True,
        )

        # ======================================================
        # ESTADO INICIAL
        # ======================================================

        self.estado_inicial = ft.Column(
            controls=[
                ft.Text(
                    "Resumo das Coletas",
                    size=18,
                    weight=ft.FontWeight.W_600,
                ),

                ft.Row(
                    controls=[
                        self._criar_indicador(
                            "Coletas realizadas",
                            "0",
                            ft.Icons.LOCAL_SHIPPING_OUTLINED,
                        ),
                        self._criar_indicador(
                            "Sacas coletadas",
                            "0",
                            ft.Icons.INVENTORY_2_OUTLINED,
                        ),
                        self._criar_indicador(
                            "Bags coletados",
                            "0",
                            ft.Icons.WORK_OUTLINE,
                        ),
                        self._criar_indicador(
                            "Peso total",
                            "0,00 kg",
                            ft.Icons.SCALE_OUTLINED,
                        ),
                    ],
                    spacing=12,
                ),

                ft.Text(
                    "Detalhamento das Coletas",
                    size=18,
                    weight=ft.FontWeight.W_600,
                ),
            ],
            spacing=16,
        )

        # ======================================================
        # RESULTADOS
        # ======================================================

        self.area_resultados = ft.Column(
            controls=[],
            spacing=18,
            visible=False,
        )

        self.anterior_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            tooltip="Página anterior",
            on_click=self._pagina_anterior,
        )

        self.proxima_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            tooltip="Próxima página",
            on_click=self._proxima_pagina,
        )

        self.paginacao_text = ft.Text(
            "Página 1 de 1",
            weight=ft.FontWeight.W_500,
        )

        # ======================================================
        # CONTAINER PRINCIPAL
        # ======================================================

        self.container = ft.Container(
            expand=True,
            padding=24,
            content=ft.Column(
                controls=[
                    self._construir_cabecalho(),
                    ft.Divider(),
                    self._construir_filtros(),
                    self.estado_inicial,
                    self.area_resultados,
                ],
                spacing=18,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

    # ==========================================================
    # CONSTRUÇÃO
    # ==========================================================

    def build(self) -> ft.Control:
        return self.container

    def _construir_cabecalho(self) -> ft.Control:
        return ft.Row(
            controls=[
                ft.Container(
                    content=PageHeader(
                        title="Relatórios de Coletas",
                        subtitle=(
                            "Consulte e gere relatórios "
                            "da operação ECOAÇAÍ."
                        ),
                        show_divider=False,
                    ),
                    expand=True,
                ),
                self.botao_gerar_pdf,
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _construir_filtros(self) -> ft.Control:
        return ft.Row(
            controls=[
                self.setor_dropdown,
                self.bairro_dropdown,
                self.data_inicial_field,
                self.data_final_field,
                self.botao_pesquisar,
                self.botao_limpar,
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ==========================================================
    # SETOR / BAIRRO
    # ==========================================================

    def _ao_alterar_setor(
            self,
            event: ft.Event[ft.Dropdown] | None = None,
    ) -> None:
        setor = str(
            self.setor_dropdown.value or ""
        ).strip()

        self.bairro_dropdown.value = None

        if not setor:
            self.bairro_dropdown.options = []
            self.bairro_dropdown.disabled = True
            self._atualizar_pagina()
            return

        bairros = sorted(
            bairro
            for bairro, setor_bairro in BAIRROS_SETORES.items()
            if setor_bairro == setor
        )

        self.bairro_dropdown.options = [
            ft.DropdownOption(
                key="TODOS",
                text="Todos os bairros",
            ),
            *[
                ft.DropdownOption(
                    key=bairro,
                    text=bairro,
                )
                for bairro in bairros
            ],
        ]

        self.bairro_dropdown.value = "TODOS"
        self.bairro_dropdown.disabled = False

        self._atualizar_pagina()

    # ==========================================================
    # RESULTADOS
    # ==========================================================

    def _criar_indicador(
            self,
            titulo: str,
            valor: str,
            icone,
    ) -> ft.Control:
        return ft.Container(
            width=260,
            height=92,
            padding=20,
            border=ft.Border.all(
                1,
                ft.Colors.OUTLINE_VARIANT,
            ),
            border_radius=12,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=44,
                        height=44,
                        border_radius=10,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            icone,
                            size=24,
                        ),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                titulo,
                                size=13,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                            ft.Text(
                                valor,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=2,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _criar_tabela_coletas(
            self,
            registros: list[dict],
    ) -> ft.Control:

        if not registros:
            return ft.Container(
                padding=24,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    "Nenhuma coleta encontrada para os filtros informados.",
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            )

        linhas = []

        for registro in registros:
            forma = str(
                registro.get("forma_acondicionamento") or ""
            ).strip().upper()

            quantidade = int(
                registro.get("quantidade_sacas_coletada") or 0
            )

            peso = float(
                registro.get("quantidade_kg_coletado") or 0
            )

            peso_formatado = (
                f"{peso:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            data_conclusao = str(
                registro.get("data_hora_conclusao") or ""
            ).strip()

            if data_conclusao:
                try:
                    data_conclusao = datetime.fromisoformat(
                        data_conclusao
                    ).strftime("%d/%m/%Y %H:%M")
                except ValueError:
                    pass

            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                str(registro.get("codigo") or "")
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(registro.get("solicitante") or "")
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(registro.get("bairro") or "")
                            )
                        ),
                        ft.DataCell(
                            ft.Text(forma)
                        ),
                        ft.DataCell(
                            ft.Text(str(quantidade))
                        ),
                        ft.DataCell(
                            ft.Text(f"{peso_formatado} kg")
                        ),
                        ft.DataCell(
                            ft.Text(data_conclusao)
                        ),
                    ],
                )
            )

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.DataTable(
                            columns=[
                                ft.DataColumn(
                                    label=ft.Text(
                                        "Código",
                                        size=17,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    label=ft.Text(
                                        "Solicitante",
                                        size=17,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    label=ft.Text(
                                        "Bairro",
                                        size=17,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    label=ft.Text(
                                        "Acondicionamento",
                                        size=17,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    label=ft.Text(
                                        "Quantidade",
                                        size=17,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    numeric=True,
                                ),
                                ft.DataColumn(
                                    label=ft.Text(
                                        "Peso coletado",
                                        size=17,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    numeric=True,
                                ),
                                ft.DataColumn(
                                    label=ft.Text(
                                        "Conclusão",
                                        size=17,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                            ],
                            rows=linhas,
                            column_spacing=24,
                            horizontal_lines=ft.BorderSide(
                                width=1,
                                color=ft.Colors.OUTLINE_VARIANT,
                            ),
                        ),
                        width=1300,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            border=ft.Border.all(
                width=1,
                color=ft.Colors.OUTLINE_VARIANT,
            ),
            border_radius=8,
            padding=8,
        )

    def _criar_descricao_filtros(self) -> ft.Control:
        setor = str(
            self.setor_dropdown.value or ""
        ).strip()

        bairro = str(
            self.bairro_dropdown.value or "TODOS"
        ).strip()

        if bairro == "TODOS":
            bairro_texto = "Todos os bairros"
        else:
            bairro_texto = bairro

        data_inicial = str(
            self.data_inicial_field.value or ""
        ).strip()

        data_final = str(
            self.data_final_field.value or ""
        ).strip()

        if data_inicial and data_final:
            periodo = (
                f"Período: {data_inicial} a {data_final}"
            )
        elif data_inicial:
            periodo = (
                f"A partir de {data_inicial}"
            )
        elif data_final:
            periodo = (
                f"Até {data_final}"
            )
        else:
            periodo = "Todo o período"

        return ft.Text(
            f"{setor}  •  {bairro_texto}  •  {periodo}",
            size=14,
            color=ft.Colors.ON_SURFACE_VARIANT,
            weight=ft.FontWeight.W_500,
        )

    def _mostrar_resultados(
            self,
            dados: dict,
    ) -> None:
        resumo = dados.get("resumo", {})
        registros = dados.get("registros", [])

        self.registros_relatorio = list(
            registros or []
        )

        self.botao_gerar_pdf.disabled = (
            not self.registros_relatorio
        )

        self.resumo_relatorio = dict(
            resumo or {}
        )

        self.pagina_atual = 1

        self._atualizar_paginacao()
        self._reconstruir_resultados()

    def _reconstruir_resultados(self) -> None:
        resumo = self.resumo_relatorio

        total_coletas = int(
            resumo.get("total_coletas", 0)
        )

        total_sacas = int(
            resumo.get("total_sacas", 0)
        )

        total_bags = int(
            resumo.get("total_bags", 0)
        )

        total_kg = float(
            resumo.get("total_kg", 0)
        )

        peso_formatado = (
            f"{total_kg:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        registros_pagina = (
            self._obter_registros_pagina()
        )

        self._atualizar_paginacao()

        self.area_resultados.controls = [
            ft.Text(
                "Resumo das Coletas",
                size=18,
                weight=ft.FontWeight.W_600,
            ),

            self._criar_descricao_filtros(),

            ft.Row(
                controls=[
                    self._criar_indicador(
                        "Coletas realizadas",
                        str(total_coletas),
                        ft.Icons.LOCAL_SHIPPING_OUTLINED,
                    ),
                    self._criar_indicador(
                        "Sacas coletadas",
                        str(total_sacas),
                        ft.Icons.INVENTORY_2_OUTLINED,
                    ),
                    self._criar_indicador(
                        "Bags coletados",
                        str(total_bags),
                        ft.Icons.WORK_OUTLINE,
                    ),
                    self._criar_indicador(
                        "Peso total",
                        f"{peso_formatado} kg",
                        ft.Icons.SCALE_OUTLINED,
                    ),
                ],
                spacing=12,
                wrap=True,
            ),

            ft.Text(
                "Detalhamento das Coletas",
                size=18,
                weight=ft.FontWeight.W_600,
            ),

            self._criar_tabela_coletas(
                registros_pagina
            ),

            self._construir_paginacao(),
        ]

        self.estado_inicial.visible = False
        self.area_resultados.visible = True

        self._atualizar_pagina()

    def _construir_paginacao(self) -> ft.Control:
        return ft.Row(
            controls=[
                self.anterior_button,
                self.paginacao_text,
                self.proxima_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _obter_registros_pagina(self) -> list[dict]:
        inicio = (
                         self.pagina_atual - 1
                 ) * self.ITENS_POR_PAGINA

        fim = inicio + self.ITENS_POR_PAGINA

        return self.registros_relatorio[inicio:fim]

    def _atualizar_paginacao(self) -> None:
        total_registros = len(
            self.registros_relatorio
        )

        self.total_paginas = max(
            1,
            math.ceil(
                total_registros
                / self.ITENS_POR_PAGINA
            ),
        )

        if self.pagina_atual > self.total_paginas:
            self.pagina_atual = self.total_paginas

        self.paginacao_text.value = (
            f"Página {self.pagina_atual} "
            f"de {self.total_paginas}"
        )

        self.anterior_button.disabled = (
                self.pagina_atual <= 1
        )

        self.proxima_button.disabled = (
                self.pagina_atual
                >= self.total_paginas
        )

    def _pagina_anterior(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        if self.pagina_atual <= 1:
            return

        self.pagina_atual -= 1
        self._reconstruir_resultados()

    def _proxima_pagina(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        if self.pagina_atual >= self.total_paginas:
            return

        self.pagina_atual += 1
        self._reconstruir_resultados()

    # ==========================================================
    # AÇÕES
    # ==========================================================

    def _abrir_data_inicial(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        picker = ft.DatePicker(
            help_text="Selecione a data inicial",
            cancel_text="Cancelar",
            confirm_text="Selecionar",
            entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY,
            on_change=self._selecionar_data_inicial,
        )

        self.page.show_dialog(picker)

    def _abrir_data_final(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        picker = ft.DatePicker(
            help_text="Selecione a data final",
            cancel_text="Cancelar",
            confirm_text="Selecionar",
            entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY,
            on_change=self._selecionar_data_final,
        )

        self.page.show_dialog(picker)

    def _selecionar_data_inicial(
            self,
            event: ft.Event[ft.DatePicker],
    ) -> None:
        data = event.control.value

        if data is None:
            return

        self.data_inicial_field.value = data.strftime(
            "%d/%m/%Y"
        )

        self._atualizar_pagina()

    def _selecionar_data_final(
            self,
            event: ft.Event[ft.DatePicker],
    ) -> None:
        data = event.control.value

        if data is None:
            return

        self.data_final_field.value = data.strftime(
            "%d/%m/%Y"
        )

        self._atualizar_pagina()

    def _ao_pesquisar(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:

        setor = str(
            self.setor_dropdown.value or ""
        ).strip()

        if not setor:
            self._mostrar_mensagem(
                "Selecione um setor para consultar o relatório.",
                erro=True,
            )
            return

        bairro = str(
            self.bairro_dropdown.value or "TODOS"
        ).strip()

        try:
            data_inicial = self._converter_data_filtro(
                self.data_inicial_field.value
            )

            data_final = self._converter_data_filtro(
                self.data_final_field.value
            )

            if (
                    data_inicial
                    and data_final
                    and data_inicial > data_final
            ):
                raise ValueError(
                    "A data inicial não pode ser maior "
                    "que a data final."
                )

            dados = (
                self.relatorio_service
                .obter_coletas_por_setor(
                    setor=setor,
                    bairro=bairro,
                    data_inicial=data_inicial,
                    data_final=data_final,
                )
            )

            self._mostrar_resultados(
                dados
            )

            # Habilita o PDF após uma consulta válida
            self.botao_gerar_pdf.disabled = False

            self._atualizar_pagina()

        except ValueError as erro:
            self._mostrar_mensagem(
                str(erro),
                erro=True,
            )

        except Exception as erro:
            self._mostrar_mensagem(
                (
                    "Não foi possível consultar "
                    f"o relatório: {erro}"
                ),
                erro=True,
            )

    def _gerar_pdf(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:

        if not self.registros_relatorio:
            self._mostrar_mensagem(
                "Não há dados para gerar o relatório.",
                erro=True,
            )
            return

        setor = str(
            self.setor_dropdown.value or ""
        ).strip()

        bairro = str(
            self.bairro_dropdown.value or "TODOS"
        ).strip()

        data_inicial = str(
            self.data_inicial_field.value or ""
        ).strip()

        data_final = str(
            self.data_final_field.value or ""
        ).strip()

        agora = datetime.now()

        nome_arquivo = (
            "relatorio_coletas_"
            f"{agora.strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        caminho_arquivo = (
                Path("relatorios")
                / nome_arquivo
        )

        try:
            caminho_gerado = (
                self.relatorio_pdf_service
                .gerar_relatorio_coletas(
                    caminho_arquivo=caminho_arquivo,
                    setor=setor,
                    bairro=bairro,
                    data_inicial=data_inicial or None,
                    data_final=data_final or None,
                    resumo=self.resumo_relatorio,
                    registros=self.registros_relatorio,
                )
            )

            self._mostrar_mensagem(
                f"Relatório gerado com sucesso: "
                f"{caminho_gerado}"
            )

        except Exception as exc:
            self._mostrar_mensagem(
                f"Não foi possível gerar o PDF: {exc}",
                erro=True,
            )

    def _limpar_filtros(
            self,
            event: ft.Event[ft.Control] | None = None,
    ) -> None:
        self.setor_dropdown.value = None

        self.bairro_dropdown.value = None
        self.bairro_dropdown.options = []
        self.bairro_dropdown.disabled = True

        self.data_inicial_field.value = ""
        self.data_final_field.value = ""

        self.pagina_atual = 1
        self.total_paginas = 1
        self.registros_relatorio = []
        self.resumo_relatorio = {}

        self.area_resultados.controls = []
        self.area_resultados.visible = False
        self.estado_inicial.visible = True

        self.botao_gerar_pdf.disabled = True

        self._atualizar_pagina()

    # ==========================================================
    # UTILITÁRIOS
    # ==========================================================

    @staticmethod
    def _converter_data_filtro(
            valor: str | None,
    ) -> str | None:
        """
        Converte uma data no formato dd/mm/aaaa
        para aaaa-mm-dd.

        Campo vazio retorna None.
        """

        texto = str(
            valor or ""
        ).strip()

        if not texto:
            return None

        try:
            data = datetime.strptime(
                texto,
                "%d/%m/%Y",
            )
        except ValueError as erro:
            raise ValueError(
                "Informe as datas no formato dd/mm/aaaa."
            ) from erro

        return data.strftime("%Y-%m-%d")

    def _mostrar_mensagem(
            self,
            mensagem: str,
            erro: bool = False,
    ) -> None:
        snackbar = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color=ft.Colors.WHITE,
            ),
            bgcolor=(
                ft.Colors.RED_700
                if erro
                else ft.Colors.PRIMARY
            ),
        )

        self.page.show_dialog(
            snackbar
        )

    def _atualizar_pagina(self) -> None:
        try:
            self.page.update()
        except RuntimeError:
            # O controle pode ainda não estar anexado à página.
            pass