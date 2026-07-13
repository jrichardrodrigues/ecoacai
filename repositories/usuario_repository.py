import sqlite3

from models import Usuario
from repositories.sqlite_database import SQLiteDatabase


class UsuarioRepository:
    """Persistência de usuários no SQLite."""

    def __init__(self, database: SQLiteDatabase | None = None):
        self.database = database or SQLiteDatabase()

    @staticmethod
    def _normalizar_cpf(cpf: str) -> str:
        return "".join(
            caractere
            for caractere in str(cpf or "")
            if caractere.isdigit()
        )

    @staticmethod
    def _normalizar_celular(celular: str) -> str:
        return "".join(
            caractere
            for caractere in str(celular or "")
            if caractere.isdigit()
        )

    def cadastrar(self, usuario: Usuario) -> Usuario:
        cpf = self._normalizar_cpf(usuario.cpf)
        celular = self._normalizar_celular(usuario.celular)

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO usuarios (
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
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
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
            mensagem = str(erro).lower()

            if "usuarios.cpf" in mensagem:
                raise ValueError("CPF já cadastrado.") from erro

            if "usuarios.celular" in mensagem:
                raise ValueError("Celular já cadastrado.") from erro

            raise ValueError("Não foi possível cadastrar o usuário.") from erro

        usuario_salvo = self.buscar_por_id(usuario.id)

        if usuario_salvo is None:
            raise RuntimeError("O usuário foi inserido, mas não pôde ser recuperado.")

        return usuario_salvo

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            ).fetchone()

        return Usuario.from_row(row) if row else None

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        cpf_normalizado = self._normalizar_cpf(cpf)

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE cpf = ?
                """,
                (cpf_normalizado,),
            ).fetchone()

        return Usuario.from_row(row) if row else None

    def buscar_por_celular(self, celular: str) -> Usuario | None:
        celular_normalizado = self._normalizar_celular(celular)

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE celular = ?
                """,
                (celular_normalizado,),
            ).fetchone()

        return Usuario.from_row(row) if row else None

    def cpf_existe(self, cpf: str, ignorar_id: int | None = None) -> bool:
        cpf_normalizado = self._normalizar_cpf(cpf)

        consulta = """
            SELECT 1
            FROM usuarios
            WHERE cpf = ?
        """
        parametros: list = [cpf_normalizado]

        if ignorar_id is not None:
            consulta += " AND id != ?"
            parametros.append(ignorar_id)

        consulta += " LIMIT 1"

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
        celular_normalizado = self._normalizar_celular(celular)

        consulta = """
            SELECT 1
            FROM usuarios
            WHERE celular = ?
        """
        parametros: list = [celular_normalizado]

        if ignorar_id is not None:
            consulta += " AND id != ?"
            parametros.append(ignorar_id)

        consulta += " LIMIT 1"

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchone()

        return row is not None

    def listar(self, somente_ativos: bool = True) -> list[Usuario]:
        consulta = "SELECT * FROM usuarios"

        if somente_ativos:
            consulta += " WHERE ativo = 1"

        consulta += " ORDER BY nome"

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(consulta).fetchall()

        return [
            Usuario.from_row(row)
            for row in rows
        ]