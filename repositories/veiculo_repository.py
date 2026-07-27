import sqlite3

from models import Veiculo
from repositories.sqlite_database import SQLiteDatabase


class VeiculoRepository:
    """Responsável pela persistência dos veículos no SQLite."""

    def __init__(
        self,
        database: SQLiteDatabase | None = None,
    ) -> None:
        self.database = database or SQLiteDatabase()

    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================

    @staticmethod
    def _normalizar_placa(placa: str) -> str:
        """
        Normaliza a placa do veículo.

        Remove espaços, hífens e outros caracteres especiais,
        mantendo somente letras e números em formato maiúsculo.
        """

        return "".join(
            caractere
            for caractere in str(placa or "")
            if caractere.isalnum()
        ).upper()

    @staticmethod
    def _normalizar_texto(valor: str) -> str:
        """Remove espaços extras do início e do final."""

        return str(valor or "").strip()

    @staticmethod
    def _normalizar_status(status: str) -> str:
        """Normaliza o status do veículo."""

        return str(
            status or "DISPONIVEL",
        ).strip().upper()

    @staticmethod
    def _from_row(
        row: sqlite3.Row,
    ) -> Veiculo:
        """Converte um registro SQLite em Veiculo."""

        return Veiculo.from_dict(
            dict(row),
        )

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        veiculo: Veiculo,
    ) -> Veiculo:
        """Cadastra um novo veículo."""

        placa = self._normalizar_placa(
            veiculo.placa,
        )

        marca = self._normalizar_texto(
            veiculo.marca,
        )

        modelo = self._normalizar_texto(
            veiculo.modelo,
        )

        tipo = self._normalizar_texto(
            veiculo.tipo,
        )

        status = self._normalizar_status(
            veiculo.status,
        )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO veiculos (
                        placa,
                        marca,
                        modelo,
                        ano,
                        tipo,
                        capacidade,
                        motorista_id,
                        status,
                        ativo
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        placa,
                        marca,
                        modelo,
                        veiculo.ano,
                        tipo,
                        veiculo.capacidade or 0,
                        veiculo.motorista_id,
                        status,
                        int(veiculo.ativo),
                    ),
                )

                veiculo.id = cursor.lastrowid

        except sqlite3.IntegrityError as erro:
            mensagem = str(
                erro,
            ).lower()

            if (
                "veiculos.placa" in mensagem
                or "idx_veiculos_placa_unica" in mensagem
            ):
                raise ValueError(
                    "Placa já cadastrada.",
                ) from erro

            if "foreign key constraint failed" in mensagem:
                raise ValueError(
                    "O motorista informado não existe.",
                ) from erro

            raise ValueError(
                "Não foi possível cadastrar o veículo.",
            ) from erro

        veiculo_salvo = self.buscar_por_id(
            veiculo.id,
        )

        if veiculo_salvo is None:
            raise RuntimeError(
                "O veículo foi inserido, "
                "mas não pôde ser recuperado.",
            )

        return veiculo_salvo

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        veiculo_id: int,
    ) -> Veiculo | None:
        """Busca um veículo pelo identificador."""

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT
                    id,
                    placa,
                    marca,
                    modelo,
                    ano,
                    tipo,
                    capacidade,
                    motorista_id,
                    status,
                    ativo
                FROM veiculos
                WHERE id = ?
                """,
                (
                    veiculo_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._from_row(
            row,
        )

    def buscar_por_placa(
        self,
        placa: str,
    ) -> Veiculo | None:
        """Busca um veículo pela placa."""

        placa_normalizada = self._normalizar_placa(
            placa,
        )

        if not placa_normalizada:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT
                    id,
                    placa,
                    marca,
                    modelo,
                    ano,
                    tipo,
                    capacidade,
                    motorista_id,
                    status,
                    ativo
                FROM veiculos
                WHERE placa = ?
                """,
                (
                    placa_normalizada,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._from_row(
            row,
        )

    def listar(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Veiculo]:
        """
        Lista os veículos.

        Permite pesquisa por:

        - placa;
        - marca;
        - modelo;
        - tipo;
        - status;
        - nome do motorista.
        """

        consulta = """
            SELECT
                v.id,
                v.placa,
                v.marca,
                v.modelo,
                v.ano,
                v.tipo,
                v.capacidade,
                v.motorista_id,
                v.status,
                v.ativo
            FROM veiculos AS v
            LEFT JOIN motoristas AS m
                ON m.id = v.motorista_id
            WHERE 1 = 1
        """

        parametros: list[str | int] = []

        if somente_ativos is True:
            consulta += """
                AND v.ativo = 1
            """

        elif somente_ativos is False:
            consulta += """
                AND v.ativo = 0
            """

        pesquisa_normalizada = str(
            pesquisa or "",
        ).strip()

        if pesquisa_normalizada:
            filtro = (
                f"%{pesquisa_normalizada.lower()}%"
            )

            placa_pesquisa = self._normalizar_placa(
                pesquisa_normalizada,
            )

            consulta += """
                AND (
                    LOWER(v.marca) LIKE ?
                    OR LOWER(v.modelo) LIKE ?
                    OR LOWER(v.tipo) LIKE ?
                    OR LOWER(v.status) LIKE ?
                    OR LOWER(COALESCE(m.nome, '')) LIKE ?
            """

            parametros.extend(
                [
                    filtro,
                    filtro,
                    filtro,
                    filtro,
                    filtro,
                ]
            )

            if placa_pesquisa:
                consulta += """
                    OR v.placa LIKE ?
                """

                parametros.append(
                    f"%{placa_pesquisa}%",
                )

            consulta += ")"

        consulta += """
            ORDER BY
                v.marca COLLATE NOCASE,
                v.modelo COLLATE NOCASE,
                v.placa COLLATE NOCASE
        """

        if limite is not None:
            if limite <= 0:
                raise ValueError(
                    "O limite deve ser maior que zero.",
                )

            consulta += """
                LIMIT ?
            """

            parametros.append(
                limite,
            )

            if pagina is not None:
                if pagina <= 0:
                    raise ValueError(
                        "A página deve ser maior que zero.",
                    )

                consulta += """
                    OFFSET ?
                """

                parametros.append(
                    (pagina - 1) * limite,
                )

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return [
            self._from_row(row)
            for row in rows
        ]

    def listar_ativos(
        self,
    ) -> list[Veiculo]:
        """Retorna somente os veículos ativos."""

        return self.listar(
            somente_ativos=True,
        )

    def listar_disponiveis(
        self,
    ) -> list[Veiculo]:
        """Retorna os veículos ativos e disponíveis."""

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                """
                SELECT
                    id,
                    placa,
                    marca,
                    modelo,
                    ano,
                    tipo,
                    capacidade,
                    motorista_id,
                    status,
                    ativo
                FROM veiculos
                WHERE ativo = 1
                  AND status = 'DISPONIVEL'
                ORDER BY
                    marca COLLATE NOCASE,
                    modelo COLLATE NOCASE,
                    placa COLLATE NOCASE
                """
            ).fetchall()

        return [
            self._from_row(row)
            for row in rows
        ]

    def listar_por_motorista(
        self,
        motorista_id: int,
        somente_ativos: bool = True,
    ) -> list[Veiculo]:
        """Retorna os veículos vinculados a um motorista."""

        consulta = """
            SELECT
                id,
                placa,
                marca,
                modelo,
                ano,
                tipo,
                capacidade,
                motorista_id,
                status,
                ativo
            FROM veiculos
            WHERE motorista_id = ?
        """

        parametros: list[int] = [
            motorista_id,
        ]

        if somente_ativos:
            consulta += """
                AND ativo = 1
            """

        consulta += """
            ORDER BY
                marca COLLATE NOCASE,
                modelo COLLATE NOCASE,
                placa COLLATE NOCASE
        """

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return [
            self._from_row(row)
            for row in rows
        ]

    # ==========================================================
    # VERIFICAÇÃO DE DUPLICIDADE
    # ==========================================================

    def placa_existe(
        self,
        placa: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """
        Verifica se a placa já pertence a outro veículo.

        O parâmetro ignorar_id é utilizado durante a atualização.
        """

        placa_normalizada = self._normalizar_placa(
            placa,
        )

        if not placa_normalizada:
            return False

        consulta = """
            SELECT 1
            FROM veiculos
            WHERE placa = ?
        """

        parametros: list[str | int] = [
            placa_normalizada,
        ]

        if ignorar_id is not None:
            consulta += """
                AND id != ?
            """

            parametros.append(
                ignorar_id,
            )

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
    # CONTAGEM
    # ==========================================================

    def quantidade(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
    ) -> int:
        """Retorna a quantidade de veículos."""

        consulta = """
            SELECT COUNT(DISTINCT v.id)
            FROM veiculos AS v
            LEFT JOIN motoristas AS m
                ON m.id = v.motorista_id
            WHERE 1 = 1
        """

        parametros: list[str | int] = []

        if somente_ativos is True:
            consulta += """
                AND v.ativo = 1
            """

        elif somente_ativos is False:
            consulta += """
                AND v.ativo = 0
            """

        pesquisa_normalizada = str(
            pesquisa or "",
        ).strip()

        if pesquisa_normalizada:
            filtro = (
                f"%{pesquisa_normalizada.lower()}%"
            )

            placa_pesquisa = self._normalizar_placa(
                pesquisa_normalizada,
            )

            consulta += """
                AND (
                    LOWER(v.marca) LIKE ?
                    OR LOWER(v.modelo) LIKE ?
                    OR LOWER(v.tipo) LIKE ?
                    OR LOWER(v.status) LIKE ?
                    OR LOWER(COALESCE(m.nome, '')) LIKE ?
            """

            parametros.extend(
                [
                    filtro,
                    filtro,
                    filtro,
                    filtro,
                    filtro,
                ]
            )

            if placa_pesquisa:
                consulta += """
                    OR v.placa LIKE ?
                """

                parametros.append(
                    f"%{placa_pesquisa}%",
                )

            consulta += ")"

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchone()

        return int(
            row[0],
        )

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def atualizar(
        self,
        veiculo: Veiculo,
    ) -> Veiculo:
        """Atualiza os dados de um veículo."""

        if veiculo.id is None:
            raise ValueError(
                "Veículo sem identificador.",
            )

        placa = self._normalizar_placa(
            veiculo.placa,
        )

        marca = self._normalizar_texto(
            veiculo.marca,
        )

        modelo = self._normalizar_texto(
            veiculo.modelo,
        )

        tipo = self._normalizar_texto(
            veiculo.tipo,
        )

        status = self._normalizar_status(
            veiculo.status,
        )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    UPDATE veiculos
                    SET
                        placa = ?,
                        marca = ?,
                        modelo = ?,
                        ano = ?,
                        tipo = ?,
                        capacidade = ?,
                        motorista_id = ?,
                        status = ?,
                        ativo = ?,
                        atualizado_em = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (
                        placa,
                        marca,
                        modelo,
                        veiculo.ano,
                        tipo,
                        veiculo.capacidade or 0,
                        veiculo.motorista_id,
                        status,
                        int(veiculo.ativo),
                        veiculo.id,
                    ),
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        "Veículo não encontrado.",
                    )

        except sqlite3.IntegrityError as erro:
            mensagem = str(
                erro,
            ).lower()

            if (
                "veiculos.placa" in mensagem
                or "idx_veiculos_placa_unica" in mensagem
            ):
                raise ValueError(
                    "Placa já cadastrada para outro veículo.",
                ) from erro

            if "foreign key constraint failed" in mensagem:
                raise ValueError(
                    "O motorista informado não existe.",
                ) from erro

            raise ValueError(
                "Não foi possível atualizar o veículo.",
            ) from erro

        veiculo_atualizado = self.buscar_por_id(
            veiculo.id,
        )

        if veiculo_atualizado is None:
            raise RuntimeError(
                "O veículo foi atualizado, "
                "mas não pôde ser recuperado.",
            )

        return veiculo_atualizado

    # ==========================================================
    # EXCLUSÃO LÓGICA E REATIVAÇÃO
    # ==========================================================

    def excluir(
        self,
        veiculo_id: int,
    ) -> bool:
        """
        Realiza a exclusão lógica de um veículo.

        O registro permanece no banco com ativo = 0.
        """

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE veiculos
                SET
                    ativo = 0,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND ativo = 1
                """,
                (
                    veiculo_id,
                ),
            )

        return cursor.rowcount > 0

    def reativar(
        self,
        veiculo_id: int,
    ) -> bool:
        """Reativa um veículo anteriormente desativado."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE veiculos
                SET
                    ativo = 1,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND ativo = 0
                """,
                (
                    veiculo_id,
                ),
            )

        return cursor.rowcount > 0

    def alterar_status(
        self,
        veiculo_id: int,
        status: str,
    ) -> bool:
        """Altera somente o status operacional do veículo."""

        status_normalizado = self._normalizar_status(
            status,
        )

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE veiculos
                SET
                    status = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    status_normalizado,
                    veiculo_id,
                ),
            )

        return cursor.rowcount > 0