from pathlib import Path

from models import Usuario
from repositories import SQLiteDatabase, UsuarioRepository
from services import AuthService, PasswordService


ARQUIVO_TESTE = Path("data/teste_auth.db")

if ARQUIVO_TESTE.exists():
    ARQUIVO_TESTE.unlink()

database = SQLiteDatabase(ARQUIVO_TESTE)
database.inicializar()

usuario_repository = UsuarioRepository(database)
password_service = PasswordService()

usuario = Usuario(
    nome="Carlos da Silva",
    cpf="529.982.247-25",
    celular="(91) 98888-7777",
    cep="66000-000",
    logradouro="Rua de Teste",
    numero="100",
    bairro="Centro",
    cidade="Belém",
    uf="PA",
    senha_hash=password_service.gerar_hash("@Carlos12"),
    celular_confirmado=True,
)

usuario_repository.cadastrar(usuario)

auth_service = AuthService(
    usuario_repository=usuario_repository,
    password_service=password_service,
)

print(
    "Login correto:",
    auth_service.autenticar(
        "529.982.247-25",
        "@Carlos12",
    )[:2],
)

print(
    "Senha incorreta:",
    auth_service.autenticar(
        "529.982.247-25",
        "@Carlos99",
    )[:2],
)

print(
    "CPF inexistente:",
    auth_service.autenticar(
        "168.995.350-09",
        "@Carlos12",
    )[:2],
)

print(
    "CPF incompleto:",
    auth_service.autenticar(
        "123",
        "@Carlos12",
    )[:2],
)

ARQUIVO_TESTE.unlink(missing_ok=True)