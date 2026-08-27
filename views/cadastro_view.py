from collections.abc import Callable

import flet as ft

from components.fields import (
    CpfField,
    EmailField,
    NameField,
    PhoneField,
)

from config.constants import BAIRROS_SETORES, SETORES

from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from models import Estabelecimento
from utils.messages import mostrar_erro, mostrar_sucesso
from components.theme import (
    Spacing,
    Radius,
)
from components.layout import PageHeader
from components.buttons import PrimaryButton, SecondaryButton


class CadastroView:
    """Tela de cadastro e edição de estabelecimentos."""

    def __init__(
        self,
        page: ft.Page,
        on_salvar_sucesso: Callable[[], None] | None = None,
        estabelecimento: Estabelecimento | None = None,
    ) -> None:
        self.page = page
        self.on_salvar_sucesso = on_salvar_sucesso
        self.estabelecimento = estabelecimento
        self.modo_edicao = estabelecimento is not None

        self.controller = EstabelecimentoController()

        ignorar_id = (
            estabelecimento.id
            if estabelecimento is not None
            and estabelecimento.id is not None
            else 0
        )

        self.nome = NameField()

        self.cpf = CpfField(
            usuario_service=self.controller.estabelecimento_service,
            ignorar_id=ignorar_id,
        )

        self.email = EmailField(
            usuario_service=self.controller.estabelecimento_service,
            ignorar_id=ignorar_id,
        )

        self.celular = PhoneField(
            usuario_service=self.controller.estabelecimento_service,
            ignorar_id=ignorar_id,
        )

        self.endereco = ft.TextField(
            label="Endereço",
            hint_text="Rua, Travessa, Avenida e Número",
            expand=True,
            border_radius=Radius.INPUT,
        )

        self.bairro = ft.Dropdown(
            label="Bairro",
            hint_text="Selecione o Bairro",
            expand=True,
            border_radius=Radius.INPUT,
            options=[
                ft.dropdown.Option(bairro)
                for bairro in sorted(
                    BAIRROS_SETORES.keys()
                )
            ],
        )

        self.bairro.on_select = (
            self._preencher_setor_por_bairro
        )

        self.setor = ft.TextField(
            label="Setor de recolhimento",
            hint_text="Definido automaticamente pelo Bairro",
            expand=True,
            border_radius=Radius.INPUT,
            read_only=True,
        )

        self.nome.container.expand = True
        self.cpf.container.expand = True
        self.email.container.expand = True
        self.celular.container.expand = True

        self.preencher_campos()

    def _preencher_setor_por_bairro(
            self,
            _e,
    ) -> None:
        bairro_informado = (
                self.bairro.value or ""
        ).strip()

        if not bairro_informado:
            self.setor.value = None
            self.setor.update()
            return

        bairro_normalizado = bairro_informado.casefold()

        setor_encontrado = next(
            (
                setor
                for bairro, setor in BAIRROS_SETORES.items()
                if bairro.casefold() == bairro_normalizado
            ),
            None,
        )

        self.setor.value = setor_encontrado
        self.setor.update()

    def preencher_campos(self) -> None:
        """Preenche o formulário no modo de edição."""

        if self.estabelecimento is None:
            return

        self.nome.value = self.estabelecimento.nome
        self.cpf.value = self.estabelecimento.cpf
        self.email.value = self.estabelecimento.email
        self.celular.value = self.estabelecimento.celular

        self.endereco.value = self.estabelecimento.endereco

        bairro = (self.estabelecimento.bairro or "").strip()

        if bairro in BAIRROS_SETORES:
            self.bairro.value = bairro
            self.setor.value = BAIRROS_SETORES[bairro]
        else:
            self.bairro.value = None
            self.setor.value = None

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
        """Cadastra ou atualiza o estabelecimento."""

        dados = self.obter_dados()

        if self.modo_edicao:
            if (
                self.estabelecimento is None
                or self.estabelecimento.id is None
            ):
                mostrar_erro(
                    self.page,
                    "Estabelecimento sem identificador.",
                )
                return

            sucesso, mensagem = (
                self.controller.atualizar_estabelecimento(
                    self.estabelecimento.id,
                    dados,
                )
            )
        else:
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

        if self.on_salvar_sucesso is not None:
            self.on_salvar_sucesso()
            return

        if not self.modo_edicao:
            self.limpar_campos()

    def construir(self) -> ft.Control:
        """Constrói o formulário de cadastro ou edição."""

        titulo = (
            "Editar Estabelecimento"
            if self.modo_edicao
            else "Cadastro de Estabelecimentos"
        )

        subtitulo = (
            "Altere os dados e clique em atualizar."
            if self.modo_edicao
            else (
                "Preencha os dados do estabelecimento "
                "ou responsável."
            )
        )

        texto_botao = (
            "Atualizar cadastro"
            if self.modo_edicao
            else "Salvar cadastro"
        )

        icone_botao = (
            ft.Icons.EDIT
            if self.modo_edicao
            else ft.Icons.SAVE
        )

        return ft.Column(
            controls=[
                PageHeader(
                    title=titulo,
                    subtitle=subtitulo,
                ),

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
                    spacing=Spacing.MD,
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
                    spacing=Spacing.MD,
                ),

                ft.Row(
                    controls=[
                        self.setor,
                    ],
                ),

                ft.Divider(),

                ft.Row(
                    controls=[
                        PrimaryButton(
                            label=texto_botao,
                            icon=icone_botao,
                            on_click=self.salvar,
                        ),
                        SecondaryButton(
                            label="Limpar",
                            icon=ft.Icons.CLEAR,
                            on_click=self.limpar_campos,
                        ),
                    ],
                    spacing=Spacing.SM,
                )
            ],
            spacing=Spacing.MD,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )