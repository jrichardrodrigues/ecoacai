import re

from models import Usuario
from repositories import UsuarioRepository
from services.cep_service import CepService
from services.cpf_service import CpfService
from services.password_service import PasswordService
from services.phone_service import PhoneService


class CadastroContaService:
    """Valida e cadastra uma nova conta no SQLite."""

    def __init__(
        self,
        usuario_repository: UsuarioRepository | None = None,
        password_service: PasswordService | None = None,
    ):
        self.usuario_repository = (
            usuario_repository or UsuarioRepository()
        )

        self.password_service = (
            password_service or PasswordService()
        )

    def cadastrar(
        self,
        dados: dict,
    ) -> tuple[bool, str, Usuario | None]:
        nome = self._normalizar_texto(dados.get("nome"))
        cpf = CpfService.remover_formatacao(
            dados.get("cpf") or ""
        )
        celular = PhoneService.somente_digitos(
            dados.get("celular") or ""
        )
        cep = CepService.formatar(dados.get("cep") or "")

        logradouro = self._normalizar_texto(
            dados.get("logradouro")
        )
        numero = self._normalizar_texto(
            dados.get("numero")
        )
        complemento = self._normalizar_texto(
            dados.get("complemento")
        )
        bairro = self._normalizar_texto(
            dados.get("bairro")
        )
        cidade = self._normalizar_texto(
            dados.get("cidade")
        )
        uf = self._normalizar_texto(
            dados.get("uf")
        ).upper()

        senha = str(dados.get("senha") or "")
        confirmar_senha = str(
            dados.get("confirmar_senha") or ""
        )

        valido, mensagem = self._validar_nome(nome)

        if not valido:
            return False, mensagem, None

        if not CpfService.validar(cpf):
            return False, "CPF inválido.", None

        if self.usuario_repository.cpf_existe(cpf):
            return False, "CPF já cadastrado.", None

        valido, mensagem = PhoneService.validar(celular)

        if not valido:
            return False, mensagem, None

        if self.usuario_repository.celular_existe(celular):
            return False, "Celular já cadastrado.", None

        valido, mensagem = CepService.validar_formato(cep)

        if not valido:
            return False, mensagem, None

        valido, mensagem = self._validar_endereco(
            logradouro=logradouro,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            uf=uf,
        )

        if not valido:
            return False, mensagem, None

        valido, mensagem = (
            self.password_service.validar_confirmacao(
                senha,
                confirmar_senha,
            )
        )

        if not valido:
            return False, mensagem, None

        senha_hash = self.password_service.gerar_hash(senha)

        usuario = Usuario(
            nome=nome,
            cpf=cpf,
            celular=celular,
            cep=cep,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            uf=uf,
            senha_hash=senha_hash,

            # Ficará False até confirmarmos o código enviado
            # pelo WhatsApp.
            celular_confirmado=False,
            ativo=True,
        )

        try:
            usuario_salvo = self.usuario_repository.cadastrar(
                usuario
            )

        except ValueError as erro:
            return False, str(erro), None

        return (
            True,
            "Conta criada com sucesso.",
            usuario_salvo,
        )

    @staticmethod
    def _normalizar_texto(valor) -> str:
        return " ".join(str(valor or "").strip().split())

    @staticmethod
    def _validar_nome(nome: str) -> tuple[bool, str]:
        if not nome:
            return False, "Informe o nome completo."

        if len(nome) < 5:
            return False, "Informe um nome válido."

        if len(nome.split()) < 2:
            return False, "Informe o nome e o sobrenome."

        if any(caractere.isdigit() for caractere in nome):
            return False, "O nome não pode conter números."

        padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$"

        if not re.fullmatch(padrao, nome):
            return False, "O nome contém caracteres inválidos."

        return True, ""

    @staticmethod
    def _validar_endereco(
        logradouro: str,
        numero: str,
        bairro: str,
        cidade: str,
        uf: str,
    ) -> tuple[bool, str]:
        if not logradouro:
            return False, "Informe o logradouro."

        if not numero:
            return False, "Informe o número do imóvel."

        if not bairro:
            return False, "Informe o bairro."

        if not cidade:
            return False, "Informe a cidade."

        if len(uf) != 2 or not uf.isalpha():
            return False, "Informe uma UF válida."

        return True, ""