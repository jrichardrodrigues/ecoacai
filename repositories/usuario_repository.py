from __future__ import annotations

import sqlite3
from typing import Any

from models import Usuario
from repositories.sqlite_database import SQLiteDatabase


class UsuarioRepository:
    """
    Responsável pela persistência dos usuários da plataforma.

    O usuário pertence a uma organização e possui um perfil de acesso.
    """

    def __init__(
        self,
        database: SQLiteDatabase | None = None,
    ) -> None:
        self.database = database or SQLiteDatabase()

    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================

    @staticmethod
    def _normalizar_cpf(cpf: str) -> str:
        """Mantém somente os números do CPF."""

        return "".join(
            caractere
            for caractere in str(cpf or "")
            if caractere.isdigit()
        )

    @staticmethod
    def _normalizar_celular(celular: str) -> str:
        """Mantém somente os números do celular."""

        return "".join(
            caractere
            for caractere in str(celular or "")
            if caractere.isdigit()
        )

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        usuario: Usuario,
    ) -> Usuario:
        """
        Cadastra um usuário.

        O usuário deve possuir perfil_id.

        O organizacao_id poderá ser nulo temporariamente durante
        o cadastro público, até a criação da organização vinculada.
        """

        cpf = self._normalizar_cpf(usuario.cpf)
        celular = self._normalizar_celular(usuario.celular)

        if usuario.perfil_id is None:
            raise ValueError(
                "O perfil do usuário não foi informado."
            )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO usuarios (
                        organizacao_id,
                        perfil_id,
                        nome,
                        cpf,
                        celular,
                        cep,
                        logradouro,
                        numero,
                        complemento,
                        bairro,
                        cidade,
                        uf,
                        senha_hash,
                        celular_confirmado,
                        ativo
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?,
                        ?, ?, ?
                    )
                    """,
                    (
                        usuario.organizacao_id,
                        usuario.perfil_id,
                        usuario.nome.strip(),
                        cpf,
                        celular,
                        usuario.cep.strip(),
                        usuario.logradouro.strip(),
                        usuario.numero.strip(),
                        usuario.complemento.strip(),
                        usuario.bairro.strip(),
                        usuario.cidade.strip(),
                        usuario.uf.strip().upper(),
                        usuario.senha_hash,
                        int(usuario.celular_confirmado),
                        int(usuario.ativo),
                    ),
                )

                usuario.id = cursor.lastrowid
                usuario.cpf = cpf
                usuario.celular = celular

        except sqlite3.IntegrityError as erro:
            self._tratar_erro_integridade(erro)

        usuario_salvo = self.buscar_por_id(usuario.id)

        if usuario_salvo is None:
            raise RuntimeError(
                "O usuário foi inserido, "
                "mas não pôde ser recuperado."
            )

        return usuario_salvo

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        usuario_id: int | None,
    ) -> Usuario | None:
        """Busca um usuário pelo identificador."""

        if usuario_id is None:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE id = ?
                LIMIT 1
                """,
                (usuario_id,),
            ).fetchone()

        return self._converter_row(row)

    def buscar_por_cpf(
        self,
        cpf: str,
    ) -> Usuario | None:
        """Busca um usuário pelo CPF."""

        cpf_normalizado = self._normalizar_cpf(cpf)

        if not cpf_normalizado:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE cpf = ?
                LIMIT 1
                """,
                (cpf_normalizado,),
            ).fetchone()

        return self._converter_row(row)

    def buscar_por_celular(
        self,
        celular: str,
    ) -> Usuario | None:
        """Busca um usuário pelo celular."""

        celular_normalizado = self._normalizar_celular(
            celular
        )

        if not celular_normalizado:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE celular = ?
                LIMIT 1
                """,
                (celular_normalizado,),
            ).fetchone()

        return self._converter_row(row)

    def buscar_por_cpf_e_perfil(
        self,
        cpf: str,
        perfil_id: int,
    ) -> Usuario | None:
        """
        Busca um usuário pelo CPF e perfil.

        Será utilizado na autenticação dos portais independentes.
        """

        cpf_normalizado = self._normalizar_cpf(cpf)

        if not cpf_normalizado:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE cpf = ?
                  AND perfil_id = ?
                LIMIT 1
                """,
                (
                    cpf_normalizado,
                    perfil_id,
                ),
            ).fetchone()

        return self._converter_row(row)

    def listar(
        self,
        somente_ativos: bool = True,
    ) -> list[Usuario]:
        """Lista todos os usuários."""

        consulta = """
            SELECT *
            FROM usuarios
        """

        parametros: list[Any] = []

        if somente_ativos:
            consulta += """
                WHERE ativo = 1
            """

        consulta += """
            ORDER BY nome
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return self._converter_rows(rows)

    def listar_por_organizacao(
        self,
        organizacao_id: int,
        somente_ativos: bool = True,
    ) -> list[Usuario]:
        """Lista os usuários vinculados a uma organização."""

        consulta = """
            SELECT *
            FROM usuarios
            WHERE organizacao_id = ?
        """

        parametros: list[Any] = [
            organizacao_id,
        ]

        if somente_ativos:
            consulta += """
                AND ativo = 1
            """

        consulta += """
            ORDER BY nome
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return self._converter_rows(rows)

    def listar_por_perfil(
        self,
        perfil_id: int,
        somente_ativos: bool = True,
    ) -> list[Usuario]:
        """Lista os usuários pertencentes a determinado perfil."""

        consulta = """
            SELECT *
            FROM usuarios
            WHERE perfil_id = ?
        """

        parametros: list[Any] = [
            perfil_id,
        ]

        if somente_ativos:
            consulta += """
                AND ativo = 1
            """

        consulta += """
            ORDER BY nome
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return self._converter_rows(rows)

    def listar_por_organizacao_e_perfil(
        self,
        organizacao_id: int,
        perfil_id: int,
        somente_ativos: bool = True,
    ) -> list[Usuario]:
        """
        Lista usuários de uma organização que possuem
        determinado perfil.
        """

        consulta = """
            SELECT *
            FROM usuarios
            WHERE organizacao_id = ?
              AND perfil_id = ?
        """

        parametros: list[Any] = [
            organizacao_id,
            perfil_id,
        ]

        if somente_ativos:
            consulta += """
                AND ativo = 1
            """

        consulta += """
            ORDER BY nome
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return self._converter_rows(rows)

    # ==========================================================
    # VERIFICAÇÕES
    # ==========================================================

    def cpf_existe(
        self,
        cpf: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se o CPF já está cadastrado."""

        cpf_normalizado = self._normalizar_cpf(cpf)

        if not cpf_normalizado:
            return False

        consulta = """
            SELECT 1
            FROM usuarios
            WHERE cpf = ?
        """

        parametros: list[Any] = [
            cpf_normalizado,
        ]

        if ignorar_id is not None:
            consulta += """
                AND id != ?
            """
            parametros.append(ignorar_id)

        consulta += """
            LIMIT 1
        """

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchone()

        return row is not None

    def celular_existe(
        self,
        celular: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se o celular já está cadastrado."""

        celular_normalizado = self._normalizar_celular(
            celular
        )

        if not celular_normalizado:
            return False

        consulta = """
            SELECT 1
            FROM usuarios
            WHERE celular = ?
        """

        parametros: list[Any] = [
            celular_normalizado,
        ]

        if ignorar_id is not None:
            consulta += """
                AND id != ?
            """
            parametros.append(ignorar_id)

        consulta += """
            LIMIT 1
        """

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchone()

        return row is not None

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def atualizar(
        self,
        usuario: Usuario,
    ) -> Usuario:
        """Atualiza os dados de um usuário."""

        if usuario.id is None:
            raise ValueError(
                "O usuário não possui identificador."
            )

        if usuario.perfil_id is None:
            raise ValueError(
                "O perfil do usuário não foi informado."
            )

        cpf = self._normalizar_cpf(usuario.cpf)
        celular = self._normalizar_celular(
            usuario.celular
        )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    UPDATE usuarios
                    SET
                        organizacao_id = ?,
                        perfil_id = ?,
                        nome = ?,
                        cpf = ?,
                        celular = ?,
                        cep = ?,
                        logradouro = ?,
                        numero = ?,
                        complemento = ?,
                        bairro = ?,
                        cidade = ?,
                        uf = ?,
                        celular_confirmado = ?,
                        ativo = ?,
                        atualizado_em = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (
                        usuario.organizacao_id,
                        usuario.perfil_id,
                        usuario.nome.strip(),
                        cpf,
                        celular,
                        usuario.cep.strip(),
                        usuario.logradouro.strip(),
                        usuario.numero.strip(),
                        usuario.complemento.strip(),
                        usuario.bairro.strip(),
                        usuario.cidade.strip(),
                        usuario.uf.strip().upper(),
                        int(usuario.celular_confirmado),
                        int(usuario.ativo),
                        usuario.id,
                    ),
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        "Usuário não encontrado."
                    )

        except sqlite3.IntegrityError as erro:
            self._tratar_erro_integridade(erro)

        usuario_atualizado = self.buscar_por_id(
            usuario.id
        )

        if usuario_atualizado is None:
            raise RuntimeError(
                "O usuário foi atualizado, "
                "mas não pôde ser recuperado."
            )

        return usuario_atualizado

    def atualizar_senha(
        self,
        usuario_id: int,
        senha_hash: str,
    ) -> bool:
        """Atualiza a senha criptografada do usuário."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE usuarios
                SET
                    senha_hash = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    senha_hash,
                    usuario_id,
                ),
            )

        return cursor.rowcount > 0

    def alterar_organizacao(
        self,
        usuario_id: int,
        organizacao_id: int | None,
    ) -> bool:
        """Altera a organização vinculada ao usuário."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE usuarios
                SET
                    organizacao_id = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    organizacao_id,
                    usuario_id,
                ),
            )

        return cursor.rowcount > 0

    def alterar_perfil(
        self,
        usuario_id: int,
        perfil_id: int,
    ) -> bool:
        """Altera o perfil de acesso do usuário."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE usuarios
                SET
                    perfil_id = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    perfil_id,
                    usuario_id,
                ),
            )

        return cursor.rowcount > 0

    def confirmar_celular(
        self,
        usuario_id: int,
    ) -> bool:
        """Marca o celular do usuário como confirmado."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE usuarios
                SET
                    celular_confirmado = 1,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (usuario_id,),
            )

        return cursor.rowcount > 0

    # ==========================================================
    # ATIVAÇÃO E DESATIVAÇÃO
    # ==========================================================

    def ativar(
        self,
        usuario_id: int,
    ) -> bool:
        """Ativa um usuário."""

        return self._alterar_status(
            usuario_id=usuario_id,
            ativo=True,
        )

    def desativar(
        self,
        usuario_id: int,
    ) -> bool:
        """Desativa um usuário sem excluí-lo fisicamente."""

        return self._alterar_status(
            usuario_id=usuario_id,
            ativo=False,
        )

    def _alterar_status(
        self,
        usuario_id: int,
        ativo: bool,
    ) -> bool:
        """Atualiza o status ativo do usuário."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE usuarios
                SET
                    ativo = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    int(ativo),
                    usuario_id,
                ),
            )

        return cursor.rowcount > 0

    # ==========================================================
    # MÉTODOS AUXILIARES
    # ==========================================================

    @staticmethod
    def _converter_row(
        row: Any,
    ) -> Usuario | None:
        """Converte uma linha do SQLite em Usuario."""

        if row is None:
            return None

        return Usuario.from_row(row)

    @classmethod
    def _converter_rows(
        cls,
        rows: list[Any],
    ) -> list[Usuario]:
        """Converte várias linhas do SQLite em usuários."""

        return [
            usuario
            for row in rows
            if (
                usuario := cls._converter_row(row)
            ) is not None
        ]

    @staticmethod
    def _tratar_erro_integridade(
        erro: sqlite3.IntegrityError,
    ) -> None:
        """Converte erros técnicos do SQLite em mensagens amigáveis."""

        mensagem = str(erro).lower()

        if "usuarios.cpf" in mensagem:
            raise ValueError(
                "CPF já cadastrado."
            ) from erro

        if "usuarios.celular" in mensagem:
            raise ValueError(
                "Celular já cadastrado."
            ) from erro

        if (
            "foreign key constraint failed"
            in mensagem
        ):
            raise ValueError(
                "A organização ou o perfil informado "
                "não existe."
            ) from erro

        if "usuarios.perfil_id" in mensagem:
            raise ValueError(
                "O perfil do usuário é obrigatório."
            ) from erro

        raise ValueError(
            "Não foi possível salvar o usuário."
        ) from erro