from pathlib import Path

from models import Usuario
from repositories import SQLiteDatabase, UsuarioRepository


ARQUIVO_TESTE = Path("data/teste_app.db")

if ARQUIVO_TESTE.exists():
    ARQUIVO_TESTE.unlink()

database = SQLiteDatabase(ARQUIVO_TESTE)
database.inicializar()

repository = UsuarioRepository(database)

usuario = Usuario(
    nome="Carlos da Silva",
    cpf="529.982.247-25",
    celular="(91) 98888-7777",
    cep="66000-000",
    logradouro="Rua de Teste",
    numero="100",
    complemento="Casa A",
    bairro="Centro",
    cidade="Belém",
    uf="PA",

    # Apenas valor provisório para testar o banco.
    # O hash verdadeiro será criado na próxima sprint.
    senha_hash="HASH_PROVISORIO",
)

usuario_salvo = repository.cadastrar(usuario)

print("Usuário cadastrado:")
print(usuario_salvo)

print("\nBusca pelo CPF:")
print(repository.buscar_por_cpf("52998224725"))

print("\nCPF existe:")
print(repository.cpf_existe("529.982.247-25"))

print("\nCelular existe:")
print(repository.celular_existe("(91) 98888-7777"))

print("\nUsuários:")
for item in repository.listar():
    print("-", item.nome, item.cpf, item.celular)

ARQUIVO_TESTE.unlink(missing_ok=True)

print("\nBanco temporário removido.")