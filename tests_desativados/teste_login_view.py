# import flet as ft
#
# from views.login_view import LoginView
#
#
# def main(page: ft.Page):
#
#     page.title = "EcoAçaí"
#
#     page.add(
#
#         LoginView(page).build()
#
#     )
#
#
# if __name__ == "__main__":
#     ft.run(main)

from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)

controller = SolicitacaoColetaController()

solicitacoes = controller.listar_com_estabelecimento()

print(type(solicitacoes))

for solicitacao in solicitacoes:
    print(solicitacao)