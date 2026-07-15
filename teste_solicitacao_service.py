from services import SolicitacaoColetaService

service = SolicitacaoColetaService()

solicitacao = service.criar(
    estabelecimento_id=1,
    quantidade_sacas=15,
    quantidade_kg=320,
)

print(solicitacao)