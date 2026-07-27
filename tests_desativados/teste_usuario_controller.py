from controllers import UsuarioController


controller = UsuarioController()

dados = {
    "nome": "João do Açaí",
    "cpf": "52998224725",
    "email": "joao@email.com",
    "celular": "91988887777",
    "endereco": "Travessa Central, 55",
    "bairro": "Terra Firme",
    "setor": "Terra Firme",
}

sucesso, mensagem = controller.cadastrar_usuario(dados)
print(sucesso, mensagem)

usuarios = controller.listar_usuarios()
print(usuarios)