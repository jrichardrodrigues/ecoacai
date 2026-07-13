from models import Usuario
from services import UsuarioService, UsuarioValidationService


class UsuarioController:

    def __init__(self):
        self.usuario_service = UsuarioService()

        self.validation_service = UsuarioValidationService(
            self.usuario_service
        )

    def listar_usuarios(self):
        return self.usuario_service.listar()

    def buscar_usuario_por_id(self, usuario_id: int):
        return self.usuario_service.buscar_por_id(usuario_id)

    def cadastrar_usuario(self, dados: dict):
        sucesso, mensagem, dados_normalizados = (
            self.validation_service.validar(dados)
        )

        if not sucesso:
            return False, mensagem

        usuario = Usuario(
            nome=dados_normalizados["nome"],
            cpf=dados_normalizados["cpf"],
            email=dados_normalizados["email"],
            celular=dados_normalizados["celular"],
            celular_confirmado=False,
            endereco=dados_normalizados["endereco"],
            bairro=dados_normalizados["bairro"],
            setor=dados_normalizados["setor"],
        )

        return self.usuario_service.cadastrar(usuario)

    def atualizar_usuario(
        self,
        usuario_id: int,
        dados: dict,
    ):
        usuario = self.usuario_service.buscar_por_id(usuario_id)

        if not usuario:
            return False, "Usuário não encontrado."

        sucesso, mensagem, dados_normalizados = (
            self.validation_service.validar(
                dados,
                ignorar_id=usuario_id,
            )
        )

        if not sucesso:
            return False, mensagem

        usuario.nome = dados_normalizados["nome"]
        usuario.cpf = dados_normalizados["cpf"]
        usuario.email = dados_normalizados["email"]
        usuario.celular = dados_normalizados["celular"]
        usuario.endereco = dados_normalizados["endereco"]
        usuario.bairro = dados_normalizados["bairro"]
        usuario.setor = dados_normalizados["setor"]

        return self.usuario_service.atualizar(usuario)

    def excluir_usuario(self, usuario_id: int):
        return self.usuario_service.excluir(usuario_id)