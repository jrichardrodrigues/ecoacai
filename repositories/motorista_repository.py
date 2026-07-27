import sqlite3

from models import Motorista
from repositories.sqlite_database import SQLiteDatabase


class MotoristaRepository:
    """Responsável pela persistência dos motoristas no SQLite."""

    def __init__(
        self,
        database: SQLiteDatabase | None = None,
    ) -> None:
        self.database = database or SQLiteDatabase()

    # ==========================================================
    # NORMALIZAÇÃO E VALIDAÇÃO
    # ==========================================================

    @staticmethod
    def _somente_digitos(valor: str) -> str:
        """Remove todos os caracteres não numéricos."""

        return "".join(
            caractere
            for caractere in str(valor or "")
            if caractere.isdigit()
        )

    @staticmethod
    def _normalizar_cnh(cnh: str) -> str:
        """
        Normaliza o número da CNH.

        Remove espaços e caracteres especiais, mantendo apenas
        letras e números em formato maiúsculo.
        """

        return "".join(
            caractere
            for caractere in str(cnh or "")
            if caractere.isalnum()
        ).upper()

    @classmethod
    def _validar_telefone(cls, telefone: str) -> str:
        """
        Valida e normaliza um telefone celular brasileiro.

        Regras:
        - deve possuir 11 dígitos;
        - deve possuir DDD diferente de 00;
        - o número deve começar com 9 após o DDD.

        Retorna o telefone contendo somente dígitos.
        """

        telefone_normalizado = cls._somente_digitos(
            telefone,
        )

        if not telefone_normalizado:
            raise ValueError(
                "O telefone celular é obrigatório.",
            )

        if len(telefone_normalizado) != 11:
            raise ValueError(
                "O telefone celular deve possuir 11 dígitos, "
                "incluindo o DDD.",
            )

        ddd = telefone_normalizado[:2]

        if ddd == "00":
            raise ValueError(
                "O DDD do telefone celular é inválido.",
            )

        if telefone_normalizado[2] != "9":
            raise ValueError(
                "Informe um número de telefone celular válido.",
            )

        return telefone_normalizado

    @staticmethod
    def _validar_dados_obrigatorios(
        motorista: Motorista,
    ) -> None:
        """Valida os campos obrigatórios do motorista."""

        if not str(motorista.nome or "").strip():
            raise ValueError(
                "O nome do motorista é obrigatório.",
            )

        if not str(motorista.cnh or "").strip():
            raise ValueError(
                "A CNH do motorista é obrigatória.",
            )

        if not str(
            motorista.categoria_cnh or "",
        ).strip():
            raise ValueError(
                "A categoria da CNH é obrigatória.",
            )

    @staticmethod
    def _from_row(
        row: sqlite3.Row,
    ) -> Motorista:
        """Converte um registro SQLite em Motorista."""

        return Motorista.from_dict(
            dict(row),
        )

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        motorista: Motorista,
    ) -> Motorista:
        """Cadastra um novo motorista."""

        self._validar_dados_obrigatorios(
            motorista,
        )

        nome = str(
            motorista.nome,
        ).strip()

        telefone = self._validar_telefone(
            motorista.telefone,
        )

        cnh = self._normalizar_cnh(
            motorista.cnh,
        )

        categoria_cnh = str(
            motorista.categoria_cnh,
        ).strip().upper()

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO motoristas (
                        nome,
                        telefone,
                        cnh,
                        categoria_cnh,
                        ativo
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        nome,
                        telefone,
                        cnh,
                        categoria_cnh,
                        int(motorista.ativo),
                    ),
                )

                motorista.id = cursor.lastrowid

        except sqlite3.IntegrityError as erro:
            mensagem = str(
                erro,
            ).lower()

            if "motoristas.telefone" in mensagem:
                raise ValueError(
                    "Telefone celular já cadastrado.",
                ) from erro

            if (
                    "motoristas.telefone" in mensagem
                    or "telefone duplicado" in mensagem
            ):
                raise ValueError(
                    "Telefone celular já cadastrado.",
                ) from erro

            raise ValueError(
                "Não foi possível cadastrar o motorista.",
            ) from erro

        motorista_salvo = self.buscar_por_id(
            motorista.id,
        )

        if motorista_salvo is None:
            raise RuntimeError(
                "O motorista foi inserido, "
                "mas não pôde ser recuperado.",
            )

        return motorista_salvo

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def buscar_por_id(
        self,
        motorista_id: int,
    ) -> Motorista | None:
        """Busca um motorista pelo identificador."""

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT
                    id,
                    nome,
                    telefone,
                    cnh,
                    categoria_cnh,
                    ativo
                FROM motoristas
                WHERE id = ?
                """,
                (
                    motorista_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._from_row(
            row,
        )

    def buscar_por_cnh(
        self,
        cnh: str,
    ) -> Motorista | None:
        """Busca um motorista pela CNH."""

        cnh_normalizada = self._normalizar_cnh(
            cnh,
        )

        if not cnh_normalizada:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT
                    id,
                    nome,
                    telefone,
                    cnh,
                    categoria_cnh,
                    ativo
                FROM motoristas
                WHERE cnh = ?
                """,
                (
                    cnh_normalizada,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._from_row(
            row,
        )

    def buscar_por_telefone(
        self,
        telefone: str,
    ) -> Motorista | None:
        """Busca um motorista pelo telefone celular."""

        telefone_normalizado = self._somente_digitos(
            telefone,
        )

        if not telefone_normalizado:
            return None

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT
                    id,
                    nome,
                    telefone,
                    cnh,
                    categoria_cnh,
                    ativo
                FROM motoristas
                WHERE telefone = ?
                """,
                (
                    telefone_normalizado,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._from_row(
            row,
        )

    # ==========================================================
    # VERIFICAÇÃO DE DUPLICIDADE
    # ==========================================================

    def telefone_existe(
        self,
        telefone: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """
        Verifica se o telefone já pertence a outro motorista.

        O parâmetro ignorar_id é utilizado durante a atualização.
        """

        telefone_normalizado = self._somente_digitos(
            telefone,
        )

        if not telefone_normalizado:
            return False

        return self._campo_existe(
            campo="telefone",
            valor=telefone_normalizado,
            ignorar_id=ignorar_id,
        )

    def cnh_existe(
        self,
        cnh: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """
        Verifica se a CNH já pertence a outro motorista.

        O parâmetro ignorar_id é utilizado durante a atualização.
        """

        cnh_normalizada = self._normalizar_cnh(
            cnh,
        )

        if not cnh_normalizada:
            return False

        return self._campo_existe(
            campo="cnh",
            valor=cnh_normalizada,
            ignorar_id=ignorar_id,
        )

    def _campo_existe(
        self,
        *,
        campo: str,
        valor: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica duplicidade nos campos permitidos."""

        campos_permitidos = {
            "telefone",
            "cnh",
        }

        if campo not in campos_permitidos:
            raise ValueError(
                f"Campo não permitido para pesquisa: {campo}",
            )

        consulta = f"""
            SELECT 1
            FROM motoristas
            WHERE {campo} = ?
        """

        parametros: list[str | int] = [
            valor,
        ]

        if ignorar_id is not None:
            consulta += " AND id != ?"
            parametros.append(
                ignorar_id,
            )

        consulta += " LIMIT 1"

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchone()

        return row is not None

    # ==========================================================
    # LISTAGEM E PAGINAÇÃO
    # ==========================================================

    def listar(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Motorista]:
        """
        Lista os motoristas com filtros opcionais.

        A pesquisa é aplicada sobre:

        - nome;
        - telefone;
        - CNH.

        O parâmetro somente_ativos aceita:

        - True: somente ativos;
        - False: somente inativos;
        - None: ativos e inativos.

        A paginação é aplicada quando limite é informado.
        """

        consulta = """
            SELECT
                id,
                nome,
                telefone,
                cnh,
                categoria_cnh,
                ativo
            FROM motoristas
            WHERE 1 = 1
        """

        parametros: list[str | int] = []

        if somente_ativos is True:
            consulta += " AND ativo = 1"

        elif somente_ativos is False:
            consulta += " AND ativo = 0"

        pesquisa_normalizada = str(
            pesquisa or "",
        ).strip()

        if pesquisa_normalizada:
            filtro_texto = (
                f"%{pesquisa_normalizada.lower()}%"
            )

            filtro_cnh = (
                f"%{self._normalizar_cnh(pesquisa_normalizada)}%"
            )

            telefone_pesquisa = self._somente_digitos(
                pesquisa_normalizada,
            )

            consulta += """
                AND (
                    LOWER(nome) LIKE ?
                    OR UPPER(cnh) LIKE ?
            """

            parametros.extend(
                [
                    filtro_texto,
                    filtro_cnh,
                ]
            )

            if telefone_pesquisa:
                consulta += """
                    OR telefone LIKE ?
                """

                parametros.append(
                    f"%{telefone_pesquisa}%",
                )

            consulta += ")"

        consulta += """
            ORDER BY nome COLLATE NOCASE
        """

        if limite is not None:
            if limite <= 0:
                raise ValueError(
                    "O limite deve ser maior que zero.",
                )

            consulta += " LIMIT ?"
            parametros.append(
                limite,
            )

            if pagina is not None:
                if pagina <= 0:
                    raise ValueError(
                        "A página deve ser maior que zero.",
                    )

                consulta += " OFFSET ?"
                parametros.append(
                    (pagina - 1) * limite,
                )

        elif pagina is not None:
            raise ValueError(
                "O limite deve ser informado para utilizar paginação.",
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
    ) -> list[Motorista]:
        """Retorna todos os motoristas ativos."""

        return self.listar(
            somente_ativos=True,
        )

    def quantidade(
        self,
        pesquisa: str = "",
        somente_ativos: bool | None = True,
    ) -> int:
        """
        Retorna a quantidade de motoristas.

        Utiliza os mesmos filtros de listar().
        """

        consulta = """
            SELECT COUNT(*)
            FROM motoristas
            WHERE 1 = 1
        """

        parametros: list[str | int] = []

        if somente_ativos is True:
            consulta += " AND ativo = 1"

        elif somente_ativos is False:
            consulta += " AND ativo = 0"

        pesquisa_normalizada = str(
            pesquisa or "",
        ).strip()

        if pesquisa_normalizada:
            filtro_texto = (
                f"%{pesquisa_normalizada.lower()}%"
            )

            filtro_cnh = (
                f"%{self._normalizar_cnh(pesquisa_normalizada)}%"
            )

            telefone_pesquisa = self._somente_digitos(
                pesquisa_normalizada,
            )

            consulta += """
                AND (
                    LOWER(nome) LIKE ?
                    OR UPPER(cnh) LIKE ?
            """

            parametros.extend(
                [
                    filtro_texto,
                    filtro_cnh,
                ]
            )

            if telefone_pesquisa:
                consulta += """
                    OR telefone LIKE ?
                """

                parametros.append(
                    f"%{telefone_pesquisa}%",
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
        motorista: Motorista,
    ) -> Motorista:
        """Atualiza os dados de um motorista."""

        if motorista.id is None:
            raise ValueError(
                "Motorista sem identificador.",
            )

        self._validar_dados_obrigatorios(
            motorista,
        )

        nome = str(
            motorista.nome,
        ).strip()

        telefone = self._validar_telefone(
            motorista.telefone,
        )

        cnh = self._normalizar_cnh(
            motorista.cnh,
        )

        categoria_cnh = str(
            motorista.categoria_cnh,
        ).strip().upper()

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    UPDATE motoristas
                    SET
                        nome = ?,
                        telefone = ?,
                        cnh = ?,
                        categoria_cnh = ?,
                        ativo = ?,
                        atualizado_em = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (
                        nome,
                        telefone,
                        cnh,
                        categoria_cnh,
                        int(motorista.ativo),
                        motorista.id,
                    ),
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        "Motorista não encontrado.",
                    )

        except sqlite3.IntegrityError as erro:
            mensagem = str(
                erro,
            ).lower()

            if (
                    "motoristas.telefone" in mensagem
                    or "telefone duplicado" in mensagem
            ):
                raise ValueError(
                    "Telefone celular já cadastrado "
                    "para outro motorista.",
                ) from erro

            if (
                    "motoristas.cnh" in mensagem
                    or "cnh duplicada" in mensagem
            ):
                raise ValueError(
                    "CNH já cadastrada para outro motorista.",
                ) from erro

        motorista_atualizado = self.buscar_por_id(
            motorista.id,
        )

        if motorista_atualizado is None:
            raise RuntimeError(
                "O motorista foi atualizado, "
                "mas não pôde ser recuperado.",
            )

        return motorista_atualizado

    # ==========================================================
    # EXCLUSÃO LÓGICA E REATIVAÇÃO
    # ==========================================================

    def excluir(
        self,
        motorista_id: int,
    ) -> bool:
        """
        Realiza a exclusão lógica de um motorista.

        O registro permanece no banco com ativo = 0.
        """

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE motoristas
                SET
                    ativo = 0,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                AND ativo = 1
                """,
                (
                    motorista_id,
                ),
            )

        return cursor.rowcount > 0

    def reativar(
        self,
        motorista_id: int,
    ) -> bool:
        """Reativa um motorista anteriormente desativado."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE motoristas
                SET
                    ativo = 1,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                AND ativo = 0
                """,
                (
                    motorista_id,
                ),
            )

        return cursor.rowcount > 0