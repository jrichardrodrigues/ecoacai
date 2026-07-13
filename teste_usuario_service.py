from models import Usuario
from services import UsuarioService


service = UsuarioService()

usuario = Usuario(
    nome="Maria do Açaí",
    cpf="123.456.789-09",
    email="maria@email.com",
    celular="91999999999",
    endereco="Rua Principal, 100",
    bairro="Guamá",
    setor="Guamá"
)

sucesso, mensagem = service.cadastrar(usuario)
print(sucesso, mensagem)

usuarios = service.listar()
print(usuarios)

usuario_encontrado = service.buscar_por_id(1)
print(usuario_encontrado)
