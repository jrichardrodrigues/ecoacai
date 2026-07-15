from collections.abc import Callable

import flet as ft
import urllib.parse
import webbrowser
from components.cards import SolicitacaoCard
from components.tables import Toolbar
from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from models import SolicitacaoColeta
from components.dialogs import ConfirmDialog
from utils.messages import (
    mostrar_erro,
    mostrar_sucesso,
)

class SolicitacoesView:
    """Tela de listagem das solicitações de coleta."""

    def __init__(
        self,
        page: ft.Page,
        on_nova_solicitacao: Callable[[], None] | None = None,
        on_editar_solicitacao: (
            Callable[[SolicitacaoColeta], None] | None
        ) = None,
    ) -> None:
        self.page = page
        self.on_nova_solicitacao = on_nova_solicitacao
        self.on_editar_solicitacao = on_editar_solicitacao

        self.controller = SolicitacaoColetaController()

        self.estabelecimento_controller = (
            EstabelecimentoController()
        )

        self.toolbar = Toolbar(
            titulo="Solicitações de Coleta",
            on_search=self.pesquisar,
            on_add=self.nova_solicitacao,
        )

        self.total = ft.Text(
            "",
            size=14,
            color=ft.Colors.GREY_700,
        )

        self.lista_cards = ft.Column(
            controls=[],
            spacing=12,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )

        self.sem_registros = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.INBOX_OUTLINED,
                        size=64,
                        color=ft.Colors.GREY_400,
                    ),
                    ft.Text(
                        "Nenhuma solicitação encontrada.",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Clique em 'Novo' para criar "
                        "a primeira solicitação.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=10,
            ),
            expand=True,
            visible=False,
        )

        self.atualizar_lista()

    def atualizar_lista(
        self,
        pesquisa: str = "",
    ) -> None:
        """Carrega as solicitações e monta os cards."""

        solicitacoes = self.controller.listar()

        pesquisa_normalizada = (
            pesquisa or ""
        ).strip().lower()

        cards: list[ft.Control] = []

        for solicitacao in solicitacoes:
            estabelecimento = (
                self.estabelecimento_controller
                .buscar_estabelecimento_por_id(
                    solicitacao.estabelecimento_id,
                )
            )

            nome_estabelecimento = (
                estabelecimento.nome
                if estabelecimento is not None
                else "Estabelecimento não encontrado"
            )

            if pesquisa_normalizada:
                texto_pesquisa = " ".join(
                    [
                        solicitacao.numero,
                        nome_estabelecimento,
                        solicitacao.status,
                        solicitacao.prioridade,
                    ]
                ).lower()

                if pesquisa_normalizada not in texto_pesquisa:
                    continue

            cards.append(
                SolicitacaoCard(
                    solicitacao=solicitacao,
                    nome_estabelecimento=nome_estabelecimento,
                    on_editar=(
                        lambda e,
                        item_id=solicitacao.id:
                        self.editar(item_id)
                    ),
                    on_status=(
                        lambda e,
                        item_id=solicitacao.id:
                        self.alterar_status(item_id)
                    ),
                    on_maps=(
                        lambda e,
                        item_id=solicitacao.id:
                        self.abrir_maps(item_id)
                    ),
                    on_whatsapp=(
                        lambda e,
                        item_id=solicitacao.id:
                        self.abrir_whatsapp(item_id)
                    ),
                    on_excluir=(
                        lambda e,
                               item_id=solicitacao.id:
                        self.excluir(item_id)
                    ),
                )
            )

        self.lista_cards.controls = cards

        quantidade = len(cards)

        self.total.value = (
            f"Total de solicitações: {quantidade}"
        )

        tem_registros = quantidade > 0

        self.lista_cards.visible = tem_registros
        self.sem_registros.visible = not tem_registros

    def pesquisar(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Pesquisa solicitações em tempo real."""

        self.atualizar_lista(
            pesquisa=e.control.value or "",
        )

        self.page.update()

    def nova_solicitacao(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Solicita a abertura do formulário de cadastro."""

        if self.on_nova_solicitacao is None:
            mostrar_erro(
                self.page,
                "A navegação para nova solicitação "
                "não foi configurada.",
            )
            return

        self.on_nova_solicitacao()

    def editar(
        self,
        solicitacao_id: int | None,
    ) -> None:
        """Solicita a abertura do formulário de edição."""

        if solicitacao_id is None:
            mostrar_erro(
                self.page,
                "Solicitação inválida.",
            )
            return

        solicitacao = self.controller.buscar_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            mostrar_erro(
                self.page,
                "Solicitação não encontrada.",
            )
            return

        if self.on_editar_solicitacao is None:
            mostrar_erro(
                self.page,
                "A navegação para edição "
                "não foi configurada.",
            )
            return

        self.on_editar_solicitacao(
            solicitacao
        )

    def excluir(
            self,
            solicitacao_id: int | None,
    ) -> None:
        """Solicita confirmação para excluir."""

        if solicitacao_id is None:
            mostrar_erro(
                self.page,
                "Solicitação inválida.",
            )
            return

        dialog = ConfirmDialog(
            page=self.page,
            titulo="Excluir Solicitação",
            mensagem=(
                "Deseja realmente excluir esta solicitação?"
            ),
            on_confirm=lambda: self.confirmar_exclusao(
                solicitacao_id
            ),
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def confirmar_exclusao(
            self,
            solicitacao_id: int,
    ) -> None:
        """Exclui a solicitação."""

        sucesso, mensagem = self.controller.excluir(
            solicitacao_id
        )

        if not sucesso:
            mostrar_erro(
                self.page,
                mensagem,
            )
            return

        self.atualizar_lista()
        self.page.update()

        mostrar_sucesso(
            self.page,
            mensagem,
        )

    def alterar_status(
            self,
            solicitacao_id: int | None,
    ) -> None:
        """Altera o status da solicitação."""

        if solicitacao_id is None:
            mostrar_erro(
                self.page,
                "Solicitação inválida.",
            )
            return

        sucesso, mensagem, _ = (
            self.controller.alterar_status(
                solicitacao_id
            )
        )

        if not sucesso:
            mostrar_erro(
                self.page,
                mensagem,
            )
            return

        self.atualizar_lista()
        self.page.update()

        mostrar_sucesso(
            self.page,
            mensagem,
        )

    def abrir_maps(
            self,
            solicitacao_id: int | None,
    ) -> None:
        """Abre o estabelecimento no Google Maps."""

        if solicitacao_id is None:
            mostrar_erro(
                self.page,
                "Solicitação inválida.",
            )
            return

        solicitacao = self.controller.buscar_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            mostrar_erro(
                self.page,
                "Solicitação não encontrada.",
            )
            return

        estabelecimento = (
            self.estabelecimento_controller
            .buscar_estabelecimento_por_id(
                solicitacao.estabelecimento_id
            )
        )

        if estabelecimento is None:
            mostrar_erro(
                self.page,
                "Estabelecimento não encontrado.",
            )
            return

        consulta = " ".join(
            filtro
            for filtro in (
                estabelecimento.nome,
                estabelecimento.endereco,
                estabelecimento.bairro,
            )
            if filtro
        )

        if not consulta.strip():
            mostrar_erro(
                self.page,
                "O estabelecimento não possui endereço cadastrado.",
            )
            return

        url = (
                "https://www.google.com/maps/search/?api=1&query="
                + urllib.parse.quote(consulta)
        )

        try:
            webbrowser.open(url)

            mostrar_sucesso(
                self.page,
                "Abrindo Google Maps...",
            )

        except Exception as erro:
            print("Erro ao abrir Google Maps:", erro)

            mostrar_erro(
                self.page,
                "Não foi possível abrir o Google Maps.",
            )

    def abrir_whatsapp(
        self,
        solicitacao_id: int | None,
    ) -> None:
        """Ação temporária para integração com WhatsApp."""

        if solicitacao_id is None:
            mostrar_erro(
                self.page,
                "Solicitação inválida.",
            )
            return

        mostrar_erro(
            self.page,
            f"WhatsApp da solicitação "
            f"{solicitacao_id} será integrado.",
        )

    def build(self) -> ft.Control:
        """Constrói e retorna a tela."""

        return ft.Column(
            controls=[
                self.toolbar,
                self.total,
                ft.Divider(),
                ft.Stack(
                    controls=[
                        self.sem_registros,
                        self.lista_cards,
                    ],
                    expand=True,
                ),
            ],
            spacing=15,
            expand=True,
        )