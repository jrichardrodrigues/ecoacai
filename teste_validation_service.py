from services import UsuarioService, UsuarioValidationService


usuario_service = UsuarioService()
validation_service = UsuarioValidationService(usuario_service)

dados = {
    "nome": "Teste da Silva",
    "cpf": "168.995.350-09",
    "email": "teste@hotmail.con",
    "celular": "(91) 98888-7777",
    "endereco": "Rua de Teste, 100",
    "bairro": "Guamá",
    "setor": "Guamá",
}

sucesso, mensagem, dados_normalizados = validation_service.validar(dados)

print("Sucesso:", sucesso)
print("Mensagem:", mensagem)
print("Dados:", dados_normalizados)