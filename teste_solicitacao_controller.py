from repositories.sqlite_database import SQLiteDatabase
from controllers.solicitacao_coleta_controller import (
    SolicitacaoColetaController,
)


SQLiteDatabase().inicializar()

controller = SolicitacaoColetaController()

sucesso, mensagem, solicitacao = controller.criar(
    estabelecimento_id=1,
    quantidade_sacas=10,
    quantidade_kg=250,
    observacao="Coleta de teste",
)

print(sucesso)
print(mensagem)
print(solicitacao)