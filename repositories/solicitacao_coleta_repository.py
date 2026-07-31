from models import SolicitacaoColeta
from repositories.sqlite_database import SQLiteDatabase


class SolicitacaoColetaRepository:
    """Responsável pelo acesso à tabela solicitacoes."""

    def __init__(self):
        self.database = SQLiteDatabase()

    def listar(self) -> list[SolicitacaoColeta]:
        """Lista todas as solicitações ativas."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                SELECT *
                FROM solicitacoes
                WHERE ativo = 1
                ORDER BY id DESC
                """
            )

            return [
                SolicitacaoColeta.from_row(row)
                for row in cursor.fetchall()
            ]

    def cadastrar(
        self,
        solicitacao: SolicitacaoColeta,
    ) -> SolicitacaoColeta:
        """Cadastra uma nova solicitação de coleta."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                INSERT INTO solicitacoes (
                    codigo,
                    estabelecimento_id,
                    motorista_id,
                    veiculo_id,
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
                    ativo
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?
                )
                """,
                (
                    solicitacao.codigo or None,
                    solicitacao.estabelecimento_id,
                    solicitacao.motorista_id,
                    solicitacao.veiculo_id,
                    solicitacao.quantidade_sacas_prevista,
                    solicitacao.quantidade_kg_previsto,
                    solicitacao.quantidade_sacas_coletada,
                    solicitacao.quantidade_kg_coletado,
                    solicitacao.status,
                    solicitacao.prioridade,
                    solicitacao.data_solicitacao,
                    solicitacao.data_hora_agendada,
                    solicitacao.data_hora_inicio,
                    solicitacao.data_hora_chegada,
                    solicitacao.data_hora_conclusao,
                    solicitacao.observacao_cliente,
                    solicitacao.observacao_operacional,
                    solicitacao.latitude,
                    solicitacao.longitude,
                    int(solicitacao.ativo),
                ),
            )

            solicitacao.id = cursor.lastrowid

            if not solicitacao.codigo:
                solicitacao.codigo = solicitacao.numero

                conexao.execute(
                    """
                    UPDATE solicitacoes
                    SET codigo = ?
                    WHERE id = ?
                    """,
                    (
                        solicitacao.codigo,
                        solicitacao.id,
                    ),
                )

        cadastrada = self.buscar_por_id(solicitacao.id)

        if cadastrada is None:
            raise RuntimeError(
                "A solicitação foi cadastrada, "
                "mas não pôde ser recuperada."
            )

        return cadastrada

    def buscar_por_id(
        self,
        solicitacao_id: int,
    ) -> SolicitacaoColeta | None:
        """Busca uma solicitação pelo seu identificador."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                SELECT *
                FROM solicitacoes
                WHERE id = ?
                """,
                (solicitacao_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return SolicitacaoColeta.from_row(row)

    def atualizar(
        self,
        solicitacao: SolicitacaoColeta,
    ) -> SolicitacaoColeta | None:
        """Atualiza todos os dados de uma solicitação existente."""

        if solicitacao.id is None:
            raise ValueError(
                "A solicitação precisa possuir um ID "
                "para ser atualizada."
            )

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    estabelecimento_id = ?,
                    motorista_id = ?,
                    veiculo_id = ?,
                    quantidade_sacas_prevista = ?,
                    quantidade_kg_previsto = ?,
                    quantidade_sacas_coletada = ?,
                    quantidade_kg_coletado = ?,
                    status = ?,
                    prioridade = ?,
                    data_solicitacao = ?,
                    data_hora_agendada = ?,
                    data_hora_inicio = ?,
                    data_hora_chegada = ?,
                    data_hora_conclusao = ?,
                    observacao_cliente = ?,
                    observacao_operacional = ?,
                    latitude = ?,
                    longitude = ?,
                    ativo = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    solicitacao.estabelecimento_id,
                    solicitacao.motorista_id,
                    solicitacao.veiculo_id,
                    solicitacao.quantidade_sacas_prevista,
                    solicitacao.quantidade_kg_previsto,
                    solicitacao.quantidade_sacas_coletada,
                    solicitacao.quantidade_kg_coletado,
                    solicitacao.status,
                    solicitacao.prioridade,
                    solicitacao.data_solicitacao,
                    solicitacao.data_hora_agendada,
                    solicitacao.data_hora_inicio,
                    solicitacao.data_hora_chegada,
                    solicitacao.data_hora_conclusao,
                    solicitacao.observacao_cliente,
                    solicitacao.observacao_operacional,
                    solicitacao.latitude,
                    solicitacao.longitude,
                    int(solicitacao.ativo),
                    solicitacao.id,
                ),
            )

            if cursor.rowcount == 0:
                return None

        return self.buscar_por_id(solicitacao.id)

    def alterar_status(
        self,
        solicitacao: SolicitacaoColeta,
    ) -> SolicitacaoColeta | None:
        """Atualiza o status e as datas operacionais da solicitação."""

        if solicitacao.id is None:
            raise ValueError(
                "A solicitação precisa possuir um ID."
            )

        with self.database.obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    status = ?,
                    data_hora_agendada = ?,
                    data_hora_inicio = ?,
                    data_hora_chegada = ?,
                    data_hora_conclusao = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    solicitacao.status,
                    solicitacao.data_hora_agendada,
                    solicitacao.data_hora_inicio,
                    solicitacao.data_hora_chegada,
                    solicitacao.data_hora_conclusao,
                    solicitacao.id,
                ),
            )

        return self.buscar_por_id(solicitacao.id)

    def excluir(
        self,
        solicitacao_id: int,
    ) -> bool:
        """
        Exclusão lógica da solicitação.
        """

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                   SET ativo = 0,
                       atualizado_em = CURRENT_TIMESTAMP
                 WHERE id = ?
                """,
                (solicitacao_id,),
            )

            return cursor.rowcount > 0

    def obter_estatisticas(self) -> dict:
        """Retorna indicadores para o Dashboard."""

        with self.database.obter_conexao() as conexao:

            row = conexao.execute(
                """
                SELECT

                    COUNT(*) AS total,

                    SUM(
                        CASE
                            WHEN status='PENDENTE'
                            THEN 1
                            ELSE 0
                        END
                    ) AS pendentes,

                    SUM(
                        CASE
                            WHEN status='AGENDADA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS agendadas,

                    SUM(
                        CASE
                            WHEN status='EM_COLETA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS em_coleta,

                    SUM(
                        CASE
                            WHEN status='CONCLUIDA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS concluidas,

                    COALESCE(
                        SUM(quantidade_sacas_prevista),
                        0
                    ) AS sacas_previstas,

                    COALESCE(
                        SUM(quantidade_sacas_coletada),
                        0
                    ) AS sacas_coletadas,

                    COALESCE(
                        SUM(quantidade_kg_previsto),
                        0
                    ) AS kg_previstos,

                    COALESCE(
                        SUM(quantidade_kg_coletado),
                        0
                    ) AS kg_coletados

                FROM solicitacoes

                WHERE ativo = 1
                """
            ).fetchone()

            return dict(row)

    def listar_ultimas(
        self,
        limite: int = 5,
    ) -> list[dict]:
        """Retorna as últimas solicitações."""

        with self.database.obter_conexao() as conexao:

            cursor = conexao.execute(
                """
                SELECT

                    s.codigo,

                    e.nome AS estabelecimento,

                    s.status,

                    s.quantidade_sacas_prevista,

                    s.quantidade_kg_previsto,

                    strftime(
                        '%d/%m/%Y %H:%M',
                        s.data_solicitacao
                    ) AS data_solicitacao

                FROM solicitacoes s

                INNER JOIN estabelecimentos e
                    ON e.id = s.estabelecimento_id

                WHERE s.ativo = 1

                ORDER BY s.id DESC

                LIMIT ?
                """,
                (limite,),
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

    def contar_agendadas_hoje(self) -> int:
        """Quantidade de coletas agendadas para hoje."""

        with self.database.obter_conexao() as conexao:

            row = conexao.execute(
                """
                SELECT COUNT(*)

                FROM solicitacoes

                WHERE ativo = 1

                  AND status = 'AGENDADA'

                  AND DATE(data_hora_agendada)
                      = DATE('now','localtime')
                """
            ).fetchone()

        return int(row[0] or 0)

    def listar_com_estabelecimento(self) -> list[dict]:
        """
        Lista solicitações juntamente com o estabelecimento.
        """

        with self.database.obter_conexao() as conexao:

            cursor = conexao.execute(
                """
                SELECT

                    s.id,
                    s.codigo,

                    s.estabelecimento_id,

                    e.nome AS estabelecimento,

                    s.motorista_id,

                    s.veiculo_id,

                    s.quantidade_sacas_prevista,
                    s.quantidade_kg_previsto,

                    s.quantidade_sacas_coletada,
                    s.quantidade_kg_coletado,

                    s.data_solicitacao,
                    s.data_hora_agendada,
                    s.data_hora_inicio,
                    s.data_hora_chegada,
                    s.data_hora_conclusao,

                    s.status,
                    s.prioridade,

                    s.ativo

                FROM solicitacoes s

                INNER JOIN estabelecimentos e
                    ON e.id = s.estabelecimento_id

                WHERE s.ativo = 1

                ORDER BY s.id DESC
                """
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]