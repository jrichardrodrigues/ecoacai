from models import Usuario
from services.base_service import BaseService


class UsuarioService(BaseService):

    def listar(self):
        dados = self.repo.carregar()
        return [Usuario.from_dict(usuario) for usuario in dados["usuarios"]]

    def buscar_por_id(self, usuario_id: int):
        usuarios = self.listar()

        for usuario in usuarios:
            if usuario.id == usuario_id:
                return usuario

        return None

    def cpf_existe(self, cpf: str, ignorar_id: int = 0):
        usuarios = self.listar()

        for usuario in usuarios:
            if usuario.cpf == cpf and usuario.id != ignorar_id:
                return True

        return False

    def email_existe(self, email: str, ignorar_id: int = 0):
        usuarios = self.listar()

        for usuario in usuarios:
            if usuario.email == email and usuario.id != ignorar_id:
                return True

        return False

    def celular_existe(self, celular: str, ignorar_id: int = 0):
        usuarios = self.listar()

        for usuario in usuarios:
            if usuario.celular == celular and usuario.id != ignorar_id:
                return True

        return False

    def gerar_proximo_id(self):
        usuarios = self.listar()

        if not usuarios:
            return 1

        return max(usuario.id for usuario in usuarios) + 1

    def cadastrar(self, usuario: Usuario):
        dados = self.repo.carregar()

        if self.cpf_existe(usuario.cpf):
            return False, "CPF já cadastrado."

        if self.email_existe(usuario.email):
            return False, "E-mail já cadastrado."

        usuario.id = self.gerar_proximo_id()

        dados["usuarios"].append(usuario.to_dict())
        self.repo.salvar(dados)

        return True, "Usuário cadastrado com sucesso."

    def atualizar(self, usuario_atualizado: Usuario):
        dados = self.repo.carregar()
        usuarios = dados["usuarios"]

        if self.cpf_existe(usuario_atualizado.cpf, ignorar_id=usuario_atualizado.id):
            return False, "CPF já cadastrado para outro usuário."

        if self.email_existe(usuario_atualizado.email, ignorar_id=usuario_atualizado.id):
            return False, "E-mail já cadastrado para outro usuário."

        for index, usuario in enumerate(usuarios):
            if usuario["id"] == usuario_atualizado.id:
                usuarios[index] = usuario_atualizado.to_dict()
                self.repo.salvar(dados)
                return True, "Usuário atualizado com sucesso."

        return False, "Usuário não encontrado."

    def excluir(self, usuario_id: int):
        dados = self.repo.carregar()
        usuarios = dados["usuarios"]

        nova_lista = [usuario for usuario in usuarios if usuario["id"] != usuario_id]

        if len(nova_lista) == len(usuarios):
            return False, "Usuário não encontrado."

        dados["usuarios"] = nova_lista
        self.repo.salvar(dados)

        return True, "Usuário excluído com sucesso."