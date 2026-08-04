from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.buttons import PrimaryButton, SecondaryButton
from components.cards import FormCard
from components.fields import (
    CpfField,
    NameField,
    PasswordField,
    PhoneField,
)
from components.headers import PageHeader
from components.theme import Colors, Radius, Spacing
from controllers.usuario_controller import UsuarioController
from models import Usuario
from services.cep_service import CepService
from utils.messages import mostrar_erro, mostrar_sucesso


class CadastroUsuarioView:
    """Tela pública de criação de conta de usuário em duas etapas."""

    def __init__(
        self,
        page: ft.Page,
        on_voltar_login: Callable[[], None],
        on_cadastro_sucesso: Callable[[Usuario], None] | None = None,
        controller: UsuarioController | None = None,
    ) -> None:
        self.page = page
        self.controller = controller or UsuarioController()

        self._on_voltar_login = on_voltar_login
        self._on_cadastro_sucesso = on_cadastro_sucesso
        self._etapa_atual = 1

        self._construir_controles()
        self._construir_etapas()
        self._atualizar_etapa()

    def _construir_controles(self) -> None:
        """Cria os controles utilizados pelo formulário."""

        self.nome = NameField()
        self.cpf = CpfField(
            usuario_service=self.controller.usuario_service,
        )
        self.celular = PhoneField(
            usuario_service=self.controller.usuario_service,
        )
        self.senha = PasswordField(
            label="Senha",
            mostrar_requisitos=True,
        )
        self.confirmar_senha = PasswordField(
            label="Confirmar senha",
            mostrar_requisitos=False,
        )

        self.nome.container.width = 480
        self.cpf.container.width = 230
        self.celular.container.width = 230
        self.senha.container.width = 230
        self.confirmar_senha.container.width = 230

        self.cep = ft.TextField(
            label="CEP",
            hint_text="00000-000",
            width=210,
            border_radius=Radius.INPUT,
            on_blur=self._consultar_cep,
            on_submit=self._consultar_cep,
        )

        self.botao_buscar_cep = ft.IconButton(
            icon=ft.Icons.SEARCH,
            tooltip="Buscar CEP",
            on_click=self._consultar_cep,
        )

        self.indicador_cep = ft.ProgressRing(
            width=20,
            height=20,
            visible=False,
        )

        self.mensagem_cep = ft.Text(
            value="",
            size=12,
            visible=False,
        )

        self.logradouro = ft.TextField(
            label="Logradouro",
            width=480,
            read_only=True,
            border_radius=Radius.INPUT,
        )

        self.bairro = ft.TextField(
            label="Bairro",
            width=230,
            read_only=True,
            border_radius=Radius.INPUT,
        )

        self.cidade = ft.TextField(
            label="Cidade",
            width=170,
            read_only=True,
            border_radius=Radius.INPUT,
        )

        self.uf = ft.TextField(
            label="UF",
            width=60,
            read_only=True,
            border_radius=Radius.INPUT,
        )

        self.numero = ft.TextField(
            label="Número",
            width=140,
            border_radius=Radius.INPUT,
        )

        self.complemento = ft.TextField(
            label="Complemento",
            hint_text="Opcional",
            width=320,
            border_radius=Radius.INPUT,
        )

        self.indicador = ft.ProgressRing(
            width=22,
            height=22,
            visible=False,
        )

        self.botao_voltar_login = SecondaryButton(
            label="VOLTAR AO LOGIN",
            icon=ft.Icons.ARROW_BACK,
            on_click=self._voltar_ao_login,
        )

        self.botao_proximo = PrimaryButton(
            label="PRÓXIMO",
            icon=ft.Icons.ARROW_FORWARD,
            on_click=self._ir_para_endereco,
        )

        self.botao_voltar_dados = SecondaryButton(
            label="VOLTAR",
            icon=ft.Icons.ARROW_BACK,
            on_click=self._voltar_para_dados,
        )

        self.botao_criar_conta = PrimaryButton(
            label="CRIAR CONTA",
            icon=ft.Icons.PERSON_ADD_OUTLINED,
            on_click=self._criar_conta,
        )

        self.texto_etapa = ft.Text(
            value="Etapa 1 de 2",
            size=12,
            color=Colors.TEXT_SECONDARY,
        )

    def _construir_etapas(self) -> None:
        """Monta os conteúdos das duas etapas."""

        self.etapa_dados = ft.Column(
            controls=[
                PageHeader(
                    title="Criar conta",
                    subtitle=(
                        "Informe seus dados pessoais "
                        "e defina uma senha de acesso."
                    ),
                    icon=ft.Icons.PERSON_ADD_OUTLINED,
                ),
                self.texto_etapa,
                self.nome.container,
                ft.Row(
                    controls=[
                        self.cpf.container,
                        self.celular.container,
                    ],
                    spacing=Spacing.MD,
                    wrap=True,
                ),
                ft.Row(
                    controls=[
                        self.senha.container,
                        self.confirmar_senha.container,
                    ],
                    spacing=Spacing.MD,
                    wrap=True,
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        self.botao_voltar_login,
                        self.botao_proximo,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=Spacing.SM,
                ),
            ],
            spacing=Spacing.MD,
            tight=True,
        )

        self.etapa_endereco = ft.Column(
            controls=[
                PageHeader(
                    title="Endereço",
                    subtitle=(
                        "Informe o CEP para preencher "
                        "automaticamente o endereço."
                    ),
                    icon=ft.Icons.LOCATION_ON_OUTLINED,
                ),
                self.texto_etapa,
                ft.Row(
                    controls=[
                        self.cep,
                        self.botao_buscar_cep,
                        self.indicador_cep,
                    ],
                    spacing=Spacing.SM,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.mensagem_cep,
                self.logradouro,
                ft.Row(
                    controls=[
                        self.bairro,
                        self.cidade,
                        self.uf,
                    ],
                    spacing=Spacing.MD,
                    wrap=True,
                ),
                ft.Row(
                    controls=[
                        self.numero,
                        self.complemento,
                    ],
                    spacing=Spacing.MD,
                    wrap=True,
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        self.botao_voltar_dados,
                        self.indicador,
                        self.botao_criar_conta,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=Spacing.SM,
                ),
            ],
            spacing=Spacing.MD,
            tight=True,
            visible=False,
        )

    def construir(self) -> ft.Control:
        """Constrói e retorna a interface da tela."""

        card = FormCard(
            content=ft.Column(
                controls=[
                    self.etapa_dados,
                    self.etapa_endereco,
                ],
                spacing=0,
                tight=True,
            ),
            width=560,
        )

        return ft.Container(
            expand=True,
            bgcolor=Colors.BACKGROUND,
            alignment=ft.Alignment.CENTER,
            padding=20,
            content=card,
        )

    def build(self) -> ft.Control:
        """Mantém compatibilidade com locais que chamem build()."""

        return self.construir()

    def _ir_para_endereco(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        """Valida a primeira etapa e abre o formulário de endereço."""

        valido, mensagem = self._validar_dados_pessoais()

        if not valido:
            mostrar_erro(self.page, mensagem)
            return

        self._etapa_atual = 2
        self._atualizar_etapa()

        try:
            self.cep.focus()
        except RuntimeError:
            pass

    def _voltar_para_dados(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        """Retorna para a etapa de dados pessoais."""

        self._etapa_atual = 1
        self._atualizar_etapa()

    def _atualizar_etapa(self) -> None:
        """Atualiza a visibilidade dos conteúdos."""

        primeira_etapa = self._etapa_atual == 1

        self.etapa_dados.visible = primeira_etapa
        self.etapa_endereco.visible = not primeira_etapa
        self.texto_etapa.value = (
            "Etapa 1 de 2"
            if primeira_etapa
            else "Etapa 2 de 2"
        )
        self._atualizar_pagina()

    def _consultar_cep(
        self,
        _evento: ft.ControlEvent | None = None,
    ) -> None:
        """Consulta o CEP e preenche automaticamente o endereço."""

        cep = str(self.cep.value or "").strip()
        valido, mensagem = CepService.validar_formato(cep)

        if not valido:
            self._limpar_endereco_automatico()
            self._mostrar_mensagem_cep(mensagem, erro=True)
            return

        self.indicador_cep.visible = True
        self.botao_buscar_cep.disabled = True
        self._atualizar_pagina()

        try:
            sucesso, mensagem, endereco = CepService.consultar(cep)
        finally:
            self.indicador_cep.visible = False
            self.botao_buscar_cep.disabled = False

        if not sucesso:
            self._limpar_endereco_automatico()
            self._mostrar_mensagem_cep(mensagem, erro=True)
            return

        self.cep.value = endereco.get(
            "cep",
            CepService.formatar(cep),
        )
        self.logradouro.value = endereco.get("logradouro", "")
        self.bairro.value = endereco.get("bairro", "")
        self.cidade.value = endereco.get("cidade", "")
        self.uf.value = endereco.get("uf", "")

        complemento_api = endereco.get("complemento", "")
        if complemento_api and not self.complemento.value:
            self.complemento.value = complemento_api

        self._mostrar_mensagem_cep(mensagem, erro=False)
        self._atualizar_pagina()

        try:
            self.numero.focus()
        except RuntimeError:
            pass

    def _mostrar_mensagem_cep(
        self,
        mensagem: str,
        *,
        erro: bool,
    ) -> None:
        """Exibe o retorno da consulta do CEP."""

        self.mensagem_cep.value = mensagem
        self.mensagem_cep.color = (
            ft.Colors.RED
            if erro
            else ft.Colors.GREEN
        )
        self.mensagem_cep.visible = True
        self._atualizar_pagina()

    def _limpar_endereco_automatico(self) -> None:
        """Limpa os campos preenchidos pela consulta do CEP."""

        self.logradouro.value = ""
        self.bairro.value = ""
        self.cidade.value = ""
        self.uf.value = ""

    def _criar_conta(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        """Valida os dados e solicita o cadastro do usuário."""

        valido, mensagem = self._validar_endereco()

        if not valido:
            mostrar_erro(self.page, mensagem)
            return

        dados = self._obter_dados()
        self._definir_carregamento(True)

        try:
            sucesso, mensagem, usuario = (
                self.controller.cadastrar_usuario(dados)
            )
        finally:
            self._definir_carregamento(False)

        if not sucesso or usuario is None:
            mostrar_erro(self.page, mensagem)
            return

        mostrar_sucesso(self.page, mensagem)

        if self._on_cadastro_sucesso is not None:
            self._on_cadastro_sucesso(usuario)
            return

        self._on_voltar_login()

    def _voltar_ao_login(
        self,
        _evento: ft.ControlEvent | None = None,
    ) -> None:
        """Retorna para a tela de login."""

        self._on_voltar_login()

    def _validar_dados_pessoais(self) -> tuple[bool, str]:
        """Valida os campos da primeira etapa."""

        nome = str(self.nome.value or "").strip()
        cpf = str(self.cpf.value or "").strip()
        celular = str(self.celular.value or "").strip()
        senha = str(self.senha.value or "")
        confirmar_senha = str(self.confirmar_senha.value or "")

        if not nome:
            return False, "Informe o nome completo."
        if not cpf:
            return False, "Informe o CPF."
        if not celular:
            return False, "Informe o celular."
        if not senha:
            return False, "Informe a senha."
        if not confirmar_senha:
            return False, "Confirme a senha."
        if senha != confirmar_senha:
            return False, "As senhas não coincidem."

        return True, ""

    def _validar_endereco(self) -> tuple[bool, str]:
        """Valida os dados obrigatórios da segunda etapa."""

        valido, mensagem = CepService.validar_formato(
            str(self.cep.value or "")
        )

        if not valido:
            return False, mensagem

        if not str(self.logradouro.value or "").strip():
            return False, "Consulte um CEP válido antes de criar a conta."
        if not str(self.bairro.value or "").strip():
            return False, "O CEP consultado não retornou o bairro."
        if not str(self.cidade.value or "").strip():
            return False, "O CEP consultado não retornou a cidade."
        if not str(self.uf.value or "").strip():
            return False, "O CEP consultado não retornou a UF."
        if not str(self.numero.value or "").strip():
            return False, "Informe o número do imóvel."

        return True, ""

    def _obter_dados(self) -> dict[str, str]:
        """Reúne os valores informados nas duas etapas."""

        return {
            "nome": self.nome.value,
            "cpf": self.cpf.value,
            "celular": self.celular.value,
            "cep": self.cep.value or "",
            "logradouro": self.logradouro.value or "",
            "numero": self.numero.value or "",
            "complemento": self.complemento.value or "",
            "bairro": self.bairro.value or "",
            "cidade": self.cidade.value or "",
            "uf": self.uf.value or "",
            "senha": self.senha.value,
            "confirmar_senha": self.confirmar_senha.value,
        }

    def _definir_carregamento(
        self,
        carregando: bool,
    ) -> None:
        """Atualiza o estado visual durante o cadastro."""

        self.indicador.visible = carregando
        self.botao_criar_conta.disabled = carregando
        self.botao_voltar_dados.disabled = carregando
        self.botao_buscar_cep.disabled = carregando
        self._atualizar_pagina()

    def _atualizar_pagina(self) -> None:
        """Atualiza a página sem interromper o fluxo inicial."""

        try:
            self.page.update()
        except RuntimeError:
            pass
