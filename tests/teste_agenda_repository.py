from repositories.agenda_repository import AgendaRepository
from repositories.sqlite_database import SQLiteDatabase


database = SQLiteDatabase()
database.inicializar()

repository = AgendaRepository(database)

coletas = repository.listar()

print(f"Total encontrado: {len(coletas)}")

for coleta in coletas:
    print(
        coleta["codigo"],
        coleta["estabelecimento_nome"],
        coleta["data_hora_agendada"],
        coleta["status"],
    )

print("\nTeste obter_por_id:")

coleta = repository.obter_por_id(13)

if coleta:
    print(coleta)
else:
    print("Solicitação não encontrada.")

print("\n=== PESQUISAR AGENDADAS ===")

coletas_agendadas = repository.pesquisar(
    status="AGENDADA",
)

print(f"Total agendadas: {len(coletas_agendadas)}")

for coleta in coletas_agendadas:
    print(
        coleta["codigo"],
        coleta["estabelecimento_nome"],
        coleta["data_hora_agendada"],
        coleta["status"],
    )

print("\n=== REAGENDAR COLETA ===")

resultado = repository.reagendar(
    solicitacao_id=13,
    nova_data_hora="2026-08-05 08:30:00",
)

print("Resultado:", resultado)

coleta = repository.obter_por_id(13)

print(
    coleta["codigo"],
    coleta["data_hora_agendada"],
    coleta["status"],
)