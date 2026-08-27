from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class RelatorioColetasPDF:
    """
    Gera o relatório PDF de coletas realizadas por setor.

    Recebe os dados já preparados pelo RelatorioService.
    Não realiza consultas ao banco de dados.
    """

    # ==========================================================
    # CORES ECOAÇAÍ
    # ==========================================================

    COR_PRINCIPAL = colors.HexColor("#861747")
    COR_TEXTO = colors.HexColor("#2F2930")
    COR_TEXTO_SECUNDARIO = colors.HexColor("#6F646A")
    COR_LINHA = colors.HexColor("#DDD6DA")
    COR_FUNDO_CABECALHO = colors.HexColor("#F3EDF0")
    COR_FUNDO_RESUMO = colors.HexColor("#FAF7F8")

    def __init__(self):
        self.estilos = getSampleStyleSheet()
        self._criar_estilos()

    # ==========================================================
    # ESTILOS
    # ==========================================================

    def _criar_estilos(self) -> None:
        self.estilo_marca = ParagraphStyle(
            name="MarcaEcoAcai",
            parent=self.estilos["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            textColor=self.COR_PRINCIPAL,
            alignment=TA_LEFT,
        )

        self.estilo_slogan = ParagraphStyle(
            name="SloganEcoAcai",
            parent=self.estilos["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=self.COR_TEXTO_SECUNDARIO,
            alignment=TA_LEFT,
        )

        self.estilo_titulo = ParagraphStyle(
            name="TituloRelatorio",
            parent=self.estilos["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=self.COR_TEXTO,
            alignment=TA_LEFT,
            spaceAfter=4,
        )

        self.estilo_filtro = ParagraphStyle(
            name="FiltroRelatorio",
            parent=self.estilos["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=self.COR_TEXTO_SECUNDARIO,
        )

        self.estilo_resumo_titulo = ParagraphStyle(
            name="ResumoTitulo",
            parent=self.estilos["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=self.COR_TEXTO_SECUNDARIO,
            alignment=TA_CENTER,
        )

        self.estilo_resumo_valor = ParagraphStyle(
            name="ResumoValor",
            parent=self.estilos["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=self.COR_TEXTO,
            alignment=TA_CENTER,
        )

        self.estilo_tabela = ParagraphStyle(
            name="Tabela",
            parent=self.estilos["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=self.COR_TEXTO,
        )

        self.estilo_tabela_direita = ParagraphStyle(
            name="TabelaDireita",
            parent=self.estilo_tabela,
            alignment=TA_RIGHT,
        )

        self.estilo_sem_registros = ParagraphStyle(
            name="SemRegistros",
            parent=self.estilos["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=self.COR_TEXTO_SECUNDARIO,
            alignment=TA_CENTER,
            spaceBefore=8,
            spaceAfter=8,
        )

    # ==========================================================
    # FORMATAÇÃO
    # ==========================================================

    @staticmethod
    def _formatar_data(valor: str | None) -> str:
        if not valor:
            return "-"

        try:
            data = datetime.fromisoformat(valor)
            return data.strftime("%d/%m/%Y")
        except (TypeError, ValueError):
            return str(valor)

    @staticmethod
    def _formatar_periodo(
            data_inicial: str | None,
            data_final: str | None,
    ) -> str:
        if data_inicial and data_final:
            inicio = RelatorioColetasPDF._formatar_data(
                data_inicial
            )
            fim = RelatorioColetasPDF._formatar_data(
                data_final
            )
            return f"{inicio} a {fim}"

        if data_inicial:
            return (
                "A partir de "
                f"{RelatorioColetasPDF._formatar_data(data_inicial)}"
            )

        if data_final:
            return (
                "Até "
                f"{RelatorioColetasPDF._formatar_data(data_final)}"
            )

        return "Todo o período"

    @staticmethod
    def _formatar_numero(valor: float | int) -> str:
        return f"{valor:,.0f}".replace(",", ".")

    @staticmethod
    def _formatar_peso(valor: float | int) -> str:
        return (
            f"{valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    # ==========================================================
    # CABEÇALHO / RODAPÉ
    # ==========================================================

    def _desenhar_cabecalho_rodape(
            self,
            canvas,
            doc,
    ) -> None:
        canvas.saveState()

        largura, altura = landscape(A4)

        # Linha superior institucional
        canvas.setStrokeColor(self.COR_PRINCIPAL)
        canvas.setLineWidth(2)
        canvas.line(
            15 * mm,
            altura - 12 * mm,
            largura - 15 * mm,
            altura - 12 * mm,
        )

        # Rodapé
        canvas.setStrokeColor(self.COR_LINHA)
        canvas.setLineWidth(0.5)
        canvas.line(
            15 * mm,
            12 * mm,
            largura - 15 * mm,
            12 * mm,
        )

        canvas.setFillColor(self.COR_TEXTO_SECUNDARIO)
        canvas.setFont("Helvetica", 7)

        canvas.drawString(
            15 * mm,
            7 * mm,
            "ECOAÇAÍ • Gestão Inteligente de Resíduo do Açaí",
        )

        canvas.drawRightString(
            largura - 15 * mm,
            7 * mm,
            f"Página {doc.page}",
        )

        canvas.restoreState()

    # ==========================================================
    # GERAÇÃO
    # ==========================================================

    def gerar(
            self,
            dados: dict,
            caminho_saida: str | Path,
    ) -> Path:
        """
        Gera o arquivo PDF e retorna o caminho criado.
        """

        caminho = Path(caminho_saida)

        caminho.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        documento = SimpleDocTemplate(
            str(caminho),
            pagesize=landscape(A4),
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
            title=dados.get(
                "titulo",
                "Relatório de Coletas",
            ),
            author="ECOAÇAÍ",
        )

        elementos = []

        # ======================================================
        # IDENTIDADE
        # ======================================================

        elementos.append(
            Paragraph(
                "ECOAÇAÍ",
                self.estilo_marca,
            )
        )

        elementos.append(
            Paragraph(
                "GESTÃO INTELIGENTE DE RESÍDUO DO AÇAÍ",
                self.estilo_slogan,
            )
        )

        elementos.append(
            Spacer(1, 7 * mm)
        )

        # ======================================================
        # TÍTULO
        # ======================================================

        elementos.append(
            Paragraph(
                dados.get(
                    "titulo",
                    "Relatório de Coletas por Setor",
                ),
                self.estilo_titulo,
            )
        )

        filtros = dados.get("filtros", {})

        setor = filtros.get("setor") or "Todos"
        bairro = filtros.get("bairro") or "Todos"

        periodo = self._formatar_periodo(
            filtros.get("data_inicial"),
            filtros.get("data_final"),
        )

        elementos.append(
            Paragraph(
                f"<b>Setor:</b> {setor}"
                f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                f"<b>Bairro:</b> {bairro}"
                f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                f"<b>Período:</b> {periodo}",
                self.estilo_filtro,
            )
        )

        elementos.append(
            Spacer(1, 6 * mm)
        )

        # ======================================================
        # RESUMO
        # ======================================================

        resumo = dados.get("resumo", {})

        resumo_dados = [
            [
                Paragraph(
                    "COLETAS REALIZADAS",
                    self.estilo_resumo_titulo,
                ),
                Paragraph(
                    "SACAS COLETADAS",
                    self.estilo_resumo_titulo,
                ),
                Paragraph(
                    "BAGS COLETADOS",
                    self.estilo_resumo_titulo,
                ),
                Paragraph(
                    "PESO TOTAL",
                    self.estilo_resumo_titulo,
                ),
            ],
            [
                Paragraph(
                    self._formatar_numero(
                        resumo.get("total_coletas", 0)
                    ),
                    self.estilo_resumo_valor,
                ),
                Paragraph(
                    self._formatar_numero(
                        resumo.get("total_sacas", 0)
                    ),
                    self.estilo_resumo_valor,
                ),
                Paragraph(
                    self._formatar_numero(
                        resumo.get("total_bags", 0)
                    ),
                    self.estilo_resumo_valor,
                ),
                Paragraph(
                    (
                        self._formatar_peso(
                            resumo.get("total_kg", 0)
                        )
                        + " kg"
                    ),
                    self.estilo_resumo_valor,
                ),
            ],
        ]

        tabela_resumo = Table(
            resumo_dados,
            colWidths=[
                50 * mm,
                50 * mm,
                50 * mm,
                55 * mm,
            ],
            rowHeights=[
                8 * mm,
                11 * mm,
            ],
        )

        tabela_resumo.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    self.COR_FUNDO_RESUMO,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    self.COR_LINHA,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    self.COR_LINHA,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ])
        )

        elementos.append(tabela_resumo)

        elementos.append(
            Spacer(1, 7 * mm)
        )

        # ======================================================
        # TABELA DE COLETAS
        # ======================================================

        registros = dados.get("registros", [])

        if registros:
            cabecalho = [
                "Data",
                "Código",
                "Solicitante",
                "Bairro",
                "Forma",
                "Quantidade",
                "Peso (kg)",
            ]

            linhas = [cabecalho]

            for registro in registros:
                linhas.append([
                    Paragraph(
                        self._formatar_data(
                            registro.get("data_hora_conclusao")
                        ),
                        self.estilo_tabela,
                    ),
                    Paragraph(
                        str(registro.get("codigo") or "-"),
                        self.estilo_tabela,
                    ),
                    Paragraph(
                        str(registro.get("solicitante") or "-"),
                        self.estilo_tabela,
                    ),
                    Paragraph(
                        str(registro.get("bairro") or "-"),
                        self.estilo_tabela,
                    ),
                    Paragraph(
                        str(
                            registro.get("forma_acondicionamento")
                            or "-"
                        ),
                        self.estilo_tabela,
                    ),
                    Paragraph(
                        self._formatar_numero(
                            registro.get("quantidade_sacas_coletada")
                            or 0
                        ),
                        self.estilo_tabela_direita,
                    ),
                    Paragraph(
                        self._formatar_peso(
                            registro.get("quantidade_kg_coletado")
                            or 0
                        ),
                        self.estilo_tabela_direita,
                    ),
                ])

            tabela = Table(
                linhas,
                repeatRows=1,
                colWidths=[
                    24 * mm,
                    28 * mm,
                    65 * mm,
                    42 * mm,
                    27 * mm,
                    27 * mm,
                    32 * mm,
                ],
            )

            tabela.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        self.COR_PRINCIPAL,
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, 0),
                        8,
                    ),
                    (
                        "ALIGN",
                        (5, 0),
                        (-1, 0),
                        "RIGHT",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, 0),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 1),
                        (-1, -1),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 1),
                        (-1, -1),
                        5,
                    ),
                    (
                        "LINEBELOW",
                        (0, 1),
                        (-1, -1),
                        0.35,
                        self.COR_LINHA,
                    ),
                ])
            )

            elementos.append(tabela)
        else:
            aviso = Table(
                [[
                    Paragraph(
                        "Nenhuma coleta concluída foi encontrada "
                        "para os filtros selecionados.",
                        self.estilo_sem_registros,
                    )
                ]],
                colWidths=[245 * mm],
            )

            aviso.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        self.COR_FUNDO_RESUMO,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        self.COR_LINHA,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                ])
            )

            elementos.append(aviso)

        elementos.append(
            Spacer(1, 7 * mm)
        )

        # ======================================================
        # EMISSÃO
        # ======================================================

        agora = datetime.now().strftime(
            "%d/%m/%Y às %H:%M"
        )

        elementos.append(
            Paragraph(
                f"Relatório emitido em {agora}.",
                self.estilo_filtro,
            )
        )

        documento.build(
            elementos,
            onFirstPage=self._desenhar_cabecalho_rodape,
            onLaterPages=self._desenhar_cabecalho_rodape,
        )

        return caminho