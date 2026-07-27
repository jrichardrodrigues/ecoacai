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
            self._criar_tabela_usuarios(conexao)
            self._criar_tabela_codigos_verificacao(conexao)
            self._criar_tabela_estabelecimentos(conexao)

            self._garantir_tabela_motoristas(conexao)
            self._garantir_tabela_veiculos(conexao)

            self._garantir_tabela_solicitacoes(conexao)

    @staticmethod
    def _criar_tabela_usuarios(
            conexao: sqlite3.Connection,
    ) -> None:
        """Cria a tabela de usuários."""

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
        """
        Cria a tabela de solicitações ou migra a estrutura antiga.

        A versão antiga usava usuario_id, tipo e quantidade.
        A nova versão relaciona a solicitação a um estabelecimento.
        """

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
            "estabelecimento_id",
            "quantidade_sacas",
            "quantidade_kg",
            "data_solicitacao",
            "data_agendada",
            "data_conclusao",
            "status",
            "prioridade",
            "observacao",
            "motorista",
            "veiculo",
            "latitude",
            "longitude",
            "criado_em",
            "atualizado_em",
        }

        # Apenas adicionar colunas não corrige as restrições antigas,
        # como usuario_id e tipo obrigatórios. Por isso, uma tabela
        # legada precisa ser reconstruída.
        possui_estrutura_antiga = (
            "usuario_id" in colunas
            or "tipo" in colunas
            or "quantidade" in colunas
        )

        if possui_estrutura_antiga:
            cls._migrar_tabela_solicitacoes(
                conexao,
                colunas,
            )
        elif not colunas_atuais.issubset(colunas):
            cls._adicionar_colunas_solicitacoes(
                conexao,
                colunas,
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
    def _criar_tabela_solicitacoes(
        conexao: sqlite3.Connection,
        nome_tabela: str = "solicitacoes",
    ) -> None:
        # O nome é interno e controlado pelo código.
        conexao.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                codigo TEXT UNIQUE,

                estabelecimento_id INTEGER NOT NULL,

                quantidade_sacas INTEGER NOT NULL DEFAULT 1
                    CHECK (quantidade_sacas > 0),

                quantidade_kg REAL NOT NULL DEFAULT 0
                    CHECK (quantidade_kg >= 0),

                data_solicitacao TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                data_agendada TEXT,

                data_conclusao TEXT,

                status TEXT NOT NULL DEFAULT 'PENDENTE'
                    CHECK (
                        status IN (
                            'PENDENTE',
                            'AGENDADA',
                            'EM_COLETA',
                            'CONCLUIDA'
                        )
                    ),

                prioridade TEXT NOT NULL DEFAULT 'NORMAL'
                    CHECK (
                        prioridade IN (
                            'NORMAL',
                            'URGENTE',
                            'PROGRAMADA'
                        )
                    ),

                observacao TEXT NOT NULL DEFAULT '',

                motorista_id,
                
                veiculo_id,
                
                latitude REAL,

                longitude REAL,

                criado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                atualizado_em TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (estabelecimento_id)
                    REFERENCES estabelecimentos(id)
                    ON DELETE RESTRICT
            )
            """
        )

    @classmethod
    def _migrar_tabela_solicitacoes(
        cls,
        conexao: sqlite3.Connection,
        colunas_antigas: set[str],
    ) -> None:
        """
        Reconstrói a tabela antiga.

        Registros sem estabelecimento_id válido não são copiados,
        pois a nova estrutura exige vínculo com estabelecimento.
        """

        conexao.execute(
            "DROP TABLE IF EXISTS solicitacoes_nova"
        )

        cls._criar_tabela_solicitacoes(
            conexao,
            nome_tabela="solicitacoes_nova",
        )

        if "estabelecimento_id" in colunas_antigas:
            quantidade_sacas = (
                "COALESCE(quantidade_sacas, 1)"
                if "quantidade_sacas" in colunas_antigas
                else (
                    "COALESCE(quantidade, 1)"
                    if "quantidade" in colunas_antigas
                    else "1"
                )
            )

            quantidade_kg = (
                "COALESCE(quantidade_kg, 0)"
                if "quantidade_kg" in colunas_antigas
                else "0"
            )

            data_solicitacao = (
                "COALESCE(data_solicitacao, criado_em, "
                "CURRENT_TIMESTAMP)"
                if "data_solicitacao" in colunas_antigas
                else (
                    "COALESCE(criado_em, CURRENT_TIMESTAMP)"
                    if "criado_em" in colunas_antigas
                    else "CURRENT_TIMESTAMP"
                )
            )

            data_agendada = (
                "data_agendada"
                if "data_agendada" in colunas_antigas
                else "NULL"
            )

            data_conclusao = (
                "data_conclusao"
                if "data_conclusao" in colunas_antigas
                else "NULL"
            )

            prioridade = (
                "COALESCE(prioridade, 'NORMAL')"
                if "prioridade" in colunas_antigas
                else "'NORMAL'"
            )

            observacao = (
                "COALESCE(observacao, '')"
                if "observacao" in colunas_antigas
                else "''"
            )

            motorista = (
                "motorista"
                if "motorista" in colunas_antigas
                else "NULL"
            )

            veiculo = (
                "veiculo"
                if "veiculo" in colunas_antigas
                else "NULL"
            )

            latitude = (
                "latitude"
                if "latitude" in colunas_antigas
                else "NULL"
            )

            longitude = (
                "longitude"
                if "longitude" in colunas_antigas
                else "NULL"
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

            codigo = (
                "codigo"
                if "codigo" in colunas_antigas
                else "NULL"
            )

            status = """
                CASE status
                    WHEN 'ACEITA' THEN 'AGENDADA'
                    WHEN 'EM_COLETA' THEN 'EM_COLETA'
                    WHEN 'CONCLUIDA' THEN 'CONCLUIDA'
                    WHEN 'PENDENTE' THEN 'PENDENTE'
                    ELSE 'PENDENTE'
                END
            """

            conexao.execute(
                f"""
                INSERT INTO solicitacoes_nova (
                    id,
                    codigo,
                    estabelecimento_id,
                    quantidade_sacas,
                    quantidade_kg,
                    data_solicitacao,
                    data_agendada,
                    data_conclusao,
                    status,
                    prioridade,
                    observacao,
                    motorista,
                    veiculo,
                    latitude,
                    longitude,
                    criado_em,
                    atualizado_em
                )
                SELECT
                    s.id,
                    {codigo},
                    s.estabelecimento_id,
                    {quantidade_sacas},
                    {quantidade_kg},
                    {data_solicitacao},
                    {data_agendada},
                    {data_conclusao},
                    {status},
                    {prioridade},
                    {observacao},
                    {motorista},
                    {veiculo},
                    {latitude},
                    {longitude},
                    {criado_em},
                    {atualizado_em}
                FROM solicitacoes AS s
                WHERE s.estabelecimento_id IS NOT NULL
                  AND EXISTS (
                      SELECT 1
                      FROM estabelecimentos AS e
                      WHERE e.id = s.estabelecimento_id
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
    def _adicionar_colunas_solicitacoes(
        conexao: sqlite3.Connection,
        colunas_existentes: set[str],
    ) -> None:
        novas_colunas = {
            "codigo": "TEXT",
            "estabelecimento_id": "INTEGER",
            "quantidade_sacas": (
                "INTEGER NOT NULL DEFAULT 1"
            ),
            "quantidade_kg": (
                "REAL NOT NULL DEFAULT 0"
            ),
            "data_solicitacao": "TEXT",
            "data_agendada": "TEXT",
            "data_conclusao": "TEXT",
            "prioridade": (
                "TEXT NOT NULL DEFAULT 'NORMAL'"
            ),
            "observacao": (
                "TEXT NOT NULL DEFAULT ''"
            ),
            "motorista": "TEXT",
            "veiculo": "TEXT",
            "latitude": "REAL",
            "longitude": "REAL",
            "criado_em": "TEXT",
            "atualizado_em": "TEXT",
        }

        for nome, definicao in novas_colunas.items():
            if nome in colunas_existentes:
                continue

            conexao.execute(
                f"""
                ALTER TABLE solicitacoes
                ADD COLUMN {nome} {definicao}
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
        conexao.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_solicitacoes_codigo
            ON solicitacoes(codigo)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_solicitacoes_status
            ON solicitacoes(status)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_solicitacoes_prioridade
            ON solicitacoes(prioridade)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_solicitacoes_estabelecimento
            ON solicitacoes(estabelecimento_id)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_solicitacoes_data_agendada
            ON solicitacoes(data_agendada)
            """
        )

        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_solicitacoes_data_solicitacao
            ON solicitacoes(data_solicitacao)
            """
        )

