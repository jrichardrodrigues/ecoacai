from datetime import date

from repositories.agenda_repository import AgendaRepository
from repositories.sqlite_database import SQLiteDatabase


database = SQLiteDatabase()
database.inicializar()

repository = AgendaRepository(database)


# ==========================================================
# TOTAL POR STATUS
# ==========================================================

print("\n=== TOTAL POR STATUS ===")

totais = repository.total_por_status()

for status, total in sorted(totais.items()):
    print(f"{status}: {total}")

total_repository = sum(totais.values())

with database.obter_conexao() as conexao:
    registro_total = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM solicitacoes
        WHERE ativo = 1
        """
    ).fetchone()

total_banco = int(registro_total["total"])

print("\nTotal pelo repository:", total_repository)
print("Total direto no banco:", total_banco)

assert total_repository == total_banco, (
    "O total agrupado por status não corresponde "
    "ao total de solicitações ativas."
)

print("Validação dos totais: OK")


# ==========================================================
# LOCALIZA UMA DATA VÁLIDA PARA TESTAR O PERÍODO
# ==========================================================

with database.obter_conexao() as conexao:
    registro_com_data = conexao.execute(
        """
        SELECT
            id,
            codigo,
            DATE(data_hora_agendada) AS data_agendada
        FROM solicitacoes
        WHERE ativo = 1
          AND data_hora_agendada IS NOT NULL
          AND TRIM(data_hora_agendada) <> ''
          AND DATE(data_hora_agendada) IS NOT NULL
        ORDER BY data_hora_agendada
        LIMIT 1
        """
    ).fetchone()


# ==========================================================
# AGENDA POR PERÍODO
# ==========================================================

print("\n=== AGENDA POR PERÍODO ===")

if registro_com_data is None:
    print(
        "Nenhuma solicitação com data no padrão SQLite "
        "foi encontrada."
    )
else:
    data_teste = registro_com_data["data_agendada"]

    print(
        "Data utilizada:",
        data_teste,
    )

    coletas_periodo = repository.agenda_periodo(
        data_inicial=data_teste,
        data_final=data_teste,
    )

    print(
        "Total no período:",
        len(coletas_periodo),
    )

    for coleta in coletas_periodo:
        print(
            coleta["codigo"],
            coleta["estabelecimento_nome"],
            coleta["data_hora_agendada"],
            coleta["status"],
        )

    codigos = {
        coleta["codigo"]
        for coleta in coletas_periodo
    }

    assert registro_com_data["codigo"] in codigos, (
        "A solicitação usada como referência não foi "
        "retornada pela agenda do período."
    )

    print("Validação do período: OK")


# ==========================================================
# AGENDA DE HOJE
# ==========================================================

print("\n=== AGENDA DE HOJE ===")

hoje = date.today().isoformat()

print("Data atual:", hoje)

coletas_hoje = repository.agenda_hoje()

print(
    "Total de coletas hoje:",
    len(coletas_hoje),
)

for coleta in coletas_hoje:
    print(
        coleta["codigo"],
        coleta["estabelecimento_nome"],
        coleta["data_hora_agendada"],
        coleta["status"],
    )

assert isinstance(coletas_hoje, list), (
    "agenda_hoje() deveria retornar uma lista."
)

print("Validação da agenda de hoje: OK")


# ==========================================================
# AGENDA DE HOJE FILTRADA
# ==========================================================

print("\n=== AGENDA DE HOJE — AGENDADAS ===")

agendadas_hoje = repository.agenda_hoje(
    status="AGENDADA",
)

print(
    "Total agendadas hoje:",
    len(agendadas_hoje),
)

for coleta in agendadas_hoje:
    print(
        coleta["codigo"],
        coleta["data_hora_agendada"],
        coleta["status"],
    )

assert all(
    coleta["status"] == "AGENDADA"
    for coleta in agendadas_hoje
), "A consulta retornou status diferente de AGENDADA."

print("Validação do filtro por status: OK")


# ==========================================================
# PERÍODO INVÁLIDO
# ==========================================================

print("\n=== PERÍODO INVÁLIDO ===")

try:
    repository.agenda_periodo(
        data_inicial="2026-08-10",
        data_final="2026-08-01",
    )

except ValueError as erro:
    print(
        "Erro esperado:",
        erro,
    )

else:
    raise AssertionError(
        "agenda_periodo() deveria rejeitar "
        "uma data inicial maior que a final."
    )


print("\n=== TESTE DA VERSÃO 1.3 CONCLUÍDO ===")