import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from config.settings import DATABASE_PATH


class SQLiteDatabase:
    """Gerencia a conexão e a estrutura do banco SQLite."""

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
        """Abre e configura uma conexão SQLite."""

        conexao = sqlite3.connect(
            self.database_path,
        )

        conexao.row_factory = sqlite3.Row

        # O SQLite não ativa as chaves estrangeiras por padrão.
        conexao.execute(
            "PRAGMA foreign_keys = ON"
        )

        return conexao

    @contextmanager
    def obter_conexao(
        self,
    ) -> Generator[sqlite3.Connection, None, None]:
        """Fornece uma conexão com commit e rollback automáticos."""

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
        """Cria e atualiza as tabelas necessárias."""

        with self.obter_conexao() as conexao:
            self._criar_tabela_schema_version(conexao)

            self._criar_tabela_organizacoes(conexao)
            self._criar_tabela_perfis(conexao)
            self._inserir_perfis_iniciais(conexao)
            self._criar_organizacao_administracao(conexao)
            self._garantir_tabela_usuarios(conexao)

            self._criar_tabela_codigos_verificacao(conexao)
            self._criar_tabela_estabelecimentos(conexao)

            self._garantir_tabela_motoristas(conexao)
            self._garantir_tabela_veiculos(conexao)
            self._garantir_tabela_solicitacoes(conexao)

            self._registrar_versao_schema(
                conexao,
                versao=2,
                descricao=(
                    "Modelo organizacional: organizações, perfis e "
                    "vínculos de usuários"
                ),
            )

            self._registrar_versao_schema(
                conexao,
                versao=3,
                descricao=(
                    "UC-002: evolução das solicitações para o "
                    "modelo operacional da ZELURBIS"
                ),
            )

    # ==========================================================
    # CONTROLE DE VERSÃO DO BANCO
    # ==========================================================

    @staticmethod
    def _criar_tabela_schema_version(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria o histórico de versões estruturais do banco."""

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                versao INTEGER PRIMARY KEY,
                descricao TEXT NOT NULL,
                aplicado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    @staticmethod
    def _registrar_versao_schema(
        conexao: sqlite3.Connection,
        *,
        versao: int,
        descricao: str,
    ) -> None:
        """Registra uma migração sem duplicar versões já aplicadas."""

        conexao.execute(
            """
            INSERT OR IGNORE INTO schema_version (
                versao,
                descricao
            )
            VALUES (?, ?)
            """,
            (versao, descricao),
        )

    # ==========================================================
    # ORGANIZAÇÕES
    # ==========================================================

    @staticmethod
    def _criar_tabela_organizacoes(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria as organizações participantes da plataforma."""

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS organizacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                tipo TEXT NOT NULL
                    CHECK (
                        tipo IN (
                            'ZELURBIS',
                            'GERADOR',
                            'EMPRESA_PARCEIRA',
                            'PREFEITURA',
                            'COOPERATIVA'
                        )
                    ),

                nome TEXT NOT NULL,
                documento TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                telefone TEXT NOT NULL DEFAULT '',

                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_organizacoes_tipo
            ON organizacoes(tipo)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_organizacoes_nome
            ON organizacoes(nome)
            """
        )

        conexao.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_organizacoes_documento_unico
            ON organizacoes(documento)
            WHERE TRIM(documento) <> ''
            """
        )

    @staticmethod
    def _criar_organizacao_administracao(
        conexao: sqlite3.Connection,
    ) -> None:
        """Garante a organização interna da administração ZELURBIS."""

        conexao.execute(
            """
            INSERT INTO organizacoes (
                tipo,
                nome,
                documento,
                email,
                telefone,
                ativo
            )
            SELECT
                'ZELURBIS',
                'Administração ZELURBIS',
                '',
                '',
                '',
                1
            WHERE NOT EXISTS (
                SELECT 1
                FROM organizacoes
                WHERE tipo = 'ZELURBIS'
                  AND nome = 'Administração ZELURBIS'
            )
            """
        )

    # ==========================================================
    # PERFIS
    # ==========================================================

    @staticmethod
    def _criar_tabela_perfis(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria os perfis de acesso da plataforma."""

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS perfis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL DEFAULT '',

                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    @staticmethod
    def _inserir_perfis_iniciais(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cadastra os perfis oficiais sem gerar duplicidade."""

        perfis = (
            (
                'GESTOR',
                'Gestor do Sistema',
                'Administra e acompanha todo o ecossistema.',
            ),
            (
                'GERADOR',
                'Gerador do Resíduo',
                'Solicita e acompanha as próprias coletas.',
            ),
            (
                'EMPRESA_PARCEIRA',
                'Empresa Parceira',
                'Executa as operações designadas à organização.',
            ),
        )

        conexao.executemany(
            """
            INSERT OR IGNORE INTO perfis (
                codigo,
                nome,
                descricao
            )
            VALUES (?, ?, ?)
            """,
            perfis,
        )

    # ==========================================================
    # USUÁRIOS
    # ==========================================================

    @classmethod
    def _garantir_tabela_usuarios(
        cls,
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria ou migra usuários para o modelo organizacional."""

        if not cls._tabela_existe(conexao, 'usuarios'):
            cls._criar_tabela_usuarios(conexao)
        else:
            colunas = cls._obter_colunas(conexao, 'usuarios')

            # Para bancos existentes, o ALTER TABLE preserva os dados e
            # evita conflitos com codigos_verificacao, que referencia usuários.
            if 'organizacao_id' not in colunas:
                conexao.execute(
                    """
                    ALTER TABLE usuarios
                    ADD COLUMN organizacao_id INTEGER
                    """
                )

            if 'perfil_id' not in colunas:
                conexao.execute(
                    """
                    ALTER TABLE usuarios
                    ADD COLUMN perfil_id INTEGER
                    """
                )

        cls._vincular_usuarios_legados(conexao)
        cls._criar_indices_usuarios(conexao)

    @staticmethod
    def _criar_tabela_usuarios(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria a estrutura atual da tabela de usuários."""

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                organizacao_id INTEGER,
                perfil_id INTEGER,

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
                atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (organizacao_id)
                    REFERENCES organizacoes(id)
                    ON DELETE RESTRICT,

                FOREIGN KEY (perfil_id)
                    REFERENCES perfis(id)
                    ON DELETE RESTRICT
            )
            """
        )

    @staticmethod
    def _vincular_usuarios_legados(
        conexao: sqlite3.Connection,
    ) -> None:
        """Vincula usuários sem contexto ao gestor da ZELURBIS."""

        organizacao = conexao.execute(
            """
            SELECT id
            FROM organizacoes
            WHERE tipo = 'ZELURBIS'
              AND nome = 'Administração ZELURBIS'
            LIMIT 1
            """
        ).fetchone()

        perfil = conexao.execute(
            """
            SELECT id
            FROM perfis
            WHERE codigo = 'GESTOR'
            LIMIT 1
            """
        ).fetchone()

        if organizacao is None or perfil is None:
            raise RuntimeError(
                'Não foi possível preparar organização e perfil padrão.'
            )

        conexao.execute(
            """
            UPDATE usuarios
            SET organizacao_id = COALESCE(organizacao_id, ?),
                perfil_id = COALESCE(perfil_id, ?)
            WHERE organizacao_id IS NULL
               OR perfil_id IS NULL
            """,
            (organizacao['id'], perfil['id']),
        )

    @staticmethod
    def _criar_indices_usuarios(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria índices para vínculos organizacionais e de acesso."""

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_usuarios_organizacao
            ON usuarios(organizacao_id)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_usuarios_perfil
            ON usuarios(perfil_id)
            """
        )

    # ==========================================================
    # MOTORISTAS
    # ==========================================================

    @classmethod
    def _garantir_tabela_motoristas(
        cls,
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria ou migra a tabela de motoristas."""

        if not cls._tabela_existe(
            conexao,
            "motoristas",
        ):
            cls._criar_tabela_motoristas(conexao)
            cls._criar_indices_motoristas(conexao)
            return

        colunas = cls._obter_colunas(
            conexao,
            "motoristas",
        )

        colunas_atuais = {
            "id",
            "nome",
            "telefone",
            "cnh",
            "categoria_cnh",
            "ativo",
            "criado_em",
            "atualizado_em",
        }

        colunas_legadas = {
            "cpf",
            "email",
            "observacao",
        }

        estrutura_legada = bool(
            colunas.intersection(colunas_legadas)
        )

        estrutura_incompleta = not colunas_atuais.issubset(
            colunas,
        )

        if estrutura_legada or estrutura_incompleta:
            cls._migrar_tabela_motoristas(
                conexao,
                colunas,
            )

        cls._criar_indices_motoristas(conexao)

    @staticmethod
    def _criar_tabela_motoristas(
        conexao: sqlite3.Connection,
        nome_tabela: str = "motoristas",
    ) -> None:
        """Cria a estrutura atual da tabela de motoristas."""

        conexao.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL,

                telefone TEXT NOT NULL DEFAULT '',

                cnh TEXT NOT NULL DEFAULT '',

                categoria_cnh TEXT NOT NULL DEFAULT '',

                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                criado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                atualizado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    @classmethod
    def _migrar_tabela_motoristas(
        cls,
        conexao: sqlite3.Connection,
        colunas_antigas: set[str],
    ) -> None:
        """
        Reconstrói a tabela de motoristas na estrutura atual.

        CPF, e-mail e observação pertenciam à estrutura anterior e
        são descartados. Os campos compatíveis são preservados.
        """

        conexao.execute(
            "DROP TABLE IF EXISTS motoristas_nova"
        )

        cls._criar_tabela_motoristas(
            conexao,
            nome_tabela="motoristas_nova",
        )

        id_coluna = (
            "id"
            if "id" in colunas_antigas
            else "NULL"
        )

        nome = (
            "COALESCE(nome, '')"
            if "nome" in colunas_antigas
            else "''"
        )

        telefone = (
            "COALESCE(telefone, '')"
            if "telefone" in colunas_antigas
            else "''"
        )

        cnh = (
            "COALESCE(cnh, '')"
            if "cnh" in colunas_antigas
            else "''"
        )

        categoria_cnh = (
            "COALESCE(categoria_cnh, '')"
            if "categoria_cnh" in colunas_antigas
            else "''"
        )

        ativo = (
            "CASE WHEN ativo = 0 THEN 0 ELSE 1 END"
            if "ativo" in colunas_antigas
            else "1"
        )

        criado_em = (
            "COALESCE(criado_em, CURRENT_TIMESTAMP)"
            if "criado_em" in colunas_antigas
            else "CURRENT_TIMESTAMP"
        )

        atualizado_em = (
            "COALESCE(atualizado_em, CURRENT_TIMESTAMP)"
            if "atualizado_em" in colunas_antigas
            else "CURRENT_TIMESTAMP"
        )

        conexao.execute(
            f"""
            INSERT INTO motoristas_nova (
                id,
                nome,
                telefone,
                cnh,
                categoria_cnh,
                ativo,
                criado_em,
                atualizado_em
            )
            SELECT
                {id_coluna},
                {nome},
                {telefone},
                {cnh},
                {categoria_cnh},
                {ativo},
                {criado_em},
                {atualizado_em}
            FROM motoristas
            """
        )

        conexao.execute(
            "DROP TABLE motoristas"
        )

        conexao.execute(
            """
            ALTER TABLE motoristas_nova
            RENAME TO motoristas
            """
        )

    @staticmethod
    def _criar_indices_motoristas(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria índices de consulta e unicidade dos motoristas."""

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_motoristas_nome
            ON motoristas(nome)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_motoristas_ativo
            ON motoristas(ativo)
            """
        )

        # Índices parciais preservam registros legados vazios,
        # mas impedem duplicidade em novos dados válidos.
        conexao.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_motoristas_telefone_unico
            ON motoristas(telefone)
            WHERE TRIM(telefone) <> ''
            """
        )

        conexao.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_motoristas_cnh_unica
            ON motoristas(cnh)
            WHERE TRIM(cnh) <> ''
            """
        )

    # ==========================================================
    # VEÍCULOS
    # ==========================================================

    @classmethod
    def _garantir_tabela_veiculos(
            cls,
            conexao: sqlite3.Connection,
    ) -> None:
        """Cria ou migra a tabela de veículos."""

        if not cls._tabela_existe(
                conexao,
                "veiculos",
        ):
            cls._criar_tabela_veiculos(conexao)
            cls._criar_indices_veiculos(conexao)
            return

        colunas = cls._obter_colunas(
            conexao,
            "veiculos",
        )

        colunas_atuais = {
            "id",
            "placa",
            "marca",
            "modelo",
            "ano",
            "tipo",
            "capacidade",
            "motorista_id",
            "status",
            "ativo",
            "criado_em",
            "atualizado_em",
        }

        estrutura_incompleta = not colunas_atuais.issubset(colunas)

        if estrutura_incompleta:
            cls._migrar_tabela_veiculos(
                conexao,
                colunas,
            )

        cls._criar_indices_veiculos(conexao)

    @staticmethod
    def _criar_tabela_veiculos(
            conexao: sqlite3.Connection,
            nome_tabela: str = "veiculos",
    ) -> None:
        """Cria a estrutura atual da tabela de veículos."""

        conexao.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                placa TEXT NOT NULL,

                marca TEXT NOT NULL,

                modelo TEXT NOT NULL,

                ano INTEGER,

                tipo TEXT NOT NULL,

                capacidade REAL NOT NULL DEFAULT 0,

                motorista_id INTEGER,

                status TEXT NOT NULL DEFAULT 'DISPONIVEL',

                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                criado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                atualizado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (motorista_id)
                    REFERENCES motoristas(id)
                    ON DELETE SET NULL
            )
            """
        )

    @classmethod
    def _migrar_tabela_veiculos(
            cls,
            conexao: sqlite3.Connection,
            colunas_antigas: set[str],
    ) -> None:
        """
        Reconstrói a tabela de veículos na estrutura atual.
        """

        conexao.execute(
            "DROP TABLE IF EXISTS veiculos_nova"
        )

        cls._criar_tabela_veiculos(
            conexao,
            nome_tabela="veiculos_nova",
        )

        id_coluna = (
            "id"
            if "id" in colunas_antigas
            else "NULL"
        )

        placa = (
            "COALESCE(placa, '')"
            if "placa" in colunas_antigas
            else "''"
        )

        marca = (
            "COALESCE(marca, '')"
            if "marca" in colunas_antigas
            else "''"
        )

        modelo = (
            "COALESCE(modelo, '')"
            if "modelo" in colunas_antigas
            else "''"
        )

        ano = (
            "ano"
            if "ano" in colunas_antigas
            else "NULL"
        )

        tipo = (
            "COALESCE(tipo, '')"
            if "tipo" in colunas_antigas
            else "''"
        )

        capacidade = (
            "COALESCE(capacidade, 0)"
            if "capacidade" in colunas_antigas
            else "0"
        )

        motorista_id = (
            "motorista_id"
            if "motorista_id" in colunas_antigas
            else "NULL"
        )

        status = (
            "COALESCE(status, 'DISPONIVEL')"
            if "status" in colunas_antigas
            else "'DISPONIVEL'"
        )

        ativo = (
            "CASE WHEN ativo = 0 THEN 0 ELSE 1 END"
            if "ativo" in colunas_antigas
            else "1"
        )

        criado_em = (
            "COALESCE(criado_em, CURRENT_TIMESTAMP)"
            if "criado_em" in colunas_antigas
            else "CURRENT_TIMESTAMP"
        )

        atualizado_em = (
            "COALESCE(atualizado_em, CURRENT_TIMESTAMP)"
            if "atualizado_em" in colunas_antigas
            else "CURRENT_TIMESTAMP"
        )

        conexao.execute(
            f"""
            INSERT INTO veiculos_nova (
                id,
                placa,
                marca,
                modelo,
                ano,
                tipo,
                capacidade,
                motorista_id,
                status,
                ativo,
                criado_em,
                atualizado_em
            )
            SELECT
                {id_coluna},
                {placa},
                {marca},
                {modelo},
                {ano},
                {tipo},
                {capacidade},
                {motorista_id},
                {status},
                {ativo},
                {criado_em},
                {atualizado_em}
            FROM veiculos
            """
        )

        conexao.execute(
            "DROP TABLE veiculos"
        )

        conexao.execute(
            """
            ALTER TABLE veiculos_nova
            RENAME TO veiculos
            """
        )

    @staticmethod
    def _criar_indices_veiculos(
            conexao: sqlite3.Connection,
    ) -> None:
        """Cria os índices da tabela de veículos."""

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_veiculos_marca
            ON veiculos(marca)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_veiculos_modelo
            ON veiculos(modelo)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_veiculos_motorista
            ON veiculos(motorista_id)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_veiculos_status
            ON veiculos(status)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_veiculos_ativo
            ON veiculos(ativo)
            """
        )

        conexao.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_veiculos_placa_unica
            ON veiculos(placa)
            WHERE TRIM(placa) <> ''
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

    @classmethod
    def _garantir_tabela_solicitacoes(
        cls,
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria ou migra a tabela de solicitações de coleta."""

        if not cls._tabela_existe(
            conexao,
            "solicitacoes",
        ):
            cls._criar_tabela_solicitacoes(conexao)
            cls._criar_indices_solicitacoes(conexao)
            return

        colunas = cls._obter_colunas(
            conexao,
            "solicitacoes",
        )

        colunas_atuais = {
            "id",
            "codigo",
            "organizacao_id",
            "empresa_parceira_id",
            "usuario_criacao_id",
            "estabelecimento_id",
            "motorista_id",
            "veiculo_id",
            "tipo_residuo",
            "unidade_medida",
            "origem",
            "quantidade_sacas_prevista",
            "quantidade_kg_previsto",
            "quantidade_sacas_coletada",
            "quantidade_kg_coletado",
            "status",
            "prioridade",
            "data_solicitacao",
            "data_hora_agendada",
            "data_hora_inicio",
            "data_hora_chegada",
            "data_hora_conclusao",
            "observacao_cliente",
            "observacao_operacional",
            "latitude",
            "longitude",
            "ativo",
            "criado_em",
            "atualizado_em",
            "forma_acondicionamento",
            "quantidade_prevista",
            "peso_estimado_kg",
            "tipo_operacao",
        }

        # Apenas nomes realmente pertencentes a estruturas antigas.
        # Não inclua aqui colunas que também existem na estrutura atual,
        # pois isso provocaria uma migração a cada inicialização.
        colunas_legadas = {
            "usuario_id",
            "tipo",
            "quantidade",
            "observacao",
            "data-hora_agendada",
        }

        estrutura_incompleta = not colunas_atuais.issubset(
            colunas,
        )

        estrutura_legada = bool(
            colunas.intersection(colunas_legadas)
        )

        if estrutura_incompleta or estrutura_legada:
            cls._migrar_tabela_solicitacoes(
                conexao,
                colunas,
            )

        cls._adicionar_coluna_se_nao_existir(
            conexao,
            "solicitacoes",
            "forma_acondicionamento",
            "TEXT NOT NULL DEFAULT 'SACA'",
        )

        cls._adicionar_coluna_se_nao_existir(
            conexao,
            "solicitacoes",
            "quantidade_prevista",
            "INTEGER NOT NULL DEFAULT 0",
        )

        cls._adicionar_coluna_se_nao_existir(
            conexao,
            "solicitacoes",
            "peso_estimado_kg",
            "REAL NOT NULL DEFAULT 0",
        )

        cls._adicionar_coluna_se_nao_existir(
            conexao,
            "solicitacoes",
            "tipo_operacao",
            "TEXT NOT NULL DEFAULT 'MANUAL'",
        )

        cls._adicionar_coluna_se_nao_existir(
            conexao,
            "solicitacoes",
            "motivo_recusa",
            "TEXT",
        )

        cls._adicionar_coluna_se_nao_existir(
            conexao,
            "solicitacoes",
            "data_hora_recusa",
            "TEXT",
        )

        cls._adicionar_coluna_se_nao_existir(
            conexao,
            "solicitacoes",
            "data_hora_exclusao",
            "TEXT",
        )

        cls._preencher_codigos_solicitacoes(conexao)
        cls._criar_indices_solicitacoes(conexao)

    @staticmethod
    def _tabela_existe(
        conexao: sqlite3.Connection,
        nome_tabela: str,
    ) -> bool:
        row = conexao.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            LIMIT 1
            """,
            (nome_tabela,),
        ).fetchone()

        return row is not None

    @staticmethod
    def _obter_colunas(
        conexao: sqlite3.Connection,
        nome_tabela: str,
    ) -> set[str]:
        rows = conexao.execute(
            f"PRAGMA table_info({nome_tabela})"
        ).fetchall()

        return {
            str(row["name"])
            for row in rows
        }

    @staticmethod
    def _adicionar_coluna_se_nao_existir(
            conexao: sqlite3.Connection,
            tabela: str,
            coluna: str,
            definicao: str,
    ) -> None:
        """
        Adiciona uma coluna somente se ela ainda não existir.
        """

        colunas = SQLiteDatabase._obter_colunas(
            conexao,
            tabela,
        )

        if coluna in colunas:
            return

        conexao.execute(
            f"""
            ALTER TABLE {tabela}
            ADD COLUMN {coluna} {definicao}
            """
        )

    @staticmethod
    def _criar_tabela_solicitacoes(
        conexao: sqlite3.Connection,
        nome_tabela: str = "solicitacoes",
    ) -> None:
        """Cria a estrutura atual das solicitações."""

        conexao.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                codigo TEXT UNIQUE,

                organizacao_id INTEGER,

                empresa_parceira_id INTEGER,

                usuario_criacao_id INTEGER,

                estabelecimento_id INTEGER,

                motorista_id INTEGER,

                veiculo_id INTEGER,

                tipo_residuo TEXT NOT NULL
                    DEFAULT 'CAROCO_ACAI',

                unidade_medida TEXT NOT NULL
                    DEFAULT 'SACAS'
                    CHECK (
                        unidade_medida IN (
                            'SACAS',
                            'KG',
                            'UNIDADES',
                            'M3',
                            'CACAMBAS'
                        )
                    ),

                origem TEXT NOT NULL
                    DEFAULT 'GERADOR'
                    CHECK (
                        origem IN (
                            'GERADOR',
                            'GESTOR',
                            'APP',
                            'API'
                        )
                    ),

                quantidade_sacas_prevista INTEGER NOT NULL
                    DEFAULT 1
                    CHECK (quantidade_sacas_prevista > 0),

                quantidade_kg_previsto REAL NOT NULL
                    DEFAULT 0
                    CHECK (quantidade_kg_previsto >= 0),

                quantidade_sacas_coletada INTEGER NOT NULL
                    DEFAULT 0
                    CHECK (quantidade_sacas_coletada >= 0),

                quantidade_kg_coletado REAL NOT NULL
                    DEFAULT 0
                    CHECK (quantidade_kg_coletado >= 0),

                status TEXT NOT NULL
                    DEFAULT 'SOLICITADA'
                    CHECK (
                        status IN (
                            'SOLICITADA',
                            'EM_ANALISE',
                            'AGENDADA',
                            'EM_DESLOCAMENTO',
                            'EM_COLETA',
                            'CONCLUIDA',
                            'CANCELADA',
                            'RECUSADA'
                        )
                    ),

                prioridade TEXT NOT NULL
                    DEFAULT 'NORMAL'
                    CHECK (
                        prioridade IN (
                            'NORMAL',
                            'URGENTE',
                            'PROGRAMADA'
                        )
                    ),

                data_solicitacao TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                data_hora_agendada TEXT,

                data_hora_inicio TEXT,

                data_hora_chegada TEXT,

                data_hora_conclusao TEXT,

                observacao_cliente TEXT NOT NULL
                    DEFAULT '',
                
                observacao_operacional TEXT NOT NULL
                    DEFAULT '',
                
                motivo_cancelamento TEXT,
                
                data_hora_cancelamento TEXT,
                
                motivo_recusa TEXT,
                
                data_hora_recusa TEXT,

                data_hora_exclusao TEXT,
                
                latitude REAL,
                
                longitude REAL,

                ativo INTEGER NOT NULL
                    DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                criado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                atualizado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                CHECK (
                    organizacao_id IS NOT NULL
                    OR estabelecimento_id IS NOT NULL
                ),

                FOREIGN KEY (organizacao_id)
                    REFERENCES organizacoes(id)
                    ON DELETE RESTRICT,

                FOREIGN KEY (empresa_parceira_id)
                    REFERENCES organizacoes(id)
                    ON DELETE SET NULL,

                FOREIGN KEY (usuario_criacao_id)
                    REFERENCES usuarios(id)
                    ON DELETE SET NULL,

                FOREIGN KEY (estabelecimento_id)
                    REFERENCES estabelecimentos(id)
                    ON DELETE RESTRICT,

                FOREIGN KEY (motorista_id)
                    REFERENCES motoristas(id)
                    ON DELETE SET NULL,

                FOREIGN KEY (veiculo_id)
                    REFERENCES veiculos(id)
                    ON DELETE SET NULL
            )
            """
        )

    @classmethod
    def _migrar_tabela_solicitacoes(
        cls,
        conexao: sqlite3.Connection,
        colunas_antigas: set[str],
    ) -> None:
        """Reconstrói solicitações preservando os dados compatíveis."""

        conexao.execute(
            "DROP TABLE IF EXISTS solicitacoes_nova"
        )

        cls._criar_tabela_solicitacoes(
            conexao,
            nome_tabela="solicitacoes_nova",
        )

        def coluna(
            nome: str,
            expressao: str,
            padrao: str,
        ) -> str:
            return (
                expressao
                if nome in colunas_antigas
                else padrao
            )

        organizacao_id = coluna(
            "organizacao_id",
            """
            CASE
                WHEN s.organizacao_id IS NOT NULL
                 AND EXISTS (
                    SELECT 1
                    FROM organizacoes AS o
                    WHERE o.id = s.organizacao_id
                 )
                THEN s.organizacao_id
                ELSE NULL
            END
            """,
            "NULL",
        )

        estabelecimento_id = coluna(
            "estabelecimento_id",
            """
            CASE
                WHEN s.estabelecimento_id IS NOT NULL
                 AND EXISTS (
                    SELECT 1
                    FROM estabelecimentos AS e
                    WHERE e.id = s.estabelecimento_id
                 )
                THEN s.estabelecimento_id
                ELSE NULL
            END
            """,
            "NULL",
        )

        empresa_parceira_id = coluna(
            "empresa_parceira_id",
            """
            CASE
                WHEN s.empresa_parceira_id IS NOT NULL
                 AND EXISTS (
                    SELECT 1
                    FROM organizacoes AS o
                    WHERE o.id = s.empresa_parceira_id
                      AND o.tipo = 'EMPRESA_PARCEIRA'
                 )
                THEN s.empresa_parceira_id
                ELSE NULL
            END
            """,
            "NULL",
        )

        usuario_criacao_id = coluna(
            "usuario_criacao_id",
            """
            CASE
                WHEN s.usuario_criacao_id IS NOT NULL
                 AND EXISTS (
                    SELECT 1
                    FROM usuarios AS u
                    WHERE u.id = s.usuario_criacao_id
                 )
                THEN s.usuario_criacao_id
                ELSE NULL
            END
            """,
            "NULL",
        )

        motorista_id = coluna(
            "motorista_id",
            """
            CASE
                WHEN s.motorista_id IS NOT NULL
                 AND EXISTS (
                    SELECT 1
                    FROM motoristas AS m
                    WHERE m.id = s.motorista_id
                 )
                THEN s.motorista_id
                ELSE NULL
            END
            """,
            "NULL",
        )

        veiculo_id = coluna(
            "veiculo_id",
            """
            CASE
                WHEN s.veiculo_id IS NOT NULL
                 AND EXISTS (
                    SELECT 1
                    FROM veiculos AS v
                    WHERE v.id = s.veiculo_id
                 )
                THEN s.veiculo_id
                ELSE NULL
            END
            """,
            "NULL",
        )

        codigo = coluna(
            "codigo",
            "NULLIF(TRIM(s.codigo), '')",
            "NULL",
        )

        tipo_residuo = coluna(
            "tipo_residuo",
            """
            COALESCE(
                NULLIF(TRIM(s.tipo_residuo), ''),
                'CAROCO_ACAI'
            )
            """,
            "'CAROCO_ACAI'",
        )

        unidade_medida = coluna(
            "unidade_medida",
            """
            CASE UPPER(COALESCE(s.unidade_medida, 'SACAS'))
                WHEN 'KG' THEN 'KG'
                WHEN 'UNIDADES' THEN 'UNIDADES'
                WHEN 'M3' THEN 'M3'
                WHEN 'CACAMBAS' THEN 'CACAMBAS'
                ELSE 'SACAS'
            END
            """,
            "'SACAS'",
        )

        origem = coluna(
            "origem",
            """
            CASE UPPER(COALESCE(s.origem, 'GERADOR'))
                WHEN 'GESTOR' THEN 'GESTOR'
                WHEN 'APP' THEN 'APP'
                WHEN 'API' THEN 'API'
                ELSE 'GERADOR'
            END
            """,
            "'GERADOR'",
        )

        if "quantidade_sacas_prevista" in colunas_antigas:
            quantidade_sacas_prevista = """
                CASE
                    WHEN COALESCE(
                        s.quantidade_sacas_prevista,
                        0
                    ) > 0
                    THEN s.quantidade_sacas_prevista
                    ELSE 1
                END
            """
        elif "quantidade" in colunas_antigas:
            quantidade_sacas_prevista = """
                CASE
                    WHEN COALESCE(s.quantidade, 0) > 0
                    THEN s.quantidade
                    ELSE 1
                END
            """
        else:
            quantidade_sacas_prevista = "1"

        quantidade_kg_previsto = coluna(
            "quantidade_kg_previsto",
            """
            CASE
                WHEN COALESCE(
                    s.quantidade_kg_previsto,
                    0
                ) >= 0
                THEN s.quantidade_kg_previsto
                ELSE 0
            END
            """,
            "0",
        )

        quantidade_sacas_coletada = coluna(
            "quantidade_sacas_coletada",
            """
            CASE
                WHEN COALESCE(
                    s.quantidade_sacas_coletada,
                    0
                ) >= 0
                THEN s.quantidade_sacas_coletada
                ELSE 0
            END
            """,
            "0",
        )

        quantidade_kg_coletado = coluna(
            "quantidade_kg_coletado",
            """
            CASE
                WHEN COALESCE(
                    s.quantidade_kg_coletado,
                    0
                ) >= 0
                THEN s.quantidade_kg_coletado
                ELSE 0
            END
            """,
            "0",
        )

        if "status" in colunas_antigas:
            status = """
                CASE UPPER(
                    COALESCE(s.status, 'SOLICITADA')
                )
                    WHEN 'PENDENTE' THEN 'SOLICITADA'
                    WHEN 'SOLICITADA' THEN 'SOLICITADA'
                    WHEN 'EM_ANALISE' THEN 'EM_ANALISE'
                    WHEN 'EM ANÁLISE' THEN 'EM_ANALISE'
                    WHEN 'AGENDADA' THEN 'AGENDADA'
                    WHEN 'ACEITA' THEN 'AGENDADA'
                    WHEN 'EM_DESLOCAMENTO'
                        THEN 'EM_DESLOCAMENTO'
                    WHEN 'EM COLETA' THEN 'EM_COLETA'
                    WHEN 'EM_COLETA' THEN 'EM_COLETA'
                    WHEN 'CONCLUIDA' THEN 'CONCLUIDA'
                    WHEN 'CONCLUÍDA' THEN 'CONCLUIDA'
                    WHEN 'CANCELADA' THEN 'CANCELADA'
                    WHEN 'RECUSADA' THEN 'RECUSADA'
                    ELSE 'SOLICITADA'
                END
            """
        else:
            status = "'SOLICITADA'"

        prioridade = coluna(
            "prioridade",
            """
            CASE UPPER(COALESCE(s.prioridade, 'NORMAL'))
                WHEN 'URGENTE' THEN 'URGENTE'
                WHEN 'PROGRAMADA' THEN 'PROGRAMADA'
                ELSE 'NORMAL'
            END
            """,
            "'NORMAL'",
        )

        if {
            "data_solicitacao",
            "criado_em",
        }.issubset(colunas_antigas):
            data_solicitacao = """
                COALESCE(
                    s.data_solicitacao,
                    s.criado_em,
                    CURRENT_TIMESTAMP
                )
            """
        elif "data_solicitacao" in colunas_antigas:
            data_solicitacao = """
                COALESCE(
                    s.data_solicitacao,
                    CURRENT_TIMESTAMP
                )
            """
        elif "criado_em" in colunas_antigas:
            data_solicitacao = """
                COALESCE(
                    s.criado_em,
                    CURRENT_TIMESTAMP
                )
            """
        else:
            data_solicitacao = "CURRENT_TIMESTAMP"

        data_hora_agendada = coluna(
            "data_hora_agendada",
            "s.data_hora_agendada",
            "NULL",
        )

        data_hora_inicio = coluna(
            "data_hora_inicio",
            "s.data_hora_inicio",
            "NULL",
        )

        data_hora_chegada = coluna(
            "data_hora_chegada",
            "s.data_hora_chegada",
            "NULL",
        )

        data_hora_conclusao = coluna(
            "data_hora_conclusao",
            "s.data_hora_conclusao",
            "NULL",
        )

        if "observacao_cliente" in colunas_antigas:
            observacao_cliente = """
                COALESCE(s.observacao_cliente, '')
            """
        elif "observacao" in colunas_antigas:
            observacao_cliente = """
                COALESCE(s.observacao, '')
            """
        else:
            observacao_cliente = "''"

        observacao_operacional = coluna(
            "observacao_operacional",
            "COALESCE(s.observacao_operacional, '')",
            "''",
        )

        latitude = coluna(
            "latitude",
            "s.latitude",
            "NULL",
        )

        longitude = coluna(
            "longitude",
            "s.longitude",
            "NULL",
        )

        ativo = coluna(
            "ativo",
            """
            CASE
                WHEN s.ativo = 0 THEN 0
                ELSE 1
            END
            """,
            "1",
        )

        criado_em = coluna(
            "criado_em",
            """
            COALESCE(
                s.criado_em,
                CURRENT_TIMESTAMP
            )
            """,
            "CURRENT_TIMESTAMP",
        )

        atualizado_em = coluna(
            "atualizado_em",
            """
            COALESCE(
                s.atualizado_em,
                CURRENT_TIMESTAMP
            )
            """,
            "CURRENT_TIMESTAMP",
        )

        conexao.execute(
            f"""
            INSERT INTO solicitacoes_nova (
                id,
                codigo,
                organizacao_id,
                empresa_parceira_id,
                usuario_criacao_id,
                estabelecimento_id,
                motorista_id,
                veiculo_id,
                tipo_residuo,
                unidade_medida,
                origem,
                quantidade_sacas_prevista,
                quantidade_kg_previsto,
                quantidade_sacas_coletada,
                quantidade_kg_coletado,
                status,
                prioridade,
                data_solicitacao,
                data_hora_agendada,
                data_hora_inicio,
                data_hora_chegada,
                data_hora_conclusao,
                observacao_cliente,
                observacao_operacional,
                latitude,
                longitude,
                ativo,
                criado_em,
                atualizado_em
            )
            SELECT
                s.id,
                {codigo},
                {organizacao_id},
                {empresa_parceira_id},
                {usuario_criacao_id},
                {estabelecimento_id},
                {motorista_id},
                {veiculo_id},
                {tipo_residuo},
                {unidade_medida},
                {origem},
                {quantidade_sacas_prevista},
                {quantidade_kg_previsto},
                {quantidade_sacas_coletada},
                {quantidade_kg_coletado},
                {status},
                {prioridade},
                {data_solicitacao},
                {data_hora_agendada},
                {data_hora_inicio},
                {data_hora_chegada},
                {data_hora_conclusao},
                {observacao_cliente},
                {observacao_operacional},
                {latitude},
                {longitude},
                {ativo},
                {criado_em},
                {atualizado_em}
            FROM solicitacoes AS s
            WHERE
                (
                    {organizacao_id} IS NOT NULL
                    OR {estabelecimento_id} IS NOT NULL
                )
            """
        )

        conexao.execute(
            "DROP TABLE solicitacoes"
        )

        conexao.execute(
            """
            ALTER TABLE solicitacoes_nova
            RENAME TO solicitacoes
            """
        )

    @staticmethod
    def _preencher_codigos_solicitacoes(
        conexao: sqlite3.Connection,
    ) -> None:
        conexao.execute(
            """
            UPDATE solicitacoes
            SET codigo = printf('COL-%06d', id)
            WHERE codigo IS NULL
               OR TRIM(codigo) = ''
            """
        )

    @staticmethod
    def _criar_indices_solicitacoes(
        conexao: sqlite3.Connection,
    ) -> None:
        """Cria os índices de consulta das solicitações."""

        indices = (
            (
                "idx_solicitacoes_codigo",
                "codigo",
                True,
            ),
            (
                "idx_solicitacoes_organizacao",
                "organizacao_id",
                False,
            ),
            (
                "idx_solicitacoes_empresa_parceira",
                "empresa_parceira_id",
                False,
            ),
            (
                "idx_solicitacoes_usuario_criacao",
                "usuario_criacao_id",
                False,
            ),
            (
                "idx_solicitacoes_estabelecimento",
                "estabelecimento_id",
                False,
            ),
            (
                "idx_solicitacoes_motorista",
                "motorista_id",
                False,
            ),
            (
                "idx_solicitacoes_veiculo",
                "veiculo_id",
                False,
            ),
            (
                "idx_solicitacoes_tipo_residuo",
                "tipo_residuo",
                False,
            ),
            (
                "idx_solicitacoes_status",
                "status",
                False,
            ),
            (
                "idx_solicitacoes_prioridade",
                "prioridade",
                False,
            ),
            (
                "idx_solicitacoes_data_solicitacao",
                "data_solicitacao",
                False,
            ),
            (
                "idx_solicitacoes_data_hora_agendada",
                "data_hora_agendada",
                False,
            ),
            (
                "idx_solicitacoes_data_hora_inicio",
                "data_hora_inicio",
                False,
            ),
            (
                "idx_solicitacoes_data_hora_conclusao",
                "data_hora_conclusao",
                False,
            ),
            (
                "idx_solicitacoes_ativo",
                "ativo",
                False,
            ),
        )

        for nome, coluna, unico in indices:
            comando_unico = "UNIQUE " if unico else ""

            conexao.execute(
                f"""
                CREATE {comando_unico}INDEX IF NOT EXISTS
                    {nome}
                ON solicitacoes({coluna})
                """
            )
