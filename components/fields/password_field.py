import re

import flet as ft

from components.theme import Colors, Radius, Spacing
from services import PasswordService

from .base_validated_field import BaseValidatedField


class PasswordField(BaseValidatedField):
    """Campo inteligente de senha do EcoAçaí."""

    def __init__(
        self,
        label: str = "Senha",
        mostrar_requisitos: bool = True,
    ):
        super().__init__(
            label=label,
            hint_text="Digite sua senha",
            password=True,
            can_reveal_password=True,
            max_length=128,
        )

        self.password_service = PasswordService()
        self.mostrar_requisitos = mostrar_requisitos

        self.barra_forca = ft.ProgressBar(
            value=0,
            height=6,
            color=Colors.ERROR,
            bgcolor=Colors.BORDER,
            border_radius=Radius.SM,
            visible=False,
        )

        self.texto_forca = ft.Text(
            value="",
            size=12,
            color=Colors.TEXT_SECONDARY,
            visible=False,
        )

        self.requisito_tamanho = self._criar_requisito(
            "Pelo menos 9 caracteres"
        )
        self.requisito_maiuscula = self._criar_requisito(
            "Uma letra maiúscula"
        )
        self.requisito_minuscula = self._criar_requisito(
            "Uma letra minúscula"
        )
        self.requisito_numero = self._criar_requisito(
            "Um número"
        )
        self.requisito_especial = self._criar_requisito(
            "Um caractere especial"
        )
        self.requisito_espacos = self._criar_requisito(
            "Sem espaços"
        )

        self.requisitos = ft.Column(
            controls=[
                self.requisito_tamanho,
                self.requisito_maiuscula,
                self.requisito_minuscula,
                self.requisito_numero,
                self.requisito_especial,
                self.requisito_espacos,
            ],
            spacing=Spacing.XS,
            visible=False,
        )

        # Substitui a estrutura padrão do BaseValidatedField.
        self.container.controls = [
            self.control,
            self.barra_forca,
            self.texto_forca,
            self.requisitos,
            self.mensagem,
        ]

    @staticmethod
    def _criar_requisito(texto: str) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.CLOSE,
                    size=16,
                    color=Colors.TEXT_SECONDARY,
                ),
                ft.Text(
                    texto,
                    size=12,
                    color=Colors.TEXT_SECONDARY,
                ),
            ],
            spacing=Spacing.XS,
        )

    @staticmethod
    def _atualizar_requisito(
        requisito: ft.Row,
        atendido: bool,
    ):
        icone = requisito.controls[0]
        texto = requisito.controls[1]

        if atendido:
            icone.name = ft.Icons.CHECK_CIRCLE
            icone.color = Colors.SUCCESS
            texto.color = Colors.SUCCESS
        else:
            icone.name = ft.Icons.CANCEL
            icone.color = Colors.ERROR
            texto.color = Colors.ERROR

    def validar(self):
        senha = self.value

        if not senha:
            self.barra_forca.visible = False
            self.texto_forca.visible = False
            self.requisitos.visible = False
            self.limpar_mensagem()
            return

        tamanho_ok = len(senha) >= 9
        maiuscula_ok = bool(re.search(r"[A-Z]", senha))
        minuscula_ok = bool(re.search(r"[a-z]", senha))
        numero_ok = bool(re.search(r"\d", senha))
        especial_ok = bool(re.search(r"[^A-Za-z0-9]", senha))
        espacos_ok = not any(
            caractere.isspace()
            for caractere in senha
        )

        self._atualizar_requisito(
            self.requisito_tamanho,
            tamanho_ok,
        )
        self._atualizar_requisito(
            self.requisito_maiuscula,
            maiuscula_ok,
        )
        self._atualizar_requisito(
            self.requisito_minuscula,
            minuscula_ok,
        )
        self._atualizar_requisito(
            self.requisito_numero,
            numero_ok,
        )
        self._atualizar_requisito(
            self.requisito_especial,
            especial_ok,
        )
        self._atualizar_requisito(
            self.requisito_espacos,
            espacos_ok,
        )

        if self.mostrar_requisitos:
            self.requisitos.visible = True

        total_atendidos = sum(
            [
                tamanho_ok,
                maiuscula_ok,
                minuscula_ok,
                numero_ok,
                especial_ok,
                espacos_ok,
            ]
        )

        self._atualizar_forca(total_atendidos)

        valida, mensagem = (
            self.password_service.validar_regra(senha)
        )

        if not valida:
            self.erro(mensagem)
            return

        self.sucesso("Senha válida.")

    def _atualizar_forca(self, total_atendidos: int):
        self.barra_forca.visible = True
        self.texto_forca.visible = True

        percentual = total_atendidos / 6
        self.barra_forca.value = percentual

        if total_atendidos <= 2:
            self.barra_forca.color = Colors.ERROR
            self.texto_forca.value = "Força da senha: fraca"
            self.texto_forca.color = Colors.ERROR

        elif total_atendidos <= 4:
            self.barra_forca.color = Colors.WARNING
            self.texto_forca.value = "Força da senha: média"
            self.texto_forca.color = Colors.WARNING

        elif total_atendidos == 5:
            self.barra_forca.color = Colors.PRIMARY_LIGHT
            self.texto_forca.value = "Força da senha: boa"
            self.texto_forca.color = Colors.PRIMARY_LIGHT

        else:
            self.barra_forca.color = Colors.SUCCESS
            self.texto_forca.value = "Força da senha: forte"
            self.texto_forca.color = Colors.SUCCESS