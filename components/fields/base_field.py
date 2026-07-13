import flet as ft


class BaseField:
    """Classe base para os campos reutilizáveis da aplicação."""

    def __init__(self, label: str, **kwargs):
        self.control = ft.TextField(
            label=label,
            expand=True,
            border_radius=10,
            **kwargs,
        )

    @property
    def value(self) -> str:
        return self.control.value or ""

    @value.setter
    def value(self, valor: str):
        self.control.value = valor or ""

    def mostrar_erro(self, mensagem: str):
        self.control.error_text = mensagem
        self.control.helper_text = None

    def mostrar_sucesso(self, mensagem: str):
        self.control.error_text = None
        self.control.helper_text = mensagem

    def limpar_mensagem(self):
        self.control.error_text = None
        self.control.helper_text = None

    def limpar(self):
        self.value = ""
        self.limpar_mensagem()

    def habilitar(self):
        self.control.disabled = False

    def desabilitar(self):
        self.control.disabled = True