import flet as ft

from components.cards import SolicitacaoCard
from components.tables import Toolbar
from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
# from utils.messages import mostrar_erro
from utils.messages import (
    mostrar_erro,
    mostrar_sucesso,
)


class SolicitacoesView:
    """Tela de listagem das solicitações de coleta."""

    def __init__(
        self,
        page: ft.Page,
        on_nova_solicitacao=None,
    ) -> None:
        self.page = page
        self.on_nova_solicitacao = on_nova_solicitacao

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
        """Carrega as solicitações e monta os Cards."""

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
                    nome_estabelecimento=(
                        nome_estabelecimento
                    ),
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
        self.atualizar_lista(
            pesquisa=e.control.value or "",
        )

        self.page.update()

    def nova_solicitacao(
            self,
            e: ft.ControlEvent,
    ) -> None:
        """Abre o formulário de nova solicitação."""

        if self.on_nova_solicitacao is None:
            mostrar_erro(
                self.page,
                "A navegação não foi configurada.",
            )
            return

        self.on_nova_solicitacao()

    def editar(
        self,
        solicitacao_id: int | None,
    ) -> None:
        mostrar_erro(
            self.page,
            f"Edição da solicitação "
            f"{solicitacao_id} será implementada.",
        )

    def alterar_status(
        self,
        solicitacao_id: int | None,
    ) -> None:
        mostrar_erro(
            self.page,
            f"Alteração de status da solicitação "
            f"{solicitacao_id} será implementada.",
        )

    def abrir_maps(
        self,
        solicitacao_id: int | None,
    ) -> None:
        mostrar_erro(
            self.page,
            f"Google Maps da solicitação "
            f"{solicitacao_id} será integrado.",
        )

    def abrir_whatsapp(
        self,
        solicitacao_id: int | None,
    ) -> None:
        mostrar_erro(
            self.page,
            f"WhatsApp da solicitação "
            f"{solicitacao_id} será integrado.",
        )

    def build(self) -> ft.Control:
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