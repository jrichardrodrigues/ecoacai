from pathlib import Path

from repositories import SQLiteDatabase, UsuarioRepository
from services import CadastroContaService, PasswordService


ARQUIVO_TESTE = Path("data/teste_cadastro_conta.db")

if ARQUIVO_TESTE.exists():
    ARQUIVO_TESTE.unlink()

database = SQLiteDatabase(ARQUIVO_TESTE)
database.inicializar()

repository = UsuarioRepository(database)

service = CadastroContaService(
    usuario_repository=repository,
    password_service=PasswordService(),
)

dados = {
    "nome": "Carlos da Silva",
    "cpf": "529.982.247-25",
    "celular": "(91) 98888-7777",
    "cep": "01001-000",
    "logradouro": "Praça da Sé",
    "numero": "100",
    "complemento": "Sala 1",
    "bairro": "Sé",
    "cidade": "São Paulo",
    "uf": "SP",
    "senha": "@Carlos12",
    "confirmar_senha": "@Carlos12",
}

sucesso, mensagem, usuario = service.cadastrar(dados)

print("Sucesso:", sucesso)
print("Mensagem:", mensagem)
print("Usuário:", usuario)

if usuario:
    print(
        "Senha não foi armazenada em texto puro:",
        usuario.senha_hash != dados["senha"],
    )

# Teste de duplicidade
sucesso, mensagem, usuario = service.cadastrar(dados)

print("\nSegundo cadastro:")
print("Sucesso:", sucesso)
print("Mensagem:", mensagem)
print("Usuário:", usuario)

ARQUIVO_TESTE.unlink(missing_ok=True)

print("\nBanco temporário removido.")