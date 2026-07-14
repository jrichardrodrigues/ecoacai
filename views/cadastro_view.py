import flet as ft

from components.fields import (
    CpfField,
    EmailField,
    NameField,
    PhoneField,
)
from config import COR_SUCESSO, SETORES
from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from utils.messages import mostrar_erro, mostrar_sucesso


class CadastroView:
    """Tela de cadastro de estabelecimentos e responsáveis."""

    def __init__(
            self,
            page: ft.Page,
            on_salvar_sucesso=None,
    ) -> None:
        self.page = page
        self.on_salvar_sucesso = on_salvar_sucesso
        self.controller = EstabelecimentoController()

        # Campos inteligentes reutilizáveis
        self.nome = NameField()

        self.cpf = CpfField(
            usuario_service=(
                self.controller.estabelecimento_service
            ),
        )

        self.email = EmailField(
            usuario_service=(
                self.controller.estabelecimento_service
            ),
        )

        self.celular = PhoneField(
            usuario_service=(
                self.controller.estabelecimento_service
            ),
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

    def obter_dados(self) -> dict[str, str | None]:
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

    def limpar_campos(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
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

    def salvar(self, e: ft.ControlEvent) -> None:
        """Envia os dados preenchidos para o controller."""

        dados = self.obter_dados()

        sucesso, mensagem = (
            self.controller.cadastrar_estabelecimento(
                dados,
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

        self.limpar_campos()

        if self.on_salvar_sucesso:
            self.on_salvar_sucesso()

    def construir(self) -> ft.Control:
        """Constrói e retorna o conteúdo visual da tela."""

        return ft.Column(
            controls=[
                ft.Text(
                    "Cadastro de Estabelecimentos",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Preencha os dados do estabelecimento "
                    "ou responsável.",
                    size=15,
                ),
                ft.Divider(),

                ft.Row(
                    controls=[
                        self.nome.container,
                    ],
                ),

                ft.Row(
                    controls=[
                        self.cpf.container,
                        self.email.container,
                    ],
                    spacing=15,
                ),

                ft.Row(
                    controls=[
                        self.celular.container,
                    ],
                ),

                ft.Row(
                    controls=[
                        self.endereco,
                        self.bairro,
                    ],
                    spacing=15,
                ),

                ft.Row(
                    controls=[
                        self.setor,
                    ],
                ),

                ft.Divider(),

                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            content="Salvar cadastro",
                            icon=ft.Icons.SAVE,
                            bgcolor=COR_SUCESSO,
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