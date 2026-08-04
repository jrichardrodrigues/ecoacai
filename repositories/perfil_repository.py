from __future__ import annotations

from typing import Any

from models import Perfil
from repositories.sqlite_database import SQLiteDatabase


class PerfilRepository:
    """Responsável pela persistência e consulta dos perfis de acesso."""

    def __init__(
        self,
        database: SQLiteDatabase | None = None,
    ) -> None:
        self.database = database or SQLiteDatabase()

    @staticmethod
    def _normalizar_codigo(codigo: str) -> str:
        """Padroniza o código do perfil."""

        return str(codigo or "").strip().upper()

    def buscar_por_id(
        self,
        perfil_id: int | None,
    ) -> Perfil | None:
        """Busca um perfil pelo identificador."""

        if perfil_id is None:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM perfis
                WHERE id = ?
                LIMIT 1
                """,
                (perfil_id,),
            ).fetchone()

        return Perfil.from_row(row) if row else None

    def buscar_por_codigo(
        self,
        codigo: str,
    ) -> Perfil | None:
        """Busca um perfil pelo código oficial."""

        codigo_normalizado = self._normalizar_codigo(codigo)

        if not codigo_normalizado:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM perfis
                WHERE codigo = ?
                LIMIT 1
                """,
                (codigo_normalizado,),
            ).fetchone()

        return Perfil.from_row(row) if row else None

    def buscar_id_por_codigo(
        self,
        codigo: str,
    ) -> int | None:
        """Retorna somente o identificador do perfil."""

        perfil = self.buscar_por_codigo(codigo)

        return perfil.id if perfil else None

    def listar(
        self,
        somente_ativos: bool = True,
    ) -> list[Perfil]:
        """Lista os perfis cadastrados."""

        consulta = """
            SELECT *
            FROM perfis
        """

        if somente_ativos:
            consulta += """
                WHERE ativo = 1
            """

        consulta += """
            ORDER BY nome
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(consulta).fetchall()

        return [
            Perfil.from_row(row)
            for row in rows
        ]

    def existe(
        self,
        codigo: str,
    ) -> bool:
        """Verifica se existe um perfil com o código informado."""

        codigo_normalizado = self._normalizar_codigo(codigo)

        if not codigo_normalizado:
            return False

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT 1
                FROM perfis
                WHERE codigo = ?
                LIMIT 1
                """,
                (codigo_normalizado,),
            ).fetchone()

        return row is not None

    def definir_ativo(
        self,
        perfil_id: int,
        ativo: bool,
    ) -> bool:
        """Ativa ou desativa um perfil."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE perfis
                SET
                    ativo = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    int(ativo),
                    perfil_id,
                ),
            )

        return cursor.rowcount > 0