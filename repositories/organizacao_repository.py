from __future__ import annotations

import sqlite3
from typing import Any

from models import Organizacao
from repositories.sqlite_database import SQLiteDatabase


class OrganizacaoRepository:
    """Responsável pela persistência das organizações da ZELURBIS."""

    TIPOS_VALIDOS = {
        "ZELURBIS",
        "GERADOR",
        "EMPRESA_PARCEIRA",
        "PREFEITURA",
        "COOPERATIVA",
    }

    def __init__(
        self,
        database: SQLiteDatabase | None = None,
    ) -> None:
        self.database = database or SQLiteDatabase()

    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================

    @staticmethod
    def _normalizar_texto(valor: str) -> str:
        """Remove espaços excedentes."""

        return " ".join(
            str(valor or "").strip().split()
        )

    @staticmethod
    def _normalizar_documento(documento: str) -> str:
        """Mantém apenas os números do CPF ou CNPJ."""

        return "".join(
            caractere
            for caractere in str(documento or "")
            if caractere.isdigit()
        )

    @staticmethod
    def _normalizar_telefone(telefone: str) -> str:
        """Mantém apenas os números do telefone."""

        return "".join(
            caractere
            for caractere in str(telefone or "")
            if caractere.isdigit()
        )

    @classmethod
    def _normalizar_tipo(cls, tipo: str) -> str:
        """Padroniza e valida o tipo da organização."""

        tipo_normalizado = str(tipo or "").strip().upper()

        if tipo_normalizado not in cls.TIPOS_VALIDOS:
            raise ValueError(
                "Tipo de organização inválido."
            )

        return tipo_normalizado

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        organizacao: Organizacao,
    ) -> Organizacao:
        """Cadastra uma nova organização."""

        tipo = self._normalizar_tipo(
            organizacao.tipo
        )
        nome = self._normalizar_texto(
            organizacao.nome
        )
        documento = self._normalizar_documento(
            organizacao.documento
        )
        email = str(
            organizacao.email or ""
        ).strip().lower()
        telefone = self._normalizar_telefone(
            organizacao.telefone
        )

        if not nome:
            raise ValueError(
                "Informe o nome da organização."
            )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO organizacoes (
                        tipo,
                        nome,
                        documento,
                        email,
                        telefone,
                        ativo
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        tipo,
                        nome,
                        documento,
                        email,
                        telefone,
                        int(organizacao.ativo),
                    ),
                )

                organizacao.id = cursor.lastrowid
                organizacao.tipo = tipo
                organizacao.nome = nome
                organizacao.documento = documento
                organizacao.email = email
                organizacao.telefone = telefone

        except sqlite3.IntegrityError as erro:
            self._tratar_erro_integridade(erro)

        organizacao_salva = self.buscar_por_id(
            organizacao.id
        )

        if organizacao_salva is None:
            raise RuntimeError(
                "A organização foi inserida, "
                "mas não pôde ser recuperada."
            )

        return organizacao_salva

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        organizacao_id: int | None,
    ) -> Organizacao | None:
        """Busca uma organização pelo identificador."""

        if organizacao_id is None:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM organizacoes
                WHERE id = ?
                LIMIT 1
                """,
                (organizacao_id,),
            ).fetchone()

        return self._converter_row(row)

    def buscar_por_documento(
        self,
        documento: str,
    ) -> Organizacao | None:
        """Busca uma organização pelo CPF ou CNPJ."""

        documento_normalizado = (
            self._normalizar_documento(documento)
        )

        if not documento_normalizado:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM organizacoes
                WHERE documento = ?
                LIMIT 1
                """,
                (documento_normalizado,),
            ).fetchone()

        return self._converter_row(row)

    def listar(
        self,
        somente_ativas: bool = True,
    ) -> list[Organizacao]:
        """Lista todas as organizações."""

        consulta = """
            SELECT *
            FROM organizacoes
        """

        if somente_ativas:
            consulta += """
                WHERE ativo = 1
            """

        consulta += """
            ORDER BY nome
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta
            ).fetchall()

        return self._converter_rows(rows)

    def listar_por_tipo(
        self,
        tipo: str,
        somente_ativas: bool = True,
    ) -> list[Organizacao]:
        """Lista as organizações de um determinado tipo."""

        tipo_normalizado = self._normalizar_tipo(
            tipo
        )

        consulta = """
            SELECT *
            FROM organizacoes
            WHERE tipo = ?
        """

        parametros: list[Any] = [
            tipo_normalizado,
        ]

        if somente_ativas:
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

    def pesquisar_por_nome(
        self,
        termo: str,
        *,
        tipo: str | None = None,
        somente_ativas: bool = True,
    ) -> list[Organizacao]:
        """Pesquisa organizações pelo nome."""

        termo_normalizado = self._normalizar_texto(
            termo
        )

        consulta = """
            SELECT *
            FROM organizacoes
            WHERE nome LIKE ?
        """

        parametros: list[Any] = [
            f"%{termo_normalizado}%",
        ]

        if tipo is not None:
            consulta += """
                AND tipo = ?
            """
            parametros.append(
                self._normalizar_tipo(tipo)
            )

        if somente_ativas:
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

    def documento_existe(
        self,
        documento: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se o documento já está cadastrado."""

        documento_normalizado = (
            self._normalizar_documento(documento)
        )

        if not documento_normalizado:
            return False

        consulta = """
            SELECT 1
            FROM organizacoes
            WHERE documento = ?
        """

        parametros: list[Any] = [
            documento_normalizado,
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
        organizacao: Organizacao,
    ) -> Organizacao:
        """Atualiza uma organização existente."""

        if organizacao.id is None:
            raise ValueError(
                "A organização não possui identificador."
            )

        tipo = self._normalizar_tipo(
            organizacao.tipo
        )
        nome = self._normalizar_texto(
            organizacao.nome
        )
        documento = self._normalizar_documento(
            organizacao.documento
        )
        email = str(
            organizacao.email or ""
        ).strip().lower()
        telefone = self._normalizar_telefone(
            organizacao.telefone
        )

        if not nome:
            raise ValueError(
                "Informe o nome da organização."
            )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    UPDATE organizacoes
                    SET
                        tipo = ?,
                        nome = ?,
                        documento = ?,
                        email = ?,
                        telefone = ?,
                        ativo = ?,
                        atualizado_em = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (
                        tipo,
                        nome,
                        documento,
                        email,
                        telefone,
                        int(organizacao.ativo),
                        organizacao.id,
                    ),
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        "Organização não encontrada."
                    )

        except sqlite3.IntegrityError as erro:
            self._tratar_erro_integridade(erro)

        organizacao_atualizada = self.buscar_por_id(
            organizacao.id
        )

        if organizacao_atualizada is None:
            raise RuntimeError(
                "A organização foi atualizada, "
                "mas não pôde ser recuperada."
            )

        return organizacao_atualizada

    # ==========================================================
    # ATIVAÇÃO E DESATIVAÇÃO
    # ==========================================================

    def ativar(
        self,
        organizacao_id: int,
    ) -> bool:
        """Ativa uma organização."""

        return self._alterar_status(
            organizacao_id=organizacao_id,
            ativo=True,
        )

    def desativar(
        self,
        organizacao_id: int,
    ) -> bool:
        """Desativa uma organização sem excluí-la."""

        return self._alterar_status(
            organizacao_id=organizacao_id,
            ativo=False,
        )

    def _alterar_status(
        self,
        *,
        organizacao_id: int,
        ativo: bool,
    ) -> bool:
        """Atualiza o status ativo da organização."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE organizacoes
                SET
                    ativo = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    int(ativo),
                    organizacao_id,
                ),
            )

        return cursor.rowcount > 0

    # ==========================================================
    # CONVERSÃO E ERROS
    # ==========================================================

    @staticmethod
    def _converter_row(
        row: Any,
    ) -> Organizacao | None:
        """Converte uma linha SQLite em Organização."""

        if row is None:
            return None

        return Organizacao.from_row(row)

    @classmethod
    def _converter_rows(
        cls,
        rows: list[Any],
    ) -> list[Organizacao]:
        """Converte várias linhas em organizações."""

        return [
            organizacao
            for row in rows
            if (
                organizacao := cls._converter_row(row)
            ) is not None
        ]

    @staticmethod
    def _tratar_erro_integridade(
        erro: sqlite3.IntegrityError,
    ) -> None:
        """Converte erros do SQLite em mensagens amigáveis."""

        mensagem = str(erro).lower()

        if "organizacoes.documento" in mensagem:
            raise ValueError(
                "Documento já cadastrado para outra organização."
            ) from erro

        if "check constraint failed" in mensagem:
            raise ValueError(
                "Tipo ou situação da organização inválida."
            ) from erro

        raise ValueError(
            "Não foi possível salvar a organização."
        ) from erro