from repositories.sqlite_database import SQLiteDatabase
from models import SolicitacaoColeta


class SolicitacaoColetaRepository:
    """Repository responsável pelo acesso à tabela solicitacoes."""

    def __init__(self):
        self.database = SQLiteDatabase()

    def listar(self) -> list[SolicitacaoColeta]:
        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                SELECT *
                FROM solicitacoes
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
        """Cadastra uma solicitação de coleta."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                INSERT INTO solicitacoes (
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
                    latitude,
                    longitude
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    None,
                    solicitacao.estabelecimento_id,
                    solicitacao.quantidade_sacas,
                    solicitacao.quantidade_kg,
                    solicitacao.data_solicitacao,
                    solicitacao.data_agendada,
                    solicitacao.data_conclusao,
                    solicitacao.status,
                    solicitacao.prioridade,
                    solicitacao.observacao,
                    solicitacao.latitude,
                    solicitacao.longitude,
                ),
            )

            solicitacao.id = cursor.lastrowid
            codigo = solicitacao.numero

            conexao.execute(
                """
                UPDATE solicitacoes
                SET codigo = ?
                WHERE id = ?
                """,
                (
                    codigo,
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

    def atualizar(
            self,
            solicitacao: SolicitacaoColeta,
    ) -> SolicitacaoColeta | None:
        """Atualiza uma solicitação existente."""

        with self.database.obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    estabelecimento_id = ?,
                    quantidade_sacas = ?,
                    quantidade_kg = ?,
                    data_agendada = ?,
                    data_conclusao = ?,
                    status = ?,
                    prioridade = ?,
                    observacao = ?,
                    latitude = ?,
                    longitude = ?
                WHERE id = ?
                """,
                (
                    solicitacao.estabelecimento_id,
                    solicitacao.quantidade_sacas,
                    solicitacao.quantidade_kg,
                    solicitacao.data_agendada,
                    solicitacao.data_conclusao,
                    solicitacao.status,
                    solicitacao.prioridade,
                    solicitacao.observacao,
                    solicitacao.latitude,
                    solicitacao.longitude,
                    solicitacao.id,
                ),
            )

        return self.buscar_por_id(solicitacao.id)

    def alterar_status(
            self,
            solicitacao: SolicitacaoColeta,
    ) -> SolicitacaoColeta | None:
        """Atualiza apenas o status e as datas da solicitação."""

        with self.database.obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    status = ?,
                    data_agendada = ?,
                    data_conclusao = ?
                WHERE id = ?
                """,
                (
                    solicitacao.status,
                    solicitacao.data_agendada,
                    solicitacao.data_conclusao,
                    solicitacao.id,
                ),
            )

        return self.buscar_por_id(
            solicitacao.id
        )

    def excluir(
            self,
            solicitacao_id: int,
    ) -> bool:
        """Exclui uma solicitação."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                DELETE FROM solicitacoes
                WHERE id = ?
                """,
                (solicitacao_id,),
            )

            return cursor.rowcount > 0

    def obter_estatisticas(self) -> dict:
        """Retorna indicadores para o Dashboard."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
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
                        SUM(quantidade_sacas),
                        0
                    ) AS total_sacas,

                    COALESCE(
                        SUM(quantidade_kg),
                        0
                    ) AS total_kg

                FROM solicitacoes
                """
            )

            row = cursor.fetchone()

            return dict(row)

    def listar_ultimas(
            self,
            limite: int = 5,
    ) -> list[dict]:

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                SELECT
                    s.codigo,
                    e.nome AS estabelecimento,
                    s.status,
                    s.quantidade_sacas,
                    s.quantidade_kg

                FROM solicitacoes AS s

                INNER JOIN estabelecimentos AS e
                    ON e.id = s.estabelecimento_id

                ORDER BY s.id DESC

                LIMIT ?
                """,
                (limite,),
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

    def buscar_por_id(
        self,
        solicitacao_id: int,
    ) -> SolicitacaoColeta | None:

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