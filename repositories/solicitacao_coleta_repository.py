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