from __future__ import annotations

from repositories.sqlite_database import SQLiteDatabase


class AgendaRepository:
    """Repositório responsável pelas operações da agenda de coletas."""

    _STATUS_VALIDOS = {
        "PENDENTE",
        "AGENDADA",
        "EM_COLETA",
        "CONCLUIDA",
        "CANCELADA",
    }

    _CAMPOS_DATA_STATUS = {
        "data_hora_inicio",
        "data_hora_chegada",
        "data_hora_conclusao",
    }

    _TRANSICOES_STATUS = {
        "PENDENTE": {"AGENDADA", "CANCELADA"},
        "AGENDADA": {"EM_COLETA", "CANCELADA"},
        "EM_COLETA": {"CONCLUIDA"},
        "CONCLUIDA": set(),
        "CANCELADA": set(),
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
            status_normalizado = self._normalizar_status(status)

            consulta += """
                AND s.status = ?
            """

            parametros.append(status_normalizado)

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
                "PENDENTE",
                "AGENDADA",
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

            consulta = """
                UPDATE solicitacoes
                   SET data_hora_agendada = ?,
                       status = 'AGENDADA',
                       atualizado_em = CURRENT_TIMESTAMP
            """

            parametros: list[object] = [
                data_hora_normalizada,
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

        if status_atual != "AGENDADA":
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
            novo_status="EM_COLETA",
            campo_data="data_hora_inicio",
        )

    def concluir_coleta(
            self,
            solicitacao_id: int,
    ) -> bool:
        """
        Conclui uma coleta em andamento.

        Altera o status para CONCLUIDA e registra
        a data e a hora de conclusão.
        """

        return self._atualizar_status(
            solicitacao_id=solicitacao_id,
            novo_status="CONCLUIDA",
            campo_data="data_hora_conclusao",
        )

    def cancelar_coleta(
            self,
            solicitacao_id: int,
    ) -> bool:
        """
        Cancela uma solicitação pendente ou agendada.

        Não registra data específica de cancelamento,
        pois a tabela ainda não possui esse campo.
        """

        return self._atualizar_status(
            solicitacao_id=solicitacao_id,
            novo_status="CANCELADA",
        )

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

    # Os métodos de totais e indicadores serão implementados
    # depois das operações da agenda.

    # ==========================================================
    # MÉTODOS INTERNOS
    # ==========================================================

    @staticmethod
    def _consulta_base() -> str:
        """Retorna a consulta base utilizada pela agenda."""

        return """
            SELECT
                s.id,
                s.codigo,

                s.estabelecimento_id,
                e.nome AS estabelecimento_nome,

                s.motorista_id,
                m.nome AS motorista_nome,

                s.veiculo_id,
                v.placa AS veiculo_placa,
                v.marca AS veiculo_marca,
                v.modelo AS veiculo_modelo,

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

                s.latitude,
                s.longitude,

                s.ativo,
                s.criado_em,
                s.atualizado_em

            FROM solicitacoes AS s

            INNER JOIN estabelecimentos AS e
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

            consulta = """
                UPDATE solicitacoes
                   SET status = ?,
                       atualizado_em = CURRENT_TIMESTAMP
            """

            parametros: list[object] = [
                status_normalizado,
            ]

            if campo_data is not None:
                consulta += f"""
                    , {campo_data} = CURRENT_TIMESTAMP
                """

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