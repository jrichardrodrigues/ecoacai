from datetime import datetime


class DateUtils:
    """
    Utilitário para conversão e manipulação de datas.
    """

    FORMATO_BR = "%d/%m/%Y"
    FORMATO_ISO = "%Y-%m-%d"
    FORMATO_BANCO = "%Y-%m-%d %H:%M:%S"

    # ==========================================================
    # CONVERSÕES
    # ==========================================================

    @staticmethod
    def para_brasileiro(data_iso: str) -> str:
        """
        Converte:
            2026-08-01
        para:
            01/08/2026
        """

        if not data_iso:
            return ""

        return datetime.strptime(
            data_iso,
            DateUtils.FORMATO_ISO
        ).strftime(
            DateUtils.FORMATO_BR
        )

    @staticmethod
    def para_iso(data_br: str) -> str:
        """
        Converte:
            01/08/2026
        para:
            2026-08-01
        """

        if not data_br:
            return ""

        return datetime.strptime(
            data_br,
            DateUtils.FORMATO_BR
        ).strftime(
            DateUtils.FORMATO_ISO
        )

    @staticmethod
    def data_hora_para_banco(
        data_br: str,
        hora: str,
    ) -> str:
        """
        Converte:

        01/08/2026
        08:30

        para

        2026-08-01 08:30:00
        """

        return datetime.strptime(
            f"{data_br} {hora}",
            "%d/%m/%Y %H:%M",
        ).strftime(
            DateUtils.FORMATO_BANCO
        )

    # ==========================================================
    # DATAS ATUAIS
    # ==========================================================

    @staticmethod
    def hoje_br() -> str:
        """
        Retorna a data atual no formato brasileiro.
        """

        return datetime.now().strftime(
            DateUtils.FORMATO_BR
        )

    @staticmethod
    def hoje_iso() -> str:
        """
        Retorna a data atual no formato ISO.
        """

        return datetime.now().strftime(
            DateUtils.FORMATO_ISO
        )

    @staticmethod
    def agora_banco() -> str:
        """
        Retorna data e hora atuais
        no formato do banco.
        """

        return datetime.now().strftime(
            DateUtils.FORMATO_BANCO
        )

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    @staticmethod
    def validar_data_br(
        data: str,
    ) -> bool:

        try:

            datetime.strptime(
                data,
                DateUtils.FORMATO_BR,
            )

            return True

        except ValueError:

            return False