from models import Estabelecimento
from repositories import (
    EstabelecimentoRepository,
    SQLiteDatabase,
)


SQLiteDatabase().inicializar()

repository = EstabelecimentoRepository()

estabelecimento = Estabelecimento(
    nome="Estabelecimento Teste",
    cpf="529.982.247-25",
    email="teste@example.com",
    celular="(91) 99999-9999",
    endereco="Rua de Teste, 100",
    bairro="Centro",
    setor="Terra Firme",
)

try:
    salvo = repository.cadastrar(estabelecimento)

    print("Cadastro realizado:")
    print(salvo)

except ValueError as erro:
    print("Aviso:", erro)

print("\nEstabelecimentos cadastrados:")

for item in repository.listar():
    print(item.id, item.nome, item.cpf)