import flet as ft

from .base_field import BaseField


class BaseValidatedField(BaseField):
    """Campo reutilizável com uma mensagem de validação visível."""

    def __init__(self, label: str, **kwargs):
        super().__init__(label=label, **kwargs)

        self.mensagem = ft.Text(
            value="",
            size=12,
            visible=False,
        )

        # O componente completo passa a ser uma coluna:
        # TextField + mensagem de validação.
        self.container = ft.Column(
            controls=[
                self.control,
                self.mensagem,
            ],
            spacing=2,
        )

        self.control.on_change = self._ao_alterar
        self.control.on_blur = self._ao_sair

    def _ao_alterar(self, e):
        self.value = e.control.value or ""
        self.validar()
        self._atualizar()

    def _ao_sair(self, e):
        self.value = e.control.value or ""
        self.validar()
        self._atualizar()

    def _atualizar(self):
        try:
            self.container.update()
        except RuntimeError:
            # Pode ocorrer antes de o componente ser adicionado à página.
            pass

    def validar(self):
        raise NotImplementedError(
            "A classe filha deve implementar o método validar()."
        )

    def erro(self, mensagem: str):
        self.control.error_text = None
        self.control.helper_text = None

        self.mensagem.value = mensagem
        self.mensagem.color = ft.Colors.RED
        self.mensagem.visible = True

    def sucesso(self, mensagem: str):
        self.control.error_text = None
        self.control.helper_text = None

        self.mensagem.value = mensagem
        self.mensagem.color = ft.Colors.GREEN
        self.mensagem.visible = True

    def limpar_mensagem(self):
        self.control.error_text = None
        self.control.helper_text = None

        self.mensagem.value = ""
        self.mensagem.visible = False

    def limpar(self):
        self.value = ""
        self.limpar_mensagem()