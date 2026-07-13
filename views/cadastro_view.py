import flet as ft

from components.fields import (
    CpfField,
    EmailField,
    NameField,
    PhoneField,
)
from config import SETORES
from controllers.usuario_controller import UsuarioController
from utils.messages import mostrar_erro, mostrar_sucesso


class CadastroView:
    """Tela de cadastro de estabelecimentos e responsáveis."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = UsuarioController()

        # Campos inteligentes reutilizáveis
        self.nome = NameField()

        self.cpf = CpfField(
            usuario_service=self.controller.usuario_service,
        )

        self.email = EmailField(
            usuario_service=self.controller.usuario_service,
        )

        self.celular = PhoneField(
            usuario_service=self.controller.usuario_service,
        )

        # Campos simples
        self.endereco = ft.TextField(
            label="Endereço",
            hint_text="Rua, travessa, avenida e número",
            expand=True,
            border_radius=10,
        )

        self.bairro = ft.TextField(
            label="Bairro",
            hint_text="Informe o bairro",
            expand=True,
            border_radius=10,
        )

        self.setor = ft.Dropdown(
            label="Setor de recolhimento",
            hint_text="Selecione o setor",
            expand=True,
            border_radius=10,
            options=[
                ft.dropdown.Option(setor)
                for setor in SETORES
            ],
        )

        # Faz os componentes compostos ocuparem o espaço disponível.
        self.nome.container.expand = True
        self.cpf.container.expand = True
        self.email.container.expand = True
        self.celular.container.expand = True

    def obter_dados(self) -> dict:
        """Reúne os valores preenchidos no formulário."""

        return {
            "nome": self.nome.value,
            "cpf": self.cpf.value,
            "email": self.email.value,
            "celular": self.celular.value,
            "endereco": self.endereco.value,
            "bairro": self.bairro.value,
            "setor": self.setor.value,
        }

    def limpar_campos(self, e=None):
        """Limpa os campos e as mensagens de validação."""

        self.nome.limpar()
        self.cpf.limpar()
        self.email.limpar()
        self.celular.limpar()

        self.endereco.value = ""
        self.endereco.error_text = None

        self.bairro.value = ""
        self.bairro.error_text = None

        self.setor.value = None
        self.setor.error_text = None

        self.page.update()

    def salvar(self, e):
        """Envia os dados preenchidos para o controller."""

        dados = self.obter_dados()

        sucesso, mensagem = self.controller.cadastrar_usuario(dados)

        if not sucesso:
            mostrar_erro(self.page, mensagem)
            return

        mostrar_sucesso(self.page, mensagem)
        self.limpar_campos()

    def construir(self):
        return ft.Column(
            controls=[
                ft.Text(
                    "Cadastro de Estabelecimentos",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Preencha os dados do estabelecimento ou responsável.",
                    size=15,
                ),
                ft.Divider(),

                # Nome
                ft.Row(
                    controls=[
                        self.nome.container,
                    ],
                ),

                # CPF e e-mail
                ft.Row(
                    controls=[
                        self.cpf.container,
                        self.email.container,
                    ],
                    spacing=15,
                ),

                # Celular
                ft.Row(
                    controls=[
                        self.celular.container,
                    ],
                ),

                # Endereço e bairro
                ft.Row(
                    controls=[
                        self.endereco,
                        self.bairro,
                    ],
                    spacing=15,
                ),

                # Setor
                ft.Row(
                    controls=[
                        self.setor,
                    ],
                ),

                ft.Divider(),

                # Ações
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            content="Salvar cadastro",
                            icon=ft.Icons.SAVE,
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                            on_click=self.salvar,
                        ),
                        ft.ElevatedButton(
                            content="Limpar",
                            icon=ft.Icons.CLEAR,
                            on_click=self.limpar_campos,
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )