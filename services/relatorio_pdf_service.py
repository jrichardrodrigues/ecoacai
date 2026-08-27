from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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


class RelatorioPdfService:
    """Serviço responsável pela geração do relatório de coletas em PDF."""

    COR_PRIMARIA = colors.HexColor("#851747")
    COR_TEXTO = colors.HexColor("#2F242A")
    COR_TEXTO_SECUNDARIO = colors.HexColor("#6F666B")
    COR_BORDA = colors.HexColor("#D9D4D7")
    COR_FUNDO_CABECALHO = colors.HexColor("#F2EEF0")

    def gerar_relatorio_coletas(
            self,
            *,
            caminho_arquivo: str | Path,
            setor: str,
            bairro: str,
            data_inicial: str | None,
            data_final: str | None,
            resumo: dict,
            registros: list[dict],
    ) -> Path:
        """
        Gera o relatório de coletas em formato PDF.

        O relatório contém:
        - filtros utilizados;
        - resumo da operação;
        - detalhamento completo das coletas.
        """

        caminho = Path(caminho_arquivo)

        caminho.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        documento = SimpleDocTemplate(
            str(caminho),
            pagesize=landscape(A4),
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=18 * mm,
            title="Relatório de Coletas - ZELURBIS",
            author="ZELURBIS",
        )

        estilos = getSampleStyleSheet()

        estilo_marca = ParagraphStyle(
            "MarcaZelurbis",
            parent=estilos["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=self.COR_PRIMARIA,
            alignment=TA_LEFT,
            spaceAfter=4,
        )

        estilo_titulo = ParagraphStyle(
            "TituloRelatorio",
            parent=estilos["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=self.COR_TEXTO,
            alignment=TA_LEFT,
            spaceAfter=5,
        )

        estilo_subtitulo = ParagraphStyle(
            "SubtituloRelatorio",
            parent=estilos["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=self.COR_TEXTO_SECUNDARIO,
            alignment=TA_LEFT,
        )

        estilo_secao = ParagraphStyle(
            "SecaoRelatorio",
            parent=estilos["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=self.COR_TEXTO,
            alignment=TA_LEFT,
            spaceAfter=7,
        )

        estilo_celula = ParagraphStyle(
            "CelulaRelatorio",
            parent=estilos["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=self.COR_TEXTO,
        )

        estilo_celula_centro = ParagraphStyle(
            "CelulaRelatorioCentro",
            parent=estilo_celula,
            alignment=TA_CENTER,
        )

        estilo_assinatura = ParagraphStyle(
            "AssinaturaZelurbis",
            parent=estilos["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=self.COR_TEXTO_SECUNDARIO,
            alignment=TA_LEFT,
            spaceAfter=5,
        )

        elementos = []

        elementos.append(
            Paragraph(
                "ZELURBIS",
                estilo_marca,
            )
        )

        elementos.append(
            Paragraph(
                "Gestão Ambiental Urbana",
                estilo_assinatura,
            )
        )

        elementos.append(
            Paragraph(
                "Relatório de Coletas",
                estilo_titulo,
            )
        )

        elementos.append(
            Paragraph(
                self._criar_descricao_filtros(
                    setor=setor,
                    bairro=bairro,
                    data_inicial=data_inicial,
                    data_final=data_final,
                ),
                estilo_subtitulo,
            )
        )

        elementos.append(
            Spacer(
                1,
                7 * mm,
            )
        )

        elementos.append(
            Paragraph(
                "Resumo das Coletas",
                estilo_secao,
            )
        )

        tabela_resumo = self._criar_tabela_resumo(
            resumo=resumo,
            estilo_celula=estilo_celula,
        )

        elementos.append(tabela_resumo)

        elementos.append(
            Spacer(
                1,
                8 * mm,
            )
        )

        elementos.append(
            Paragraph(
                "Detalhamento das Coletas",
                estilo_secao,
            )
        )

        tabela_detalhamento = (
            self._criar_tabela_detalhamento(
                registros=registros,
                estilo_celula=estilo_celula,
                estilo_celula_centro=estilo_celula_centro,
            )
        )

        elementos.append(
            tabela_detalhamento
        )

        documento.build(
            elementos,
            onFirstPage=self._adicionar_rodape,
            onLaterPages=self._adicionar_rodape,
        )

        return caminho

    def _criar_descricao_filtros(
            self,
            *,
            setor: str,
            bairro: str,
            data_inicial: str | None,
            data_final: str | None,
    ) -> str:

        setor_texto = (
            str(setor or "").strip()
            or "Todos os setores"
        )

        bairro_texto = (
            str(bairro or "").strip()
            or "Todos os bairros"
        )

        if bairro_texto.upper() == "TODOS":
            bairro_texto = "Todos os bairros"

        data_inicial_texto = str(
            data_inicial or ""
        ).strip()

        data_final_texto = str(
            data_final or ""
        ).strip()

        if (
                data_inicial_texto
                and data_final_texto
        ):
            periodo = (
                f"Período: "
                f"{data_inicial_texto} "
                f"a {data_final_texto}"
            )

        elif data_inicial_texto:
            periodo = (
                f"A partir de "
                f"{data_inicial_texto}"
            )

        elif data_final_texto:
            periodo = (
                f"Até {data_final_texto}"
            )

        else:
            periodo = "Todo o período"

        return (
            f"{setor_texto}"
            f" &nbsp;&nbsp;•&nbsp;&nbsp; "
            f"{bairro_texto}"
            f" &nbsp;&nbsp;•&nbsp;&nbsp; "
            f"{periodo}"
        )

    def _criar_tabela_resumo(
            self,
            *,
            resumo: dict,
            estilo_celula: ParagraphStyle,
    ) -> Table:

        total_coletas = int(
            resumo.get(
                "total_coletas",
                0,
            )
        )

        total_sacas = int(
            resumo.get(
                "total_sacas",
                0,
            )
        )

        total_bags = int(
            resumo.get(
                "total_bags",
                0,
            )
        )

        total_kg = float(
            resumo.get(
                "total_kg",
                0,
            )
        )

        peso_formatado = (
            f"{total_kg:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        dados = [
            [
                Paragraph(
                    "<b>Coletas realizadas</b>",
                    estilo_celula,
                ),
                Paragraph(
                    "<b>Sacas coletadas</b>",
                    estilo_celula,
                ),
                Paragraph(
                    "<b>Bags coletados</b>",
                    estilo_celula,
                ),
                Paragraph(
                    "<b>Peso total</b>",
                    estilo_celula,
                ),
            ],
            [
                Paragraph(
                    str(total_coletas),
                    estilo_celula,
                ),
                Paragraph(
                    str(total_sacas),
                    estilo_celula,
                ),
                Paragraph(
                    str(total_bags),
                    estilo_celula,
                ),
                Paragraph(
                    f"{peso_formatado} kg",
                    estilo_celula,
                ),
            ],
        ]

        tabela = Table(
            dados,
            colWidths=[
                58 * mm,
                58 * mm,
                58 * mm,
                58 * mm,
            ],
        )

        tabela.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        self.COR_FUNDO_CABECALHO,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        self.COR_BORDA,
                    ),
                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        self.COR_BORDA,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        return tabela

    def _criar_tabela_detalhamento(
            self,
            *,
            registros: list[dict],
            estilo_celula: ParagraphStyle,
            estilo_celula_centro: ParagraphStyle,
    ) -> Table:

        dados = [
            [
                Paragraph(
                    "<b>Código</b>",
                    estilo_celula,
                ),
                Paragraph(
                    "<b>Solicitante</b>",
                    estilo_celula,
                ),
                Paragraph(
                    "<b>Bairro</b>",
                    estilo_celula,
                ),
                Paragraph(
                    "<b>Acondicionamento</b>",
                    estilo_celula,
                ),
                Paragraph(
                    "<b>Quantidade</b>",
                    estilo_celula_centro,
                ),
                Paragraph(
                    "<b>Peso coletado</b>",
                    estilo_celula_centro,
                ),
                Paragraph(
                    "<b>Conclusão</b>",
                    estilo_celula,
                ),
            ]
        ]

        for registro in registros:
            codigo = str(
                registro.get("codigo")
                or ""
            )

            solicitante = str(
                registro.get("solicitante")
                or ""
            )

            bairro = str(
                registro.get("bairro")
                or ""
            )

            forma = str(
                registro.get(
                    "forma_acondicionamento"
                )
                or ""
            ).strip().upper()

            quantidade = int(
                registro.get(
                    "quantidade_sacas_coletada"
                )
                or 0
            )

            peso = float(
                registro.get(
                    "quantidade_kg_coletado"
                )
                or 0
            )

            peso_formatado = (
                f"{peso:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            data_conclusao = self._formatar_data_hora(
                registro.get(
                    "data_hora_conclusao"
                )
            )

            dados.append(
                [
                    Paragraph(
                        codigo,
                        estilo_celula,
                    ),
                    Paragraph(
                        solicitante,
                        estilo_celula,
                    ),
                    Paragraph(
                        bairro,
                        estilo_celula,
                    ),
                    Paragraph(
                        forma,
                        estilo_celula,
                    ),
                    Paragraph(
                        str(quantidade),
                        estilo_celula_centro,
                    ),
                    Paragraph(
                        f"{peso_formatado} kg",
                        estilo_celula_centro,
                    ),
                    Paragraph(
                        data_conclusao,
                        estilo_celula,
                    ),
                ]
            )

        tabela = Table(
            dados,
            repeatRows=1,
            colWidths=[
                25 * mm,
                57 * mm,
                30 * mm,
                40 * mm,
                27 * mm,
                36 * mm,
                42 * mm,
            ],
        )

        tabela.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        self.COR_FUNDO_CABECALHO,
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        self.COR_TEXTO,
                    ),
                    (
                        "LINEBELOW",
                        (0, 0),
                        (-1, 0),
                        0.7,
                        self.COR_BORDA,
                    ),
                    (
                        "LINEBELOW",
                        (0, 1),
                        (-1, -1),
                        0.4,
                        self.COR_BORDA,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        return tabela

    @staticmethod
    def _formatar_data_hora(
            valor: object,
    ) -> str:

        texto = str(
            valor or ""
        ).strip()

        if not texto:
            return ""

        try:
            return datetime.fromisoformat(
                texto
            ).strftime(
                "%d/%m/%Y %H:%M"
            )

        except ValueError:
            return texto

    def _adicionar_rodape(
            self,
            canvas,
            documento,
    ) -> None:

        canvas.saveState()

        largura_pagina, _ = landscape(A4)

        agora = datetime.now().strftime(
            "%d/%m/%Y às %H:%M"
        )

        canvas.setStrokeColor(
            self.COR_BORDA
        )

        canvas.setLineWidth(0.5)

        canvas.line(
            15 * mm,
            12 * mm,
            largura_pagina - 15 * mm,
            12 * mm,
        )

        canvas.setFont(
            "Helvetica",
            7,
        )

        canvas.setFillColor(
            self.COR_TEXTO_SECUNDARIO
        )

        canvas.drawString(
            15 * mm,
            7 * mm,
            f"ZELURBIS • Relatório gerado em {agora}",
        )

        canvas.drawRightString(
            largura_pagina - 15 * mm,
            7 * mm,
            f"Página {documento.page}",
        )

        canvas.restoreState()