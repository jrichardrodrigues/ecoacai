from __future__ import annotations

from datetime import date
from typing import Any

from models import SolicitacaoColeta
from repositories.sqlite_database import SQLiteDatabase


class SolicitacaoColetaRepository:
    """Responsável pela persistência das solicitações de coleta."""

    def __init__(
        self,
        database: SQLiteDatabase | None = None,
    ) -> None:
        self.database = database or SQLiteDatabase()

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def listar(
        self,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        """Lista as solicitações por ordem decrescente de criação."""

        consulta = """
            SELECT *
            FROM solicitacoes
        """

        if somente_ativas:
            consulta += """
                WHERE ativo = 1
            """

        consulta += """
            ORDER BY id DESC
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(consulta).fetchall()

        return self._converter_rows(rows)

    def buscar_por_id(
        self,
        solicitacao_id: int | None,
    ) -> SolicitacaoColeta | None:
        """Busca uma solicitação pelo identificador."""

        if solicitacao_id is None or solicitacao_id <= 0:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM solicitacoes
                WHERE id = ?
                LIMIT 1
                """,
                (solicitacao_id,),
            ).fetchone()

        return self._converter_row(row)

    def buscar_por_codigo(
        self,
        codigo: str,
    ) -> SolicitacaoColeta | None:
        """Busca uma solicitação pelo código amigável."""

        codigo_normalizado = str(codigo or "").strip().upper()

        if not codigo_normalizado:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM solicitacoes
                WHERE codigo = ?
                LIMIT 1
                """,
                (codigo_normalizado,),
            ).fetchone()

        return self._converter_row(row)

    def listar_por_organizacao(
        self,
        organizacao_id: int,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        """Lista as solicitações pertencentes a uma organização."""

        consulta = """
            SELECT *
            FROM solicitacoes
            WHERE organizacao_id = ?
        """

        parametros: list[Any] = [organizacao_id]

        if somente_ativas:
            consulta += """
                AND ativo = 1
            """

        consulta += """
            ORDER BY id DESC
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return self._converter_rows(rows)

    def listar_por_status(
        self,
        status: str,
        *,
        organizacao_id: int | None = None,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        """Lista solicitações pelo status operacional."""

        status_normalizado = str(status or "").strip().upper()

        if not status_normalizado:
            return []

        consulta = """
            SELECT *
            FROM solicitacoes
            WHERE status = ?
        """

        parametros: list[Any] = [status_normalizado]

        if organizacao_id is not None:
            consulta += """
                AND organizacao_id = ?
            """
            parametros.append(organizacao_id)

        if somente_ativas:
            consulta += """
                AND ativo = 1
            """

        consulta += """
            ORDER BY id DESC
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return self._converter_rows(rows)

    def listar_por_periodo(
        self,
        data_inicial: str | date,
        data_final: str | date,
        *,
        organizacao_id: int | None = None,
        somente_ativas: bool = True,
    ) -> list[SolicitacaoColeta]:
        """Lista solicitações criadas dentro de um período."""

        inicio = self._normalizar_data(data_inicial)
        fim = self._normalizar_data(data_final)

        if inicio > fim:
            raise ValueError(
                "A data inicial não pode ser posterior à data final."
            )

        consulta = """
            SELECT *
            FROM solicitacoes
            WHERE DATE(data_solicitacao)
                  BETWEEN DATE(?) AND DATE(?)
        """

        parametros: list[Any] = [inicio, fim]

        if organizacao_id is not None:
            consulta += """
                AND organizacao_id = ?
            """
            parametros.append(organizacao_id)

        if somente_ativas:
            consulta += """
                AND ativo = 1
            """

        consulta += """
            ORDER BY data_solicitacao DESC, id DESC
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return self._converter_rows(rows)

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        solicitacao: SolicitacaoColeta,
    ) -> SolicitacaoColeta:
        """Cadastra uma nova solicitação de coleta."""

        self._validar_vinculo_principal(solicitacao)

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                INSERT INTO solicitacoes (
                    codigo,
                    organizacao_id,
                    empresa_parceira_id,
                    usuario_criacao_id,
                    estabelecimento_id,
                    motorista_id,
                    veiculo_id,
                    tipo_residuo,
                    forma_acondicionamento,
                    unidade_medida,
                    origem,
                    quantidade_prevista,
                    peso_estimado_kg,
                    tipo_operacao,
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
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    solicitacao.codigo or None,
                    solicitacao.organizacao_id,
                    solicitacao.empresa_parceira_id,
                    solicitacao.usuario_criacao_id,
                    solicitacao.estabelecimento_id,
                    solicitacao.motorista_id,
                    solicitacao.veiculo_id,
                    solicitacao.tipo_residuo,
                    solicitacao.forma_acondicionamento,
                    solicitacao.unidade_medida,
                    solicitacao.origem,
                    solicitacao.quantidade_prevista,
                    solicitacao.peso_estimado_kg,
                    solicitacao.tipo_operacao,
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

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def atualizar(
        self,
        solicitacao: SolicitacaoColeta,
    ) -> SolicitacaoColeta | None:
        """Atualiza os dados completos de uma solicitação."""

        if solicitacao.id is None:
            raise ValueError(
                "A solicitação precisa possuir um ID "
                "para ser atualizada."
            )

        self._validar_vinculo_principal(solicitacao)

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    organizacao_id = ?,
                    empresa_parceira_id = ?,
                    usuario_criacao_id = ?,
                    estabelecimento_id = ?,
                    motorista_id = ?,
                    veiculo_id = ?,
                    tipo_residuo = ?,
                    forma_acondicionamento = ?,
                    unidade_medida = ?,
                    origem = ?,
                    quantidade_prevista = ?,
                    peso_estimado_kg = ?,
                    tipo_operacao = ?,
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
                    solicitacao.organizacao_id,
                    solicitacao.empresa_parceira_id,
                    solicitacao.usuario_criacao_id,
                    solicitacao.estabelecimento_id,
                    solicitacao.motorista_id,
                    solicitacao.veiculo_id,
                    solicitacao.tipo_residuo,
                    solicitacao.unidade_medida,
                    solicitacao.origem,
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
        """Atualiza o status e as datas operacionais."""

        if solicitacao.id is None:
            raise ValueError(
                "A solicitação precisa possuir um ID."
            )

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
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

            if cursor.rowcount == 0:
                return None

        return self.buscar_por_id(solicitacao.id)

    def vincular_empresa_parceira(
        self,
        solicitacao_id: int,
        empresa_parceira_id: int | None,
    ) -> SolicitacaoColeta | None:
        """Vincula ou remove a empresa parceira responsável."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    empresa_parceira_id = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    empresa_parceira_id,
                    solicitacao_id,
                ),
            )

            if cursor.rowcount == 0:
                return None

        return self.buscar_por_id(solicitacao_id)

    def excluir(
        self,
        solicitacao_id: int,
    ) -> bool:
        """Realiza a exclusão lógica da solicitação."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    ativo = 0,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (solicitacao_id,),
            )

        return cursor.rowcount > 0

    # ==========================================================
    # DASHBOARD E CONSULTAS OPERACIONAIS
    # ==========================================================

    def obter_estatisticas(
        self,
        organizacao_id: int | None = None,
    ) -> dict:
        """Retorna indicadores das solicitações ativas."""

        filtro_organizacao = ""
        parametros: list[Any] = []

        if organizacao_id is not None:
            filtro_organizacao = """
                AND organizacao_id = ?
            """
            parametros.append(organizacao_id)

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                f"""
                SELECT
                    COUNT(*) AS total,

                    SUM(
                        CASE
                            WHEN status IN (
                                'SOLICITADA',
                                'EM_ANALISE'
                            )
                            THEN 1
                            ELSE 0
                        END
                    ) AS pendentes,

                    SUM(
                        CASE
                            WHEN status = 'SOLICITADA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS solicitadas,

                    SUM(
                        CASE
                            WHEN status = 'EM_ANALISE'
                            THEN 1
                            ELSE 0
                        END
                    ) AS em_analise,

                    SUM(
                        CASE
                            WHEN status = 'AGENDADA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS agendadas,

                    SUM(
                        CASE
                            WHEN status IN (
                                'EM_DESLOCAMENTO',
                                'EM_COLETA'
                            )
                            THEN 1
                            ELSE 0
                        END
                    ) AS em_coleta,

                    SUM(
                        CASE
                            WHEN status = 'CONCLUIDA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS concluidas,

                    SUM(
                        CASE
                            WHEN status = 'CANCELADA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS canceladas,

                    SUM(
                        CASE
                            WHEN status = 'RECUSADA'
                            THEN 1
                            ELSE 0
                        END
                    ) AS recusadas,

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
                {filtro_organizacao}
                """,
                tuple(parametros),
            ).fetchone()

        return dict(row)

    def listar_ultimas(
        self,
        limite: int = 5,
        *,
        organizacao_id: int | None = None,
    ) -> list[dict]:
        """Retorna as últimas solicitações com o solicitante."""

        consulta = """
            SELECT
                s.id,
                s.codigo,
                s.organizacao_id,
                s.estabelecimento_id,

                COALESCE(
                    o.nome,
                    e.nome,
                    'Solicitante não identificado'
                ) AS solicitante,

                s.tipo_residuo,
                s.unidade_medida,
                s.status,
                s.quantidade_sacas_prevista,
                s.quantidade_kg_previsto,

                strftime(
                    '%d/%m/%Y %H:%M',
                    s.data_solicitacao
                ) AS data_solicitacao

            FROM solicitacoes AS s

            LEFT JOIN organizacoes AS o
                ON o.id = s.organizacao_id

            LEFT JOIN estabelecimentos AS e
                ON e.id = s.estabelecimento_id

            WHERE s.ativo = 1
        """

        parametros: list[Any] = []

        if organizacao_id is not None:
            consulta += """
                AND s.organizacao_id = ?
            """
            parametros.append(organizacao_id)

        consulta += """
            ORDER BY s.id DESC
            LIMIT ?
        """
        parametros.append(max(1, int(limite)))

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return [dict(row) for row in rows]

    def contar_agendadas_hoje(
        self,
        organizacao_id: int | None = None,
    ) -> int:
        """Retorna a quantidade de coletas agendadas para hoje."""

        consulta = """
            SELECT COUNT(*)
            FROM solicitacoes
            WHERE ativo = 1
              AND status = 'AGENDADA'
              AND DATE(data_hora_agendada)
                  = DATE('now', 'localtime')
        """

        parametros: list[Any] = []

        if organizacao_id is not None:
            consulta += """
                AND organizacao_id = ?
            """
            parametros.append(organizacao_id)

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchone()

        return int(row[0] or 0)

    def listar_operacional(
        self,
        *,
        status: str | None = None,
        organizacao_id: int | None = None,
        empresa_parceira_id: int | None = None,
    ) -> list[dict]:
        """
        Lista solicitações com os principais vínculos operacionais.

        Este método atende ao Portal do Gestor e preserva os
        estabelecimentos legados durante a transição arquitetural.
        """

        consulta = """
            SELECT
                s.id,
                s.codigo,

                s.organizacao_id,
                s.empresa_parceira_id,
                s.usuario_criacao_id,
                s.estabelecimento_id,
                s.motorista_id,
                s.veiculo_id,

                COALESCE(
                    o.nome,
                    e.nome,
                    'Solicitante não identificado'
                ) AS solicitante,

                ep.nome AS empresa_parceira,
                m.nome AS motorista,

                CASE
                    WHEN v.id IS NULL THEN ''
                    ELSE TRIM(
                        COALESCE(v.marca, '') || ' ' ||
                        COALESCE(v.modelo, '') || ' • ' ||
                        COALESCE(v.placa, '')
                    )
                END AS veiculo,

                s.tipo_residuo,
                s.forma_acondicionamento,
                s.unidade_medida,
                s.origem,
                
                s.quantidade_prevista,
                s.peso_estimado_kg,
                s.tipo_operacao,
                
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

                s.observacao_cliente,
                s.observacao_operacional,

                s.ativo

            FROM solicitacoes AS s

            LEFT JOIN organizacoes AS o
                ON o.id = s.organizacao_id

            LEFT JOIN organizacoes AS ep
                ON ep.id = s.empresa_parceira_id

            LEFT JOIN estabelecimentos AS e
                ON e.id = s.estabelecimento_id

            LEFT JOIN motoristas AS m
                ON m.id = s.motorista_id

            LEFT JOIN veiculos AS v
                ON v.id = s.veiculo_id

            WHERE s.ativo = 1
        """

        parametros: list[Any] = []

        if status:
            consulta += """
                AND s.status = ?
            """
            parametros.append(
                str(status).strip().upper()
            )

        if organizacao_id is not None:
            consulta += """
                AND s.organizacao_id = ?
            """
            parametros.append(organizacao_id)

        if empresa_parceira_id is not None:
            consulta += """
                AND s.empresa_parceira_id = ?
            """
            parametros.append(empresa_parceira_id)

        consulta += """
            ORDER BY s.id DESC
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return [dict(row) for row in rows]

    def listar_com_estabelecimento(self) -> list[dict]:
        """
        Mantém compatibilidade com a interface antiga.

        Para novos fluxos, prefira listar_operacional().
        """

        return self.listar_operacional()

    # ==========================================================
    # MÉTODOS AUXILIARES
    # ==========================================================

    @staticmethod
    def _converter_row(
        row: Any,
    ) -> SolicitacaoColeta | None:
        if row is None:
            return None

        return SolicitacaoColeta.from_row(row)

    @classmethod
    def _converter_rows(
        cls,
        rows: list[Any],
    ) -> list[SolicitacaoColeta]:
        return [
            solicitacao
            for row in rows
            if (
                solicitacao := cls._converter_row(row)
            ) is not None
        ]

    @staticmethod
    def _normalizar_data(
        valor: str | date,
    ) -> str:
        if isinstance(valor, date):
            return valor.isoformat()

        texto = str(valor or "").strip()

        if not texto:
            raise ValueError(
                "Informe as datas inicial e final."
            )

        return texto

    @staticmethod
    def _validar_vinculo_principal(
        solicitacao: SolicitacaoColeta,
    ) -> None:
        if (
            solicitacao.organizacao_id is None
            and solicitacao.estabelecimento_id is None
        ):
            raise ValueError(
                "A solicitação deve estar vinculada a uma "
                "organização ou a um estabelecimento legado."
            )
