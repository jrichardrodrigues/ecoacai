from __future__ import annotations

import re
from typing import Any

from models import Usuario
from repositories import PerfilRepository, UsuarioRepository
from services.cep_service import CepService
from services.cpf_service import CpfService
from services.password_service import PasswordService
from services.phone_service import PhoneService


class UsuarioService:
    """Regras de negócio dos usuários da plataforma."""

    PERFIL_GERADOR = "GERADOR"
    PERFIL_GESTOR = "GESTOR"
    PERFIL_EMPRESA_PARCEIRA = "EMPRESA_PARCEIRA"

    def __init__(
        self,
        repository: UsuarioRepository | None = None,
        perfil_repository: PerfilRepository | None = None,
        password_service: PasswordService | None = None,
    ) -> None:
        self.repository = repository or UsuarioRepository()
        self.perfil_repository = (
            perfil_repository or PerfilRepository()
        )
        self.password_service = (
            password_service or PasswordService()
        )

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        dados: dict[str, Any],
        perfil_codigo: str = PERFIL_GERADOR,
        organizacao_id: int | None = None,
    ) -> tuple[bool, str, Usuario | None]:
        """
        Valida e cadastra uma conta.

        No cadastro público, o perfil padrão é GERADOR.
        """

        nome = self._normalizar_texto(
            dados.get("nome")
        )
        cpf = CpfService.remover_formatacao(
            str(dados.get("cpf") or "")
        )
        celular = PhoneService.somente_digitos(
            str(dados.get("celular") or "")
        )
        cep = CepService.formatar(
            str(dados.get("cep") or "")
        )
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

        if self.repository.cpf_existe(cpf):
            return False, "CPF já cadastrado.", None

        valido, mensagem = PhoneService.validar(celular)
        if not valido:
            return False, mensagem, None

        if self.repository.celular_existe(celular):
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

        perfil = self.perfil_repository.buscar_por_codigo(
            perfil_codigo
        )

        if perfil is None or perfil.id is None:
            return (
                False,
                f"Perfil '{perfil_codigo}' não encontrado.",
                None,
            )

        if not perfil.ativo:
            return (
                False,
                f"Perfil '{perfil_codigo}' está desativado.",
                None,
            )

        try:
            senha_hash = self.password_service.gerar_hash(
                senha
            )

            usuario = Usuario(
                organizacao_id=organizacao_id,
                perfil_id=perfil.id,
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
                celular_confirmado=True,
                ativo=True,
            )

            usuario_salvo = self.repository.cadastrar(
                usuario
            )

        except ValueError as erro:
            return False, str(erro), None

        except Exception:
            return (
                False,
                "Não foi possível criar a conta.",
                None,
            )

        return (
            True,
            "Conta criada com sucesso.",
            usuario_salvo,
        )

    def cadastrar_gerador(
        self,
        dados: dict[str, Any],
        organizacao_id: int | None = None,
    ) -> tuple[bool, str, Usuario | None]:
        """Cadastra um usuário com perfil GERADOR."""

        return self.cadastrar(
            dados=dados,
            perfil_codigo=self.PERFIL_GERADOR,
            organizacao_id=organizacao_id,
        )

    def cadastrar_gestor(
        self,
        dados: dict[str, Any],
        organizacao_id: int,
    ) -> tuple[bool, str, Usuario | None]:
        """Cadastra um usuário com perfil GESTOR."""

        return self.cadastrar(
            dados=dados,
            perfil_codigo=self.PERFIL_GESTOR,
            organizacao_id=organizacao_id,
        )

    def cadastrar_empresa_parceira(
        self,
        dados: dict[str, Any],
        organizacao_id: int,
    ) -> tuple[bool, str, Usuario | None]:
        """Cadastra usuário de uma empresa parceira."""

        return self.cadastrar(
            dados=dados,
            perfil_codigo=self.PERFIL_EMPRESA_PARCEIRA,
            organizacao_id=organizacao_id,
        )

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        usuario_id: int,
    ) -> Usuario | None:
        if not self._id_valido(usuario_id):
            return None

        return self.repository.buscar_por_id(
            usuario_id
        )

    def buscar_por_cpf(
        self,
        cpf: str,
    ) -> Usuario | None:
        cpf_normalizado = CpfService.remover_formatacao(
            str(cpf or "")
        )

        if not cpf_normalizado:
            return None

        return self.repository.buscar_por_cpf(
            cpf_normalizado
        )

    def listar(
        self,
        somente_ativos: bool = True,
    ) -> list[Usuario]:
        return self.repository.listar(
            somente_ativos=somente_ativos
        )

    def cpf_existe(
        self,
        cpf: str,
        ignorar_id: int | None = None,
    ) -> bool:
        cpf_normalizado = CpfService.remover_formatacao(
            str(cpf or "")
        )

        if not cpf_normalizado:
            return False

        return self.repository.cpf_existe(
            cpf_normalizado,
            ignorar_id=ignorar_id,
        )

    def celular_existe(
        self,
        celular: str,
        ignorar_id: int | None = None,
    ) -> bool:
        celular_normalizado = (
            PhoneService.somente_digitos(
                str(celular or "")
            )
        )

        if not celular_normalizado:
            return False

        return self.repository.celular_existe(
            celular_normalizado,
            ignorar_id=ignorar_id,
        )

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    @staticmethod
    def _validar_nome(
        nome: str,
    ) -> tuple[bool, str]:
        if not nome:
            return False, "Informe o nome completo."

        if len(nome) < 5:
            return False, "Informe um nome válido."

        if len(nome.split()) < 2:
            return False, "Informe o nome e o sobrenome."

        if any(
            caractere.isdigit()
            for caractere in nome
        ):
            return (
                False,
                "O nome não pode conter números.",
            )

        padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$"

        if not re.fullmatch(padrao, nome):
            return (
                False,
                "O nome contém caracteres inválidos.",
            )

        return True, ""

    @staticmethod
    def _validar_endereco(
        *,
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

    # ==========================================================
    # AUXILIARES
    # ==========================================================

    @staticmethod
    def _normalizar_texto(
        valor: Any,
    ) -> str:
        return " ".join(
            str(valor or "").strip().split()
        )

    @staticmethod
    def _id_valido(
        identificador: Any,
    ) -> bool:
        return (
            isinstance(identificador, int)
            and not isinstance(identificador, bool)
            and identificador > 0
        )