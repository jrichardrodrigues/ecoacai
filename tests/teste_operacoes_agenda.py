from repositories.agenda_repository import AgendaRepository
from repositories.sqlite_database import SQLiteDatabase


database = SQLiteDatabase()
database.inicializar()

repository = AgendaRepository(database)


def exibir_solicitacao(
    titulo: str,
    solicitacao_id: int,
) -> None:
    coleta = repository.obter_por_id(solicitacao_id)

    print(f"\n=== {titulo} ===")

    if coleta is None:
        print("Solicitação não encontrada.")
        return

    print(
        coleta["codigo"],
        coleta["status"],
        coleta["data_hora_agendada"],
        coleta["data_hora_inicio"],
        coleta["data_hora_conclusao"],
    )


# ==========================================================
# FLUXO 1 — AGENDADA → EM_COLETA → CONCLUIDA
# ==========================================================

solicitacao_fluxo_id = 13

exibir_solicitacao(
    "ESTADO INICIAL DO FLUXO",
    solicitacao_fluxo_id,
)

resultado_inicio = repository.iniciar_coleta(
    solicitacao_id=solicitacao_fluxo_id,
)

print("\nResultado iniciar_coleta:", resultado_inicio)

exibir_solicitacao(
    "APÓS INICIAR",
    solicitacao_fluxo_id,
)

resultado_conclusao = repository.concluir_coleta(
    solicitacao_id=solicitacao_fluxo_id,
)

print("\nResultado concluir_coleta:", resultado_conclusao)

exibir_solicitacao(
    "APÓS CONCLUIR",
    solicitacao_fluxo_id,
)


# ==========================================================
# FLUXO 2 — PENDENTE → CANCELADA
# ==========================================================

solicitacao_cancelamento_id = 14

exibir_solicitacao(
    "ESTADO INICIAL DO CANCELAMENTO",
    solicitacao_cancelamento_id,
)

resultado_cancelamento = repository.cancelar_coleta(
    solicitacao_id=solicitacao_cancelamento_id,
)

print(
    "\nResultado cancelar_coleta:",
    resultado_cancelamento,
)

exibir_solicitacao(
    "APÓS CANCELAR",
    solicitacao_cancelamento_id,
)


# ==========================================================
# TESTES DE TRANSIÇÕES INVÁLIDAS
# ==========================================================

print("\n=== TRANSIÇÕES INVÁLIDAS ===")

resultado_reiniciar_concluida = repository.iniciar_coleta(
    solicitacao_id=solicitacao_fluxo_id,
)

print(
    "Iniciar coleta já concluída:",
    resultado_reiniciar_concluida,
)

resultado_concluir_cancelada = repository.concluir_coleta(
    solicitacao_id=solicitacao_cancelamento_id,
)

print(
    "Concluir coleta cancelada:",
    resultado_concluir_cancelada,
)