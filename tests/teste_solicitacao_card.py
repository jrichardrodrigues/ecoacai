import flet as ft

from components.cards import SolicitacaoCard
from models import SolicitacaoColeta


def main(page: ft.Page):
    page.title = "Teste SolicitacaoCard"
    page.padding = 20

    solicitacao = SolicitacaoColeta(
        id=1,
        quantidade_sacas=15,
        quantidade_kg=320,
        status="PENDENTE",
    )

    card = SolicitacaoCard(
        solicitacao=solicitacao,
        nome_estabelecimento="Açaiteria Belém Norte",
    )

    page.add(card)


if __name__ == "__main__":
    ft.run(main)