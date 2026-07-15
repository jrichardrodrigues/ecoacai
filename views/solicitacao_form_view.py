from collections.abc import Callable

import flet as ft

from controllers.estabelecimento_controller import (
    EstabelecimentoController,
)
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)
from utils.messages import (
    mostrar_erro,
    mostrar_sucesso,
)

class SolicitacaoFormView:
    """Formulário para criar uma solicitação de coleta."""

    def __init__(
        self,
        page: ft.Page,
        on_cancelar: Callable[[], None] | None = None,
        on_salvar_sucesso: Callable[[], None] | None = None,
    ) -> None:
        self.page = page
        self.on_cancelar = on_cancelar
        self.on_salvar_sucesso = on_salvar_sucesso

        self.controller = SolicitacaoColetaController()
        self.estabelecimento_controller = (
            EstabelecimentoController()
        )

        self.estabelecimentos = (
            self.estabelecimento_controller
            .listar_estabelecimentos()
        )

        self.estabelecimento = ft.Dropdown(
            label="Estabelecimento",
            hint_text="Selecione o estabelecimento",
            expand=True,
            border_radius=10,
            options=[
                ft.dropdown.Option(
                    key=str(item.id),
                    text=item.nome,
                )
                for item in self.estabelecimentos
                if item.id is not None
            ],
        )

        self.estabelecimento.on_change = (
            self.ao_selecionar_estabelecimento
        )

        self.quantidade_sacas = ft.TextField(
            label="Quantidade de sacas",
            hint_text="Ex.: 10",
            value="1",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=True,
        )

        self.quantidade_kg = ft.TextField(
            label="Quantidade em kg",
            hint_text="Ex.: 250",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=True,
        )

        self.observacao = ft.TextField(
            label="Observação",
            hint_text="Informações adicionais sobre a coleta",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=10,
        )

        self.resumo_estabelecimento = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Selecione um estabelecimento.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                spacing=5,
            ),
            padding=12,
            border_radius=10,
            bgcolor=ft.Colors.GREY_100,
            visible=True,
        )

    def ao_selecionar_estabelecimento(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Atualiza o resumo do estabelecimento selecionado."""

        valor = e.control.value

        if not valor:
            self.resumo_estabelecimento.content = ft.Column(
                controls=[
                    ft.Text(
                        "Selecione um estabelecimento.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                spacing=5,
            )

            self.page.update()
            return

        estabelecimento_id = int(valor)

        estabelecimento = next(
            (
                item
                for item in self.estabelecimentos
                if item.id == estabelecimento_id
            ),
            None,
        )

        if estabelecimento is None:
            self.resumo_estabelecimento.content = ft.Text(
                "Estabelecimento não encontrado.",
                color=ft.Colors.RED,
            )

            self.page.update()
            return

        self.resumo_estabelecimento.content = ft.Column(
            controls=[
                ft.Text(
                    estabelecimento.nome,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    f"Bairro: {estabelecimento.bairro}",
                ),
                ft.Text(
                    f"Setor: {estabelecimento.setor}",
                ),
                ft.Text(
                    f"Celular: {estabelecimento.celular}",
                ),
            ],
            spacing=5,
        )

        self.page.update()

    def cancelar(
        self,
        e: ft.ControlEvent,
    ) -> None:
        """Retorna para a lista de solicitações."""

        if self.on_cancelar is not None:
            self.on_cancelar()

    def salvar(
            self,
            e: ft.ControlEvent,
    ) -> None:
        """Valida e salva a solicitação."""

        if not self.estabelecimento.value:
            mostrar_erro(
                self.page,
                "Selecione um estabelecimento.",
            )
            return

        try:
            quantidade_sacas = int(
                self.quantidade_sacas.value
            )
        except (TypeError, ValueError):
            mostrar_erro(
                self.page,
                "Quantidade de sacas inválida.",
            )
            return

        if quantidade_sacas <= 0:
            mostrar_erro(
                self.page,
                "Informe pelo menos uma saca.",
            )
            return

        try:
            quantidade_kg = float(
                (self.quantidade_kg.value or "0")
                .replace(",", ".")
            )
        except ValueError:
            mostrar_erro(
                self.page,
                "Quantidade em kg inválida.",
            )
            return

        sucesso, mensagem, _ = self.controller.criar(
            estabelecimento_id=int(
                self.estabelecimento.value
            ),
            quantidade_sacas=quantidade_sacas,
            quantidade_kg=quantidade_kg,
            observacao=self.observacao.value or "",
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

    def build(self) -> ft.Control:
        """Constrói o formulário."""

        return ft.Column(
            controls=[
                ft.Text(
                    "Nova Solicitação de Coleta",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Selecione o estabelecimento e informe "
                    "os dados previstos para a coleta.",
                    size=15,
                ),
                ft.Divider(),

                ft.Row(
                    controls=[
                        self.estabelecimento,
                    ],
                ),

                self.resumo_estabelecimento,

                ft.Row(
                    controls=[
                        self.quantidade_sacas,
                        self.quantidade_kg,
                    ],
                    spacing=15,
                ),

                self.observacao,

                ft.Divider(),

                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            content="Cancelar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=self.cancelar,
                        ),
                        ft.ElevatedButton(
                            content="Salvar solicitação",
                            icon=ft.Icons.SAVE,
                            on_click=self.salvar,
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )