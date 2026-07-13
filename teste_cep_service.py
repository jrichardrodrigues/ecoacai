from services import CepService


ceps = [
    "",
    "123",
    "99999-999",
    "01001-000",
]

for cep in ceps:
    sucesso, mensagem, endereco = CepService.consultar(cep)

    print("\nCEP:", repr(cep))
    print("Sucesso:", sucesso)
    print("Mensagem:", mensagem)
    print("Endereço:", endereco)