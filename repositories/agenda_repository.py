from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from repositories.sqlite_database import SQLiteDatabase
from config.constants import StatusColeta


class AgendaRepository:
    """Repositório responsável pelas operações da agenda de coletas."""

    _FUSO_HORARIO = ZoneInfo("America/Belem")

    _STATUS_VALIDOS = {
        StatusColeta.SOLICITADA,
        StatusColeta.EM_ANALISE,
        StatusColeta.AGENDADA,
        StatusColeta.EM_COLETA,
        StatusColeta.CONCLUIDA,
        StatusColeta.CANCELADA,
    }

    _CAMPOS_DATA_STATUS = {
        "data_hora_inicio",
        "data_hora_chegada",
        "data_hora_conclusao",
    }

    _TRANSICOES_STATUS = {
        StatusColeta.SOLICITADA: {
            StatusColeta.EM_ANALISE,
            StatusColeta.CANCELADA,
        },

        StatusColeta.EM_ANALISE: {
            StatusColeta.AGENDADA,
            StatusColeta.CANCELADA,
        },

        StatusColeta.AGENDADA: {
            StatusColeta.EM_COLETA,
            StatusColeta.CANCELADA,
        },

        StatusColeta.EM_COLETA: {
            StatusColeta.CONCLUIDA,
        },

        StatusColeta.CONCLUIDA: set(),

        StatusColeta.CANCELADA: set(),
    }

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
            status: str | None = None,
    ) -> list[dict]:
        """
        Lista as solicitações ativas da agenda.

        Quando um status é informado, retorna somente os registros
        correspondentes. Sem um status, retorna solicitações pendentes,
        agendadas e em coleta.
        """

        consulta = self._consulta_base()

        consulta += """
            WHERE s.ativo = 1
        """

        parametros: list[object] = []

        if status:
            status_normalizado = self._normalizar_status(
                status
            )

            consulta += """
                AND s.status = ?
            """

            parametros.append(
                status_normalizado
            )

        else:
            consulta += """
                AND s.status IN (
                    'PENDENTE',
                    'AGENDADA',
                    'EM_COLETA'
                )
            """

        consulta += self._ordenacao_padrao()

        with self.database.obter_conexao() as conexao:
            registros = conexao.execute(
                consulta,
                parametros,
            ).fetchall()

        return [
            dict(registro)
            for registro in registros
        ]

    def obter_por_id(
        self,
        solicitacao_id: int,
    ) -> dict | None:
        """Retorna uma solicitação ativa pelo identificador."""

        if solicitacao_id <= 0:
            return None

        consulta = self._consulta_base()

        consulta += """
            WHERE s.id = ?
              AND s.ativo = 1
            LIMIT 1
        """

        with self.database.obter_conexao() as conexao:
            registro = conexao.execute(
                consulta,
                (solicitacao_id,),
            ).fetchone()

        if registro is None:
            return None

        return dict(registro)

    def pesquisar(
        self,
        *,
        data: str | None = None,
        status: str | None = None,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
        estabelecimento_id: int | None = None,
    ) -> list[dict]:
        """
        Pesquisa solicitações combinando filtros opcionais.

        Args:
            data:
                Data do agendamento no formato AAAA-MM-DD.

            status:
                Status da solicitação.

            motorista_id:
                Identificador do motorista.

            veiculo_id:
                Identificador do veículo.

            estabelecimento_id:
                Identificador do estabelecimento.

        Returns:
            Lista de solicitações encontradas.
        """

        consulta = self._consulta_base()

        consulta += """
            WHERE s.ativo = 1
        """

        parametros: list[object] = []

        if data and data.strip():
            consulta += """
                AND DATE(s.data_hora_agendada) = DATE(?)
            """

            parametros.append(
                data.strip()
            )

        if status and status.strip():
            status_normalizado = self._normalizar_status(status)

            consulta += """
                AND s.status = ?
            """

            parametros.append(
                status_normalizado
            )

        if motorista_id is not None:
            consulta += """
                AND s.motorista_id = ?
            """

            parametros.append(
                motorista_id
            )

        if veiculo_id is not None:
            consulta += """
                AND s.veiculo_id = ?
            """

            parametros.append(
                veiculo_id
            )

        if estabelecimento_id is not None:
            consulta += """
                AND s.estabelecimento_id = ?
            """

            parametros.append(
                estabelecimento_id
            )

        consulta += self._ordenacao_padrao()

        with self.database.obter_conexao() as conexao:
            registros = conexao.execute(
                consulta,
                parametros,
            ).fetchall()

        return [
            dict(registro)
            for registro in registros
        ]

    def agenda_hoje(
            self,
            *,
            status: str | None = None,
    ) -> list[dict]:
        """
        Retorna as solicitações agendadas para a data atual.

        Opcionalmente, filtra por status.
        """

        consulta = self._consulta_base()

        consulta += """
            WHERE s.ativo = 1
              AND DATE(s.data_hora_agendada) = DATE('now', 'localtime')
        """

        parametros: list[object] = []

        if status and status.strip():
            status_normalizado = self._normalizar_status(
                status
            )

            consulta += """
                AND s.status = ?
            """

            parametros.append(
                status_normalizado
            )

        consulta += self._ordenacao_padrao()

        with self.database.obter_conexao() as conexao:
            registros = conexao.execute(
                consulta,
                parametros,
            ).fetchall()

        return [
            dict(registro)
            for registro in registros
        ]

    def agenda_periodo(
            self,
            data_inicial: str,
            data_final: str,
            *,
            status: str | None = None,
            motorista_id: int | None = None,
            veiculo_id: int | None = None,
    ) -> list[dict]:
        """
        Retorna as solicitações agendadas em um intervalo de datas.

        As datas devem ser informadas no formato AAAA-MM-DD.
        """

        data_inicial_normalizada = data_inicial.strip()
        data_final_normalizada = data_final.strip()

        if (
                not data_inicial_normalizada
                or not data_final_normalizada
        ):
            return []

        if data_inicial_normalizada > data_final_normalizada:
            raise ValueError(
                "A data inicial não pode ser maior que a data final."
            )

        consulta = self._consulta_base()

        consulta += """
            WHERE s.ativo = 1
              AND DATE(
                    CASE
                        WHEN s.status = 'CONCLUIDA'
                            THEN COALESCE(
                                s.data_hora_conclusao,
                                s.data_hora_agendada,
                                s.data_solicitacao
                            )

                        WHEN s.status = 'EM_COLETA'
                            THEN COALESCE(
                                s.data_hora_inicio,
                                s.data_hora_agendada,
                                s.data_solicitacao
                            )

                        WHEN s.status = 'CANCELADA'
                            THEN COALESCE(
                                s.data_hora_cancelamento,
                                s.data_hora_agendada,
                                s.data_solicitacao
                            )

                        WHEN s.status = 'AGENDADA'
                            THEN COALESCE(
                                s.data_hora_agendada,
                                s.data_solicitacao
                            )

                        ELSE s.data_solicitacao
                    END
                  )
                  BETWEEN DATE(?) AND DATE(?)
        """

        parametros: list[object] = [
            data_inicial_normalizada,
            data_final_normalizada,
        ]

        if status and status.strip():
            status_normalizado = self._normalizar_status(
                status
            )

            consulta += """
                AND s.status = ?
            """

            parametros.append(
                status_normalizado
            )

        if motorista_id is not None:
            consulta += """
                AND s.motorista_id = ?
            """

            parametros.append(
                motorista_id
            )

        if veiculo_id is not None:
            consulta += """
                AND s.veiculo_id = ?
            """

            parametros.append(
                veiculo_id
            )

        consulta += self._ordenacao_padrao()

        with self.database.obter_conexao() as conexao:
            registros = conexao.execute(
                consulta,
                parametros,
            ).fetchall()

        return [
            dict(registro)
            for registro in registros
        ]

    # ==========================================================
    # OPERAÇÕES
    # ==========================================================

    def agendar(
        self,
        solicitacao_id: int,
        data_hora_agendada: str,
        motorista_id: int | None = None,
        veiculo_id: int | None = None,
    ) -> bool:
        """
        Agenda uma solicitação de coleta.

        Define a data e a hora do agendamento e, opcionalmente,
        associa um motorista e um veículo.
        """

        if solicitacao_id <= 0:
            return False

        data_hora_normalizada = data_hora_agendada.strip()

        if not data_hora_normalizada:
            return False

        with self.database.obter_conexao() as conexao:
            registro = conexao.execute(
                """
                SELECT status
                FROM solicitacoes
                WHERE id = ?
                  AND ativo = 1
                LIMIT 1
                """,
                (solicitacao_id,),
            ).fetchone()

            if registro is None:
                return False

            status_atual = str(
                registro["status"]
            ).strip().upper()

            if status_atual not in {
                StatusColeta.EM_ANALISE,
                StatusColeta.AGENDADA,
            }:
                return False

            if motorista_id is not None:
                motorista_existe = conexao.execute(
                    """
                    SELECT 1
                    FROM motoristas
                    WHERE id = ?
                      AND ativo = 1
                    LIMIT 1
                    """,
                    (motorista_id,),
                ).fetchone()

                if motorista_existe is None:
                    return False

            if veiculo_id is not None:
                veiculo_existe = conexao.execute(
                    """
                    SELECT 1
                    FROM veiculos
                    WHERE id = ?
                      AND ativo = 1
                    LIMIT 1
                    """,
                    (veiculo_id,),
                ).fetchone()

                if veiculo_existe is None:
                    return False

            agora_local = self._agora_local()

            consulta = """
                UPDATE solicitacoes
                   SET data_hora_agendada = ?,
                       status = 'AGENDADA',
                       atualizado_em = ?
            """

            parametros: list[object] = [
                data_hora_normalizada,
                agora_local,
            ]

            if motorista_id is not None:
                consulta += """
                    , motorista_id = ?
                """

                parametros.append(
                    motorista_id
                )

            if veiculo_id is not None:
                consulta += """
                    , veiculo_id = ?
                """

                parametros.append(
                    veiculo_id
                )

            consulta += """
                 WHERE id = ?
                   AND ativo = 1
            """

            parametros.append(
                solicitacao_id
            )

            cursor = conexao.execute(
                consulta,
                parametros,
            )

            return cursor.rowcount > 0

    def reagendar(
            self,
            solicitacao_id: int,
            nova_data_hora: str,
            motorista_id: int | None = None,
            veiculo_id: int | None = None,
    ) -> bool:
        """
        Reagenda uma solicitação que já está com status AGENDADA.

        Opcionalmente, atualiza o motorista e o veículo vinculados.
        """

        solicitacao = self.obter_por_id(
            solicitacao_id
        )

        if solicitacao is None:
            return False

        status_atual = str(
            solicitacao["status"]
        ).strip().upper()

        if status_atual != StatusColeta.AGENDADA:
            return False

        return self.agendar(
            solicitacao_id=solicitacao_id,
            data_hora_agendada=nova_data_hora,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
        )

    def iniciar_coleta(
            self,
            solicitacao_id: int,
    ) -> bool:
        """
        Inicia uma coleta agendada.

        Altera o status para EM_COLETA e registra
        a data e a hora de início.
        """

        return self._atualizar_status(
            solicitacao_id=solicitacao_id,
            novo_status=StatusColeta.EM_COLETA,
            campo_data="data_hora_inicio",
        )

    def registrar_chegada(
            self,
            solicitacao_id: int,
    ) -> bool:
        """
        Registra a chegada da equipe ao local da coleta.

        A coleta deve estar em andamento.
        O status permanece EM_COLETA.

        Se a chegada já estiver registrada, mantém o horário
        original e considera a operação válida.
        """

        if solicitacao_id <= 0:
            return False

        with self.database.obter_conexao() as conexao:
            registro = conexao.execute(
                """
                SELECT
                    status,
                    data_hora_chegada
                FROM solicitacoes
                WHERE id = ?
                  AND ativo = 1
                LIMIT 1
                """,
                (solicitacao_id,),
            ).fetchone()

            if registro is None:
                return False

            status_atual = str(
                registro["status"] or ""
            ).strip().upper()

            if status_atual != StatusColeta.EM_COLETA:
                return False

            chegada_atual = str(
                registro["data_hora_chegada"] or ""
            ).strip()

            if chegada_atual:
                return True

            agora_local = self._agora_local()

            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    data_hora_chegada = ?,
                    atualizado_em = ?
                WHERE id = ?
                  AND ativo = 1
                  AND status = ?
                """,
                (
                    agora_local,
                    agora_local,
                    solicitacao_id,
                    StatusColeta.EM_COLETA,
                ),
            )

            return cursor.rowcount > 0

    def concluir_coleta(
            self,
            solicitacao_id: int,
            quantidade_coletada: int,
            peso_coletado_kg: float,
            observacao_operacional: str = "",
    ) -> bool:
        """
        Conclui uma coleta em andamento e registra
        os dados efetivamente coletados.
        """

        with self.database.obter_conexao() as conexao:
            agora_local = self._agora_local()
            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    quantidade_sacas_coletada = ?,
                    quantidade_kg_coletado = ?,
                    observacao_operacional = ?,
                    status = ?,
                    data_hora_conclusao = ?,
                    atualizado_em = ?
                WHERE id = ?
                  AND status = ?
                """,
                (
                    quantidade_coletada,
                    peso_coletado_kg,
                    observacao_operacional,
                    StatusColeta.CONCLUIDA,
                    agora_local,  # data_hora_conclusao
                    agora_local,  # atualizado_em
                    solicitacao_id,
                    StatusColeta.EM_COLETA,
                ),
            )

            return cursor.rowcount > 0

    def cancelar_coleta(
            self,
            solicitacao_id: int,
            motivo: str,
    ) -> bool:
        """
        Cancela uma solicitação registrando
        o motivo e a data/hora do cancelamento.
        """

        motivo_normalizado = str(
            motivo or ""
        ).strip()

        if not motivo_normalizado:
            return False

        with self.database.obter_conexao() as conexao:
            agora_local = self._agora_local()
            cursor = conexao.execute(
                """
                UPDATE solicitacoes
                SET
                    status = ?,
                    motivo_cancelamento = ?,
                    data_hora_cancelamento = ?,
                    atualizado_em = ?
                WHERE id = ?
                  AND ativo = 1
                """,
                (
                    StatusColeta.CANCELADA,
                    motivo_normalizado,
                    agora_local,  # data_hora_cancelamento
                    agora_local,  # atualizado_em
                    solicitacao_id,
                ),
            )

            return cursor.rowcount > 0

    # ==========================================================
    # DISPONIBILIDADE
    # ==========================================================

    def motorista_disponivel(
            self,
            motorista_id: int,
            data_hora_agendada: str,
            *,
            solicitacao_ignorada_id: int | None = None,
            janela_minutos: int = 60,
    ) -> dict:
        """
        Verifica se um motorista está disponível no horário informado.

        A busca considera solicitações AGENDADAS ou EM_COLETA dentro
        da janela de conflito estabelecida.

        Args:
            motorista_id:
                Identificador do motorista.

            data_hora_agendada:
                Data e hora no formato AAAA-MM-DD HH:MM:SS.

            solicitacao_ignorada_id:
                Solicitação que deve ser desconsiderada na busca.
                É útil durante um reagendamento.

            janela_minutos:
                Quantidade de minutos antes e depois do horário
                considerada como conflito.

        Returns:
            Dicionário com a disponibilidade e, quando houver,
            os dados da solicitação conflitante.
        """

        if motorista_id <= 0:
            return {
                "disponivel": False,
                "mensagem": "Motorista inválido.",
                "conflito": None,
            }

        data_hora_normalizada = data_hora_agendada.strip()

        if not data_hora_normalizada:
            return {
                "disponivel": False,
                "mensagem": "Data e hora não informadas.",
                "conflito": None,
            }

        if janela_minutos < 0:
            raise ValueError(
                "A janela de conflito não pode ser negativa."
            )

        consulta = """
            SELECT
                s.id,
                s.codigo,
                s.data_hora_agendada,
                s.status,

                s.estabelecimento_id,
                e.nome AS estabelecimento_nome,

                s.motorista_id,
                m.nome AS motorista_nome

            FROM solicitacoes AS s

            INNER JOIN estabelecimentos AS e
                ON e.id = s.estabelecimento_id

            LEFT JOIN motoristas AS m
                ON m.id = s.motorista_id

            WHERE s.ativo = 1
              AND s.motorista_id = ?
              AND s.status IN (
                  'AGENDADA',
                  'EM_COLETA'
              )
              AND s.data_hora_agendada IS NOT NULL
              AND TRIM(s.data_hora_agendada) <> ''
              AND DATETIME(s.data_hora_agendada)
                  BETWEEN DATETIME(
                      ?,
                      '-' || ? || ' minutes'
                  )
                  AND DATETIME(
                      ?,
                      '+' || ? || ' minutes'
                  )
        """

        parametros: list[object] = [
            motorista_id,
            data_hora_normalizada,
            janela_minutos,
            data_hora_normalizada,
            janela_minutos,
        ]

        if solicitacao_ignorada_id is not None:
            consulta += """
                AND s.id <> ?
            """

            parametros.append(
                solicitacao_ignorada_id
            )

        consulta += """
            ORDER BY
                ABS(
                    STRFTIME(
                        '%s',
                        s.data_hora_agendada
                    )
                    -
                    STRFTIME(
                        '%s',
                        ?
                    )
                ) ASC,
                s.id ASC

            LIMIT 1
        """

        parametros.append(
            data_hora_normalizada
        )

        with self.database.obter_conexao() as conexao:
            motorista = conexao.execute(
                """
                SELECT id, nome
                FROM motoristas
                WHERE id = ?
                  AND ativo = 1
                LIMIT 1
                """,
                (motorista_id,),
            ).fetchone()

            if motorista is None:
                return {
                    "disponivel": False,
                    "mensagem": "Motorista não encontrado ou inativo.",
                    "conflito": None,
                }

            conflito = conexao.execute(
                consulta,
                parametros,
            ).fetchone()

        if conflito is None:
            return {
                "disponivel": True,
                "mensagem": "Motorista disponível.",
                "conflito": None,
            }

        conflito_dict = dict(conflito)

        return {
            "disponivel": False,
            "mensagem": (
                "Motorista indisponível. "
                f"Conflito com a coleta "
                f"{conflito_dict['codigo']}."
            ),
            "conflito": conflito_dict,
        }

    def veiculo_disponivel(
            self,
            veiculo_id: int,
            data_hora_agendada: str,
            *,
            solicitacao_ignorada_id: int | None = None,
            janela_minutos: int = 60,
    ) -> dict:
        """
        Verifica se um veículo está disponível no horário informado.

        A busca considera solicitações AGENDADAS ou EM_COLETA dentro
        da janela de conflito estabelecida.
        """

        if veiculo_id <= 0:
            return {
                "disponivel": False,
                "mensagem": "Veículo inválido.",
                "conflito": None,
            }

        data_hora_normalizada = data_hora_agendada.strip()

        if not data_hora_normalizada:
            return {
                "disponivel": False,
                "mensagem": "Data e hora não informadas.",
                "conflito": None,
            }

        if janela_minutos < 0:
            raise ValueError(
                "A janela de conflito não pode ser negativa."
            )

        consulta = """
            SELECT
                s.id,
                s.codigo,
                s.data_hora_agendada,
                s.status,

                s.estabelecimento_id,
                e.nome AS estabelecimento_nome,

                s.veiculo_id,
                v.placa AS veiculo_placa,
                v.marca AS veiculo_marca,
                v.modelo AS veiculo_modelo

            FROM solicitacoes AS s

            INNER JOIN estabelecimentos AS e
                ON e.id = s.estabelecimento_id

            LEFT JOIN veiculos AS v
                ON v.id = s.veiculo_id

            WHERE s.ativo = 1
              AND s.veiculo_id = ?
              AND s.status IN (
                  'AGENDADA',
                  'EM_COLETA'
              )
              AND s.data_hora_agendada IS NOT NULL
              AND TRIM(s.data_hora_agendada) <> ''
              AND DATETIME(s.data_hora_agendada)
                  BETWEEN DATETIME(
                      ?,
                      '-' || ? || ' minutes'
                  )
                  AND DATETIME(
                      ?,
                      '+' || ? || ' minutes'
                  )
        """

        parametros: list[object] = [
            veiculo_id,
            data_hora_normalizada,
            janela_minutos,
            data_hora_normalizada,
            janela_minutos,
        ]

        if solicitacao_ignorada_id is not None:
            consulta += """
                AND s.id <> ?
            """

            parametros.append(
                solicitacao_ignorada_id
            )

        consulta += """
            ORDER BY
                ABS(
                    STRFTIME(
                        '%s',
                        s.data_hora_agendada
                    )
                    -
                    STRFTIME(
                        '%s',
                        ?
                    )
                ) ASC,
                s.id ASC

            LIMIT 1
        """

        parametros.append(
            data_hora_normalizada
        )

        with self.database.obter_conexao() as conexao:
            veiculo = conexao.execute(
                """
                SELECT
                    id,
                    placa,
                    marca,
                    modelo
                FROM veiculos
                WHERE id = ?
                  AND ativo = 1
                LIMIT 1
                """,
                (veiculo_id,),
            ).fetchone()

            if veiculo is None:
                return {
                    "disponivel": False,
                    "mensagem": "Veículo não encontrado ou inativo.",
                    "conflito": None,
                }

            conflito = conexao.execute(
                consulta,
                parametros,
            ).fetchone()

        if conflito is None:
            return {
                "disponivel": True,
                "mensagem": "Veículo disponível.",
                "conflito": None,
            }

        conflito_dict = dict(conflito)

        return {
            "disponivel": False,
            "mensagem": (
                "Veículo indisponível. "
                f"Conflito com a coleta "
                f"{conflito_dict['codigo']}."
            ),
            "conflito": conflito_dict,
        }

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def total_por_status(
            self,
            *,
            data_inicial: str | None = None,
            data_final: str | None = None,
    ) -> dict[str, int]:
        """
        Retorna a quantidade de solicitações agrupadas por status.

        Quando um período é informado, utiliza a data operacional
        correspondente ao status atual da solicitação.
        Sem período, contabiliza todas as solicitações ativas.
        """

        totais: dict[str, int] = {
            status: 0
            for status in self._STATUS_VALIDOS
        }

        consulta = """
            SELECT
                status,
                COUNT(*) AS total
            FROM solicitacoes
            WHERE ativo = 1
        """

        parametros: list[object] = []

        inicio = (
            data_inicial.strip()
            if data_inicial and data_inicial.strip()
            else None
        )

        fim = (
            data_final.strip()
            if data_final and data_final.strip()
            else None
        )

        data_operacional = """
            CASE
                WHEN status = 'CONCLUIDA'
                    THEN COALESCE(
                        NULLIF(TRIM(data_hora_conclusao), ''),
                        NULLIF(TRIM(data_hora_agendada), ''),
                        data_solicitacao
                    )

                WHEN status = 'EM_COLETA'
                    THEN COALESCE(
                        NULLIF(TRIM(data_hora_inicio), ''),
                        NULLIF(TRIM(data_hora_agendada), ''),
                        data_solicitacao
                    )

                WHEN status = 'CANCELADA'
                    THEN COALESCE(
                        NULLIF(TRIM(data_hora_cancelamento), ''),
                        NULLIF(TRIM(data_hora_agendada), ''),
                        data_solicitacao
                    )

                WHEN status = 'AGENDADA'
                    THEN COALESCE(
                        NULLIF(TRIM(data_hora_agendada), ''),
                        data_solicitacao
                    )

                ELSE data_solicitacao
            END
        """

        if inicio and fim:
            if inicio > fim:
                raise ValueError(
                    "A data inicial não pode ser maior que a data final."
                )

            consulta += f"""
                AND DATE({data_operacional})
                    BETWEEN DATE(?) AND DATE(?)
            """

            parametros.extend([
                inicio,
                fim,
            ])

        elif inicio:
            consulta += f"""
                AND DATE({data_operacional}) >= DATE(?)
            """

            parametros.append(
                inicio
            )

        elif fim:
            consulta += f"""
                AND DATE({data_operacional}) <= DATE(?)
            """

            parametros.append(
                fim
            )

        consulta += """
            GROUP BY status
        """

        with self.database.obter_conexao() as conexao:
            registros = conexao.execute(
                consulta,
                parametros,
            ).fetchall()

        for registro in registros:
            status = str(
                registro["status"]
            ).strip().upper()

            totais[status] = int(
                registro["total"]
            )

        return totais

    # ==========================================================
    # MÉTODOS INTERNOS
    # ==========================================================

    @classmethod
    def _agora_local(cls) -> str:
        """Retorna a data e hora atual no fuso operacional."""

        return datetime.now(
            cls._FUSO_HORARIO
        ).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _consulta_base() -> str:
        """Retorna a consulta base utilizada pela agenda."""

        return """
            SELECT
                s.id,
                s.codigo,

                s.organizacao_id,
                s.estabelecimento_id,

                COALESCE(
                    o.nome,
                    e.nome,
                    'Solicitante não identificado'
                ) AS estabelecimento_nome,

                s.motorista_id,
                m.nome AS motorista_nome,

                s.veiculo_id,
                v.placa AS veiculo_placa,
                v.marca AS veiculo_marca,
                v.modelo AS veiculo_modelo,

                s.tipo_residuo,
                s.forma_acondicionamento,
                s.quantidade_prevista,
                s.peso_estimado_kg,
                s.tipo_operacao,

                s.quantidade_sacas_prevista,
                s.quantidade_kg_previsto,
                s.quantidade_sacas_coletada,
                s.quantidade_kg_coletado,

                s.status,
                s.prioridade,

                s.data_solicitacao,
                s.data_hora_agendada,
                s.data_hora_inicio,
                s.data_hora_chegada,
                s.data_hora_conclusao,

                s.observacao_cliente,
                s.observacao_operacional,
                s.motivo_cancelamento,
                s.data_hora_cancelamento,

                s.latitude,
                s.longitude,

                s.ativo,
                s.criado_em,
                s.atualizado_em

            FROM solicitacoes AS s

            LEFT JOIN organizacoes AS o
                ON o.id = s.organizacao_id

            LEFT JOIN estabelecimentos AS e
                ON e.id = s.estabelecimento_id

            LEFT JOIN motoristas AS m
                ON m.id = s.motorista_id

            LEFT JOIN veiculos AS v
                ON v.id = s.veiculo_id
        """

    @staticmethod
    def _ordenacao_padrao() -> str:
        """Retorna a ordenação padrão das consultas da agenda."""

        return """
            ORDER BY
                CASE
                    WHEN s.data_hora_agendada IS NULL
                      OR TRIM(s.data_hora_agendada) = ''
                    THEN 1
                    ELSE 0
                END,
                s.data_hora_agendada ASC,
                s.data_solicitacao ASC,
                s.id ASC
        """

    @classmethod
    def _normalizar_status(
        cls,
        status: str,
    ) -> str:
        """Normaliza e valida um status de solicitação."""

        status_normalizado = status.strip().upper()

        if status_normalizado not in cls._STATUS_VALIDOS:
            raise ValueError(
                f"Status inválido: {status}"
            )

        return status_normalizado

    def _atualizar_status(
        self,
        solicitacao_id: int,
        novo_status: str,
        campo_data: str | None = None,
    ) -> bool:
        """
        Atualiza o status de uma solicitação.

        Opcionalmente, registra a data e a hora da operação
        em um campo previamente autorizado.
        """

        if solicitacao_id <= 0:
            return False

        status_normalizado = self._normalizar_status(
            novo_status
        )

        if (
            campo_data is not None
            and campo_data not in self._CAMPOS_DATA_STATUS
        ):
            raise ValueError(
                f"Campo de data inválido: {campo_data}"
            )

        with self.database.obter_conexao() as conexao:
            registro = conexao.execute(
                """
                SELECT status
                FROM solicitacoes
                WHERE id = ?
                  AND ativo = 1
                LIMIT 1
                """,
                (solicitacao_id,),
            ).fetchone()

            if registro is None:
                return False

            status_atual = str(
                registro["status"]
            ).strip().upper()

            transicoes_permitidas = (
                self._TRANSICOES_STATUS.get(
                    status_atual,
                    set(),
                )
            )

            if status_normalizado not in transicoes_permitidas:
                return False

            agora_local = self._agora_local()

            consulta = """
                UPDATE solicitacoes
                   SET status = ?,
                       atualizado_em = ?
            """

            parametros: list[object] = [
                status_normalizado,
                agora_local,
            ]

            if campo_data is not None:
                consulta += f"""
                    , {campo_data} = ?
                """

                parametros.append(
                    agora_local
                )

            consulta += """
                 WHERE id = ?
                   AND ativo = 1
            """

            parametros.append(
                solicitacao_id
            )

            cursor = conexao.execute(
                consulta,
                parametros,
            )

            return cursor.rowcount > 0