from repositories.solicitacao_coleta_repository import (
    SolicitacaoColetaRepository,
)


class RelatorioService:
    """
    Serviço responsável pela preparação dos dados
    utilizados nos relatórios da operação.
    """

    def __init__(
            self,
            solicitacao_repository: SolicitacaoColetaRepository | None = None,
    ):
        self.solicitacao_repository = (
            solicitacao_repository
            or SolicitacaoColetaRepository()
        )

    # ==========================================================
    # COLETAS POR SETOR
    # ==========================================================

    def obter_coletas_por_setor(
            self,
            *,
            setor: str | None = None,
            bairro: str | None = None,
            estabelecimento_id: int | None = None,
            data_inicial: str | None = None,
            data_final: str | None = None,
            organizacao_id: int | None = None,
    ) -> dict:
        """
        Retorna os dados preparados para o relatório
        de coletas realizadas por setor.

        Considera somente coletas concluídas, conforme
        regra aplicada pelo repository.
        """

        setor_normalizado = (
            setor.strip()
            if setor and setor.strip()
            else None
        )

        if (
                setor_normalizado
                and setor_normalizado.upper() == "TODOS"
        ):
            setor_normalizado = None

        bairro_normalizado = (
            bairro.strip()
            if bairro and bairro.strip()
            else None
        )

        if (
                bairro_normalizado
                and bairro_normalizado.upper() == "TODOS"
        ):
            bairro_normalizado = None
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

        if inicio and fim and inicio > fim:
            raise ValueError(
                "A data inicial não pode ser maior "
                "que a data final."
            )

        registros = (
            self.solicitacao_repository
            .listar_coletas_para_relatorio(
                setor=setor_normalizado,
                bairro=bairro_normalizado,
                estabelecimento_id=estabelecimento_id,
                data_inicial=inicio,
                data_final=fim,
                organizacao_id=organizacao_id,
            )
        )

        total_coletas = len(registros)

        total_sacas = 0
        total_bags = 0
        total_kg = 0.0

        for registro in registros:
            forma = (
                    registro.get("forma_acondicionamento")
                    or ""
            ).strip().upper()

            quantidade = (
                    registro.get("quantidade_sacas_coletada")
                    or 0
            )

            peso = (
                    registro.get("quantidade_kg_coletado")
                    or 0
            )

            if forma == "SACA":
                total_sacas += int(quantidade)

            elif forma == "BAG":
                total_bags += int(quantidade)

            total_kg += float(peso)

        return {
            "titulo": "Relatório de Coletas por Setor",

            "filtros": {
                "setor": setor_normalizado,
                "bairro": bairro_normalizado,
                "data_inicial": inicio,
                "data_final": fim,
            },

            "resumo": {
                "total_coletas": total_coletas,
                "total_sacas": total_sacas,
                "total_bags": total_bags,
                "total_kg": total_kg,
            },

            "registros": registros,
        }

    # ==========================================================
    # COLETAS POR SOLICITANTE
    # ==========================================================

    def obter_coletas_por_solicitante(
            self,
            *,
            estabelecimento_id: int,
            data_inicial: str | None = None,
            data_final: str | None = None,
            organizacao_id: int | None = None,
    ) -> dict:
        """
        Retorna os dados preparados para o relatório
        de coletas realizadas por solicitante.

        Considera somente coletas concluídas, conforme
        regra aplicada pelo repository.
        """

        if estabelecimento_id is None or estabelecimento_id <= 0:
            raise ValueError(
                "O solicitante deve ser informado."
            )

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

        if inicio and fim and inicio > fim:
            raise ValueError(
                "A data inicial não pode ser maior "
                "que a data final."
            )

        registros = (
            self.solicitacao_repository
            .listar_coletas_para_relatorio(
                estabelecimento_id=estabelecimento_id,
                data_inicial=inicio,
                data_final=fim,
                organizacao_id=organizacao_id,
            )
        )

        total_coletas = len(registros)

        total_sacas = 0
        total_bags = 0
        total_kg = 0.0

        for registro in registros:
            forma = (
                    registro.get("forma_acondicionamento")
                    or ""
            ).strip().upper()

            quantidade = (
                    registro.get("quantidade_sacas_coletada")
                    or 0
            )

            peso = (
                    registro.get("quantidade_kg_coletado")
                    or 0
            )

            if forma == "SACA":
                total_sacas += int(quantidade)

            elif forma == "BAG":
                total_bags += int(quantidade)

            total_kg += float(peso)

        solicitante = None

        if registros:
            solicitante = (
                    registros[0].get("solicitante")
                    or None
            )

        return {
            "titulo": "Relatório de Coletas por Solicitante",

            "filtros": {
                "estabelecimento_id": estabelecimento_id,
                "solicitante": solicitante,
                "data_inicial": inicio,
                "data_final": fim,
            },

            "resumo": {
                "total_coletas": total_coletas,
                "total_sacas": total_sacas,
                "total_bags": total_bags,
                "total_kg": total_kg,
            },

            "registros": registros,
        }