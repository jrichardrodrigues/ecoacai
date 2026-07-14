import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from config.settings import DATABASE_PATH


class SQLiteDatabase:
    """Gerencia conexão e estrutura inicial do banco SQLite."""

    def __init__(
        self,
        database_path: Path = DATABASE_PATH,
    ) -> None:
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def conectar(self) -> sqlite3.Connection:
        conexao = sqlite3.connect(
            self.database_path,
        )

        conexao.row_factory = sqlite3.Row

        # O SQLite não ativa chaves estrangeiras por padrão.
        conexao.execute(
            "PRAGMA foreign_keys = ON"
        )

        return conexao

    @contextmanager
    def obter_conexao(
        self,
    ) -> Generator[sqlite3.Connection, None, None]:
        conexao = self.conectar()

        try:
            yield conexao
            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    def inicializar(self) -> None:
        """Cria as tabelas necessárias, caso ainda não existam."""

        with self.obter_conexao() as conexao:
            self._criar_tabela_usuarios(conexao)
            self._criar_tabela_codigos_verificacao(conexao)
            self._criar_tabela_estabelecimentos(conexao)
            self._criar_tabela_solicitacoes(conexao)

    @staticmethod
    def _criar_tabela_usuarios(
        conexao: sqlite3.Connection,
    ) -> None:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL,

                cpf TEXT NOT NULL UNIQUE,

                celular TEXT NOT NULL UNIQUE,

                cep TEXT NOT NULL,

                logradouro TEXT NOT NULL,

                numero TEXT NOT NULL,

                complemento TEXT,

                bairro TEXT NOT NULL,

                cidade TEXT NOT NULL,

                uf TEXT NOT NULL,

                senha_hash TEXT NOT NULL,

                celular_confirmado INTEGER NOT NULL DEFAULT 0
                    CHECK (celular_confirmado IN (0, 1)),

                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    @staticmethod
    def _criar_tabela_codigos_verificacao(
        conexao: sqlite3.Connection,
    ) -> None:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS codigos_verificacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                usuario_id INTEGER,

                celular TEXT NOT NULL,

                codigo_hash TEXT NOT NULL,

                finalidade TEXT NOT NULL
                    CHECK (
                        finalidade IN (
                            'CADASTRO',
                            'RECUPERACAO_SENHA'
                        )
                    ),

                expira_em TEXT NOT NULL,

                usado INTEGER NOT NULL DEFAULT 0
                    CHECK (usado IN (0, 1)),

                tentativas INTEGER NOT NULL DEFAULT 0,

                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE
            )
            """
        )

    @staticmethod
    def _criar_tabela_estabelecimentos(
        conexao: sqlite3.Connection,
    ) -> None:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS estabelecimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL,

                cpf TEXT NOT NULL UNIQUE,

                email TEXT NOT NULL UNIQUE,

                celular TEXT NOT NULL UNIQUE,

                endereco TEXT NOT NULL,

                bairro TEXT NOT NULL,

                setor TEXT NOT NULL,

                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_estabelecimentos_nome
            ON estabelecimentos(nome)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_estabelecimentos_setor
            ON estabelecimentos(setor)
            """
        )

    @staticmethod
    def _criar_tabela_solicitacoes(
        conexao: sqlite3.Connection,
    ) -> None:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS solicitacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                usuario_id INTEGER NOT NULL,

                tipo TEXT NOT NULL
                    CHECK (
                        tipo IN (
                            'SACOS',
                            'BIG_BAG'
                        )
                    ),

                quantidade INTEGER NOT NULL DEFAULT 1
                    CHECK (quantidade > 0),

                status TEXT NOT NULL DEFAULT 'PENDENTE'
                    CHECK (
                        status IN (
                            'PENDENTE',
                            'ACEITA',
                            'EM_COLETA',
                            'CONCLUIDA',
                            'CANCELADA'
                        )
                    ),

                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE RESTRICT
            )
            """
        )