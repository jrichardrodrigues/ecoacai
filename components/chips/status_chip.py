from __future__ import annotations

import unicodedata

import flet as ft


class StatusChip(ft.Container):
    """Chip padronizado de status do ECOAÇAÍ."""

    CORES = {
        "success": (
            ft.Colors.GREEN_100,
            ft.Colors.GREEN_900,
        ),
        "warning": (
            ft.Colors.ORANGE_100,
            ft.Colors.ORANGE_900,
        ),
        "danger": (
            ft.Colors.RED_100,
            ft.Colors.RED_900,
        ),
        "info": (
            ft.Colors.BLUE_100,
            ft.Colors.BLUE_900,
        ),
        "neutral": (
            ft.Colors.GREY_200,
            ft.Colors.GREY_800,
        ),
    }

    STATUS_POR_CONTEXTO = {
        "veiculo": {
            "DISPONIVEL": "success",
            "EM_COLETA": "warning",
            "MANUTENCAO": "danger",
            "RESERVADO": "info",
            "INATIVO": "neutral",
        },
        "coleta": {
            "PENDENTE": "warning",
            "AGENDADA": "info",
            "EM_COLETA": "warning",
            "CONCLUIDA": "success",
            "CANCELADA": "danger",
        },
        "situacao": {
            "ATIVO": "success",
            "INATIVO": "neutral",
        },
    }

    def __init__(
        self,
        texto: str,
        tipo: str | None = None,
        contexto: str | None = None,
    ) -> None:
        status_normalizado = self._normalizar(
            texto
        )

        contexto_normalizado = self._normalizar(
            contexto or ""
        ).lower()

        if tipo is None:
            tipo = (
                self.STATUS_POR_CONTEXTO
                .get(
                    contexto_normalizado,
                    {},
                )
                .get(
                    status_normalizado,
                    "info",
                )
            )

        fundo, cor_texto = self.CORES.get(
            tipo,
            self.CORES["info"],
        )

        texto_formatado = self._formatar_texto(
            status_normalizado
        )

        super().__init__(
            bgcolor=fundo,
            border_radius=16,
            padding=ft.Padding(
                left=10,
                top=5,
                right=10,
                bottom=5,
            ),
            content=ft.Text(
                texto_formatado,
                size=12,
                weight=ft.FontWeight.W_600,
                color=cor_texto,
                no_wrap=True,
            ),
        )

    @staticmethod
    def _normalizar(
        valor: str,
    ) -> str:
        texto = str(
            valor or ""
        ).strip().upper()

        texto = unicodedata.normalize(
            "NFD",
            texto,
        )

        texto = "".join(
            caractere
            for caractere in texto
            if unicodedata.category(
                caractere
            ) != "Mn"
        )

        return texto.replace(
            " ",
            "_",
        )

    @staticmethod
    def _formatar_texto(
        status: str,
    ) -> str:
        textos = {
            "DISPONIVEL": "Disponível",
            "EM_COLETA": "Em coleta",
            "MANUTENCAO": "Manutenção",
            "RESERVADO": "Reservado",
            "ATIVO": "Ativo",
            "INATIVO": "Inativo",
            "PENDENTE": "Pendente",
            "AGENDADA": "Agendada",
            "CONCLUIDA": "Concluída",
            "CANCELADA": "Cancelada",
        }

        return textos.get(
            status,
            status.replace(
                "_",
                " ",
            ).title(),
        )