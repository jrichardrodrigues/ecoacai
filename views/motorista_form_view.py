from collections.abc import Callable

import flet as ft

from components.buttons import (
    PrimaryButton,
    SecondaryButton,
)
from components.fields import (
    NameField,
    PhoneField,
)
from components.layout import PageHeader
from components.theme import (
    Radius,
    Spacing,
)
from config.ui_texts import (
    MotoristaTexts,
    UITexts,
)
from controllers import MotoristaController
from models import Motorista
from utils.messages import (
    mostrar_erro,
    mostrar_sucesso,
)


class MotoristaFormView:
    """Tela de cadastro e edição de motoristas."""

    def __init__(
        self,
        page: ft.Page,
        on_salvar_sucesso: Callable[[], None] | None = None,
        motorista: Motorista | None = None,
    ) -> None:
        self.page = page
        self.on_salvar_sucesso = on_salvar_sucesso

        self.motorista = motorista
        self.modo_edicao = motorista is not None

        self.controller = MotoristaController()

        ignorar_id = (
            motorista.id
            if motorista is not None
            and motorista.id is not None
            else 0
        )

        # --------------------------------------------------
        # Nome
        # --------------------------------------------------

        self.nome = NameField()
        self.nome.container.expand = True

        # --------------------------------------------------
        # Telefone celular
        # --------------------------------------------------

        self.telefone = PhoneField(
            usuario_service=self.controller.service,
            ignorar_id=ignorar_id,
        )

        self.telefone.container.expand = True

        # --------------------------------------------------
        # CNH
        # --------------------------------------------------

        self.cnh = ft.TextField(
            label="CNH",
            hint_text="Informe o número da CNH",
            expand=True,
            border_radius=Radius.INPUT,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )

        # --------------------------------------------------
        # Categoria da CNH
        # --------------------------------------------------

        self.categoria_cnh = ft.Dropdown(
            label="Categoria da CNH",
            hint_text="Selecione a categoria",
            expand=True,
            border_radius=Radius.INPUT,
            options=[
                ft.dropdown.Option("A"),
                ft.dropdown.Option("B"),
                ft.dropdown.Option("C"),
                ft.dropdown.Option("D"),
                ft.dropdown.Option("E"),
                ft.dropdown.Option("AB"),
                ft.dropdown.Option("AC"),
                ft.dropdown.Option("AD"),
                ft.dropdown.Option("AE"),
            ],
        )

        # --------------------------------------------------
        # Situação
        # --------------------------------------------------

        self.ativo = ft.Switch(
            label="Motorista ativo",
            value=True,
        )

        self.preencher_campos()

    # ======================================================
    # PREENCHIMENTO
    # ======================================================

    def preencher_campos(self) -> None:
        """Preenche o formulário durante a edição."""

        if self.motorista is None:
            return

        self.nome.value = self.motorista.nome
        self.telefone.value = self.motorista.telefone
        self.cnh.value = self.motorista.cnh
        self.categoria_cnh.value = (
            self.motorista.categoria_cnh
        )
        self.ativo.value = self.motorista.ativo

    # ======================================================
    # VALIDAÇÃO
    # ======================================================

    def validar_formulario(self) -> bool:
        """Valida os campos específicos do formulário."""

        formulario_valido = True

        cnh = str(
            self.cnh.value or "",
        ).strip()

        categoria_cnh = str(
            self.categoria_cnh.value or "",
        ).strip()

        self.cnh.error_text = None
        self.categoria_cnh.error_text = None

        if not cnh:
            self.cnh.error_text = (
                "A CNH do motorista é obrigatória."
            )
            formulario_valido = False

        if not categoria_cnh:
            self.categoria_cnh.error_text = (
                "Selecione a categoria da CNH."
            )
            formulario_valido = False

        if not formulario_valido:
            self.page.update()

        return formulario_valido

    # ======================================================
    # CONVERSÃO
    # ======================================================

    def obter_motorista(self) -> Motorista:
        """Cria um Motorista com os dados do formulário."""

        return Motorista(
            id=(
                self.motorista.id
                if self.motorista is not None
                else None
            ),
            nome=str(
                self.nome.value or "",
            ).strip(),
            telefone=str(
                self.telefone.value or "",
            ).strip(),
            cnh=str(
                self.cnh.value or "",
            ).strip(),
            categoria_cnh=str(
                self.categoria_cnh.value or "",
            ).strip(),
            ativo=bool(
                self.ativo.value,
            ),
        )

    # ======================================================
    # LIMPEZA
    # ======================================================

    def limpar_campos(
        self,
        e: ft.ControlEvent | None = None,
    ) -> None:
        """Limpa os campos do formulário."""

        self.nome.limpar()
        self.telefone.limpar()

        self.cnh.value = ""
        self.cnh.error_text = None

        self.categoria_cnh.value = None
        self.categoria_cnh.error_text = None

        self.ativo.value = True

        self.page.update()

    # ======================================================
    # SALVAMENTO
    # ======================================================

    def salvar(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Cadastra ou atualiza um motorista."""

        if not self.validar_formulario():
            mostrar_erro(
                self.page,
                "Verifique os campos obrigatórios.",
            )
            return

        motorista = self.obter_motorista()

        if self.modo_edicao:
            sucesso, mensagem = (
                self.controller.atualizar(
                    motorista,
                )
            )
        else:
            sucesso, mensagem = (
                self.controller.cadastrar(
                    motorista,
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

    # ======================================================
    # CONSTRUÇÃO DA INTERFACE
    # ======================================================

    def construir(
        self,
    ) -> ft.Control:
        """Constrói o formulário de cadastro ou edição."""

        titulo = (
            MotoristaTexts.TITULO_EDICAO
            if self.modo_edicao
            else MotoristaTexts.TITULO_CADASTRO
        )

        subtitulo = (
            MotoristaTexts.SUBTITULO_EDICAO
            if self.modo_edicao
            else MotoristaTexts.SUBTITULO_CADASTRO
        )

        texto_botao = (
            UITexts.BOTAO_ATUALIZAR
            if self.modo_edicao
            else UITexts.BOTAO_SALVAR
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
                        self.telefone.container,
                    ],
                ),

                ft.Row(
                    controls=[
                        self.cnh,
                        self.categoria_cnh,
                    ],
                    spacing=Spacing.MD,
                ),

                ft.Row(
                    controls=[
                        self.ativo,
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
                ),
            ],
            spacing=Spacing.MD,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )