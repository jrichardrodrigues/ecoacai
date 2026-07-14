import sqlite3

from models import Estabelecimento
from repositories.sqlite_database import SQLiteDatabase


class EstabelecimentoRepository:
    """Persistência dos estabelecimentos no SQLite."""

    def __init__(
        self,
        database: SQLiteDatabase | None = None,
    ) -> None:
        self.database = database or SQLiteDatabase()

    @staticmethod
    def _somente_digitos(valor: str) -> str:
        """Remove todos os caracteres não numéricos."""

        return "".join(
            caractere
            for caractere in str(valor or "")
            if caractere.isdigit()
        )

    @staticmethod
    def _normalizar_email(email: str) -> str:
        """Normaliza o e-mail para comparação e armazenamento."""

        return str(email or "").strip().lower()

    def cadastrar(
        self,
        estabelecimento: Estabelecimento,
    ) -> Estabelecimento:
        """Cadastra um novo estabelecimento."""

        cpf = self._somente_digitos(
            estabelecimento.cpf,
        )

        celular = self._somente_digitos(
            estabelecimento.celular,
        )

        email = self._normalizar_email(
            estabelecimento.email,
        )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO estabelecimentos (
                        nome,
                        cpf,
                        email,
                        celular,
                        endereco,
                        bairro,
                        setor,
                        ativo
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        estabelecimento.nome.strip(),
                        cpf,
                        email,
                        celular,
                        estabelecimento.endereco.strip(),
                        estabelecimento.bairro.strip(),
                        estabelecimento.setor.strip(),
                        int(estabelecimento.ativo),
                    ),
                )

                estabelecimento.id = cursor.lastrowid

        except sqlite3.IntegrityError as erro:
            mensagem = str(erro).lower()

            if "estabelecimentos.cpf" in mensagem:
                raise ValueError(
                    "CPF já cadastrado.",
                ) from erro

            if "estabelecimentos.email" in mensagem:
                raise ValueError(
                    "E-mail já cadastrado.",
                ) from erro

            if "estabelecimentos.celular" in mensagem:
                raise ValueError(
                    "Celular já cadastrado.",
                ) from erro

            raise ValueError(
                "Não foi possível cadastrar o estabelecimento.",
            ) from erro

        estabelecimento_salvo = self.buscar_por_id(
            estabelecimento.id,
        )

        if estabelecimento_salvo is None:
            raise RuntimeError(
                "O estabelecimento foi inserido, "
                "mas não pôde ser recuperado."
            )

        return estabelecimento_salvo

    def buscar_por_id(
        self,
        estabelecimento_id: int,
    ) -> Estabelecimento | None:
        """Busca um estabelecimento pelo identificador."""

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM estabelecimentos
                WHERE id = ?
                """,
                (estabelecimento_id,),
            ).fetchone()

        return (
            Estabelecimento.from_row(row)
            if row
            else None
        )

    def buscar_por_cpf(
        self,
        cpf: str,
    ) -> Estabelecimento | None:
        """Busca um estabelecimento pelo CPF."""

        cpf_normalizado = self._somente_digitos(
            cpf,
        )

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                """
                SELECT *
                FROM estabelecimentos
                WHERE cpf = ?
                """,
                (cpf_normalizado,),
            ).fetchone()

        return (
            Estabelecimento.from_row(row)
            if row
            else None
        )

    def cpf_existe(
        self,
        cpf: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe um estabelecimento com o CPF."""

        return self._campo_existe(
            campo="cpf",
            valor=self._somente_digitos(cpf),
            ignorar_id=ignorar_id,
        )

    def email_existe(
        self,
        email: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe um estabelecimento com o e-mail."""

        return self._campo_existe(
            campo="email",
            valor=self._normalizar_email(email),
            ignorar_id=ignorar_id,
        )

    def celular_existe(
        self,
        celular: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica se já existe um estabelecimento com o celular."""

        return self._campo_existe(
            campo="celular",
            valor=self._somente_digitos(celular),
            ignorar_id=ignorar_id,
        )

    def _campo_existe(
        self,
        *,
        campo: str,
        valor: str,
        ignorar_id: int | None = None,
    ) -> bool:
        """Verifica duplicidade em campos permitidos."""

        campos_permitidos = {
            "cpf",
            "email",
            "celular",
        }

        if campo not in campos_permitidos:
            raise ValueError(
                f"Campo não permitido para pesquisa: {campo}",
            )

        consulta = f"""
            SELECT 1
            FROM estabelecimentos
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

    def listar(
        self,
        pesquisa: str = "",
        somente_ativos: bool = True,
        limite: int | None = None,
        pagina: int | None = None,
    ) -> list[Estabelecimento]:
        """
        Lista os estabelecimentos com filtros opcionais.

        A pesquisa é aplicada sobre:
        - nome;
        - bairro;
        - setor.

        A paginação só é aplicada quando limite é informado.
        """

        consulta = """
            SELECT *
            FROM estabelecimentos
            WHERE 1 = 1
        """

        parametros: list[str | int] = []

        if somente_ativos:
            consulta += " AND ativo = 1"

        pesquisa_normalizada = str(
            pesquisa or "",
        ).strip().lower()

        if pesquisa_normalizada:
            consulta += """
                AND (
                    LOWER(nome) LIKE ?
                    OR LOWER(bairro) LIKE ?
                    OR LOWER(setor) LIKE ?
                    OR cpf LIKE ?
                    OR celular LIKE ?
                )
            """

            filtro_texto = (
                f"%{pesquisa_normalizada}%"
            )

            filtro_numerico = (
                f"%{self._somente_digitos(pesquisa_normalizada)}%"
            )

            parametros.extend(
                [
                    filtro_texto,
                    filtro_texto,
                    filtro_texto,
                    filtro_numerico,
                    filtro_numerico,
                ]
            )

        consulta += " ORDER BY nome COLLATE NOCASE"

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

        with self.database.obter_conexao() as conexao:
            rows = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchall()

        return [
            Estabelecimento.from_row(row)
            for row in rows
        ]

    def quantidade(
        self,
        pesquisa: str = "",
        somente_ativos: bool = True,
    ) -> int:
        """
        Retorna a quantidade de estabelecimentos.

        Os filtros são os mesmos usados em listar().
        """

        consulta = """
            SELECT COUNT(*)
            FROM estabelecimentos
            WHERE 1 = 1
        """

        parametros: list[str] = []

        if somente_ativos:
            consulta += " AND ativo = 1"

        pesquisa_normalizada = str(
            pesquisa or "",
        ).strip().lower()

        if pesquisa_normalizada:
            consulta += """
                AND (
                    LOWER(nome) LIKE ?
                    OR LOWER(bairro) LIKE ?
                    OR LOWER(setor) LIKE ?
                    OR cpf LIKE ?
                    OR celular LIKE ?
                )
            """

            filtro_texto = (
                f"%{pesquisa_normalizada}%"
            )

            filtro_numerico = (
                f"%{self._somente_digitos(pesquisa_normalizada)}%"
            )

            parametros.extend(
                [
                    filtro_texto,
                    filtro_texto,
                    filtro_texto,
                    filtro_numerico,
                    filtro_numerico,
                ]
            )

        with self.database.obter_conexao() as conexao:
            row = conexao.execute(
                consulta,
                tuple(parametros),
            ).fetchone()

        return int(row[0])

    def atualizar(
        self,
        estabelecimento: Estabelecimento,
    ) -> Estabelecimento:
        """Atualiza os dados de um estabelecimento."""

        if estabelecimento.id is None:
            raise ValueError(
                "Estabelecimento sem identificador.",
            )

        cpf = self._somente_digitos(
            estabelecimento.cpf,
        )

        celular = self._somente_digitos(
            estabelecimento.celular,
        )

        email = self._normalizar_email(
            estabelecimento.email,
        )

        try:
            with self.database.obter_conexao() as conexao:
                cursor = conexao.execute(
                    """
                    UPDATE estabelecimentos
                    SET
                        nome = ?,
                        cpf = ?,
                        email = ?,
                        celular = ?,
                        endereco = ?,
                        bairro = ?,
                        setor = ?,
                        ativo = ?,
                        atualizado_em = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (
                        estabelecimento.nome.strip(),
                        cpf,
                        email,
                        celular,
                        estabelecimento.endereco.strip(),
                        estabelecimento.bairro.strip(),
                        estabelecimento.setor.strip(),
                        int(estabelecimento.ativo),
                        estabelecimento.id,
                    ),
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        "Estabelecimento não encontrado.",
                    )

        except sqlite3.IntegrityError as erro:
            mensagem = str(erro).lower()

            if "estabelecimentos.cpf" in mensagem:
                raise ValueError(
                    "CPF já cadastrado para outro estabelecimento.",
                ) from erro

            if "estabelecimentos.email" in mensagem:
                raise ValueError(
                    "E-mail já cadastrado para outro estabelecimento.",
                ) from erro

            if "estabelecimentos.celular" in mensagem:
                raise ValueError(
                    "Celular já cadastrado para outro estabelecimento.",
                ) from erro

            raise ValueError(
                "Não foi possível atualizar o estabelecimento.",
            ) from erro

        atualizado = self.buscar_por_id(
            estabelecimento.id,
        )

        if atualizado is None:
            raise RuntimeError(
                "O estabelecimento foi atualizado, "
                "mas não pôde ser recuperado."
            )

        return atualizado

    def excluir(
        self,
        estabelecimento_id: int,
    ) -> bool:
        """
        Realiza exclusão lógica.

        O registro permanece no banco com ativo = 0.
        """

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE estabelecimentos
                SET
                    ativo = 0,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                AND ativo = 1
                """,
                (estabelecimento_id,),
            )

        return cursor.rowcount > 0

    def reativar(
        self,
        estabelecimento_id: int,
    ) -> bool:
        """Reativa um estabelecimento desativado."""

        with self.database.obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                UPDATE estabelecimentos
                SET
                    ativo = 1,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                AND ativo = 0
                """,
                (estabelecimento_id,),
            )

        return cursor.rowcount > 0