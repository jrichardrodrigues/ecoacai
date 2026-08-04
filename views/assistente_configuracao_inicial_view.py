from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.buttons import PrimaryButton
from components.cards import FormCard
from components.headers import PageHeader
from components.theme import Colors, Radius, Spacing

from controllers.organizacao_controller import OrganizacaoController
from models import Organizacao, SessaoUsuario
from utils.messages import mostrar_erro, mostrar_sucesso


class AssistenteConfiguracaoInicialView:
    """
    Assistente de primeiro acesso do Gerador.

    Permite cadastrar a organização e vinculá-la ao usuário
    autenticado antes de liberar o acesso ao portal.
    """

    def __init__(
            self,
            page: ft.Page,
            controller: OrganizacaoController,
            sessao: SessaoUsuario,
            on_configuracao_concluida: Callable[[Organizacao], None],
    ) -> None:
        self.page = page
        self.controller = controller
        self.sessao = sessao
        self._on_configuracao_concluida = on_configuracao_concluida

        self._construir_controles()
        self._preencher_dados_usuario()

    def _construir_controles(self) -> None:
        """Cria os controles do formulário."""

        self.nome = ft.TextField(
            label="Nome da organização",
            hint_text="Ex.: Açaí Rodrigues",
            autofocus=True,
            width=480,
            border_radius=Radius.INPUT,
        )

        self.documento = ft.TextField(
            label="CPF ou CNPJ",
            hint_text="Somente números ou documento formatado",
            width=230,
            border_radius=Radius.INPUT,
        )

        self.telefone = ft.TextField(
            label="Telefone/WhatsApp da organização",
            hint_text="(00) 00000-0000",
            width=230,
            border_radius=Radius.INPUT,
            keyboard_type=ft.KeyboardType.PHONE,
        )

        self.email = ft.TextField(
            label="E-mail",
            hint_text="contato@organizacao.com.br",
            width=480,
            border_radius=Radius.INPUT,
            keyboard_type=ft.KeyboardType.EMAIL,
        )

        self.indicador = ft.ProgressRing(
            width=22,
            height=22,
            visible=False,
        )

        self.botao_continuar = PrimaryButton(
            label="CONTINUAR",
            icon=ft.Icons.ARROW_FORWARD,
            on_click=self._salvar,
        )

    def _preencher_dados_usuario(self) -> None:
        """Reaproveita os dados do usuário autenticado."""

        usuario = self.sessao.usuario

        if usuario.celular:
            self.telefone.value = usuario.celular

        if usuario.email:
            self.email.value = usuario.email

    def construir(self) -> ft.Control:
        """Constrói a interface do assistente."""

        card = FormCard(
            width=560,
            content=ft.Column(
                controls=[
                    PageHeader(
                        title="Bem-vindo à ZELURBIS",
                        subtitle=(
                            "Antes de começar, informe os dados "
                            "da organização geradora do resíduo."
                        ),
                        icon=ft.Icons.DOMAIN_ADD_OUTLINED,
                    ),
                    ft.Container(
                        padding=ft.Padding.only(
                            bottom=Spacing.SM,
                        ),
                        content=ft.Text(
                            (
                                "Essa configuração é necessária "
                                "somente no primeiro acesso."
                            ),
                            size=13,
                            color=Colors.TEXT_SECONDARY,
                        ),
                    ),
                    self.nome,
                    ft.Row(
                        controls=[
                            self.documento,
                            self.telefone,
                        ],
                        spacing=Spacing.MD,
                        wrap=True,
                    ),
                    self.email,
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self.indicador,
                            self.botao_continuar,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        vertical_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        spacing=Spacing.SM,
                    ),
                ],
                spacing=Spacing.MD,
                tight=True,
            ),
        )

        return ft.Container(
            expand=True,
            bgcolor=Colors.BACKGROUND,
            alignment=ft.Alignment.CENTER,
            padding=Spacing.LG,
            content=card,
        )

    def build(self) -> ft.Control:
        """Mantém compatibilidade com o padrão atual das Views."""

        return self.construir()

    def _salvar(
        self,
        _evento: ft.ControlEvent,
    ) -> None:
        """Cadastra a organização e conclui o primeiro acesso."""

        nome = str(self.nome.value or "").strip()
        documento = str(self.documento.value or "").strip()
        telefone = str(self.telefone.value or "").strip()
        email = str(self.email.value or "").strip()

        if not nome:
            mostrar_erro(
                self.page,
                "Informe o nome da organização.",
            )
            return

        if not documento:
            mostrar_erro(
                self.page,
                "Informe o CPF ou CNPJ da organização.",
            )
            return

        self._definir_carregamento(True)

        try:
            sucesso, mensagem, organizacao = (
                self.controller.cadastrar_gerador(
                    nome=nome,
                    documento=documento,
                    telefone=telefone,
                    email=email,
                )
            )
        finally:
            self._definir_carregamento(False)

        if not sucesso or organizacao is None:
            mostrar_erro(
                self.page,
                mensagem,
            )
            return

        mostrar_sucesso(
            self.page,
            mensagem,
        )

        self._on_configuracao_concluida(
            organizacao
        )

    def _definir_carregamento(
        self,
        carregando: bool,
    ) -> None:
        """Atualiza o estado visual durante o cadastro."""

        self.indicador.visible = carregando
        self.botao_continuar.disabled = carregando

        try:
            self.page.update()
        except RuntimeError:
            pass