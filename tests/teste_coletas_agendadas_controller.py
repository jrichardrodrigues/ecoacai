from datetime import datetime, timedelta

from controllers.coletas_agendadas_controller import (
    ColetasAgendadasController,
)
from repositories.agenda_repository import AgendaRepository
from repositories.sqlite_database import SQLiteDatabase
from services.coletas_agendadas_service import (
    ColetasAgendadasService,
)


database = SQLiteDatabase()
database.inicializar()

repository = AgendaRepository(database)
service = ColetasAgendadasService(repository)
controller = ColetasAgendadasController(service)


def exibir_resultado(
    titulo: str,
    resultado,
) -> None:
    print(f"\n=== {titulo} ===")
    print("Sucesso:", resultado.sucesso)
    print("Mensagem:", resultado.mensagem)
    print("Dados:", resultado.dados)


# ==========================================================
# CONSULTAS
# ==========================================================

resultado_listar = controller.listar()

exibir_resultado(
    "LISTAR",
    resultado_listar,
)

assert resultado_listar.sucesso is True
assert isinstance(resultado_listar.dados, list)


resultado_agendadas = controller.pesquisar(
    status="AGENDADA",
)

exibir_resultado(
    "PESQUISAR AGENDADAS",
    resultado_agendadas,
)

assert resultado_agendadas.sucesso is True
assert all(
    coleta["status"] == "AGENDADA"
    for coleta in resultado_agendadas.dados
)


resultado_hoje = controller.agenda_hoje()

exibir_resultado(
    "AGENDA DE HOJE",
    resultado_hoje,
)

assert resultado_hoje.sucesso is True
assert isinstance(resultado_hoje.dados, list)


resultado_totais = controller.total_por_status()

exibir_resultado(
    "TOTAL POR STATUS",
    resultado_totais,
)

assert resultado_totais.sucesso is True
assert isinstance(resultado_totais.dados, dict)


# ==========================================================
# VALIDAÇÕES
# ==========================================================

resultado_id_invalido = controller.obter_por_id(
    0
)

exibir_resultado(
    "ID INVÁLIDO",
    resultado_id_invalido,
)

assert resultado_id_invalido.falhou is True


resultado_data_invalida = controller.pesquisar(
    data="31/07/2026",
)

exibir_resultado(
    "DATA INVÁLIDA",
    resultado_data_invalida,
)

assert resultado_data_invalida.falhou is True


resultado_periodo_invalido = controller.agenda_periodo(
    data_inicial="2026-08-10",
    data_final="2026-08-01",
)

exibir_resultado(
    "PERÍODO INVÁLIDO",
    resultado_periodo_invalido,
)

assert resultado_periodo_invalido.falhou is True


# ==========================================================
# LOCALIZA DADOS PARA TESTE OPERACIONAL
# ==========================================================

with database.obter_conexao() as conexao:
    motorista = conexao.execute(
        """
        SELECT id, nome
        FROM motoristas
        WHERE ativo = 1
        ORDER BY id
        LIMIT 1
        """
    ).fetchone()

    veiculo = conexao.execute(
        """
        SELECT id, placa, marca, modelo
        FROM veiculos
        WHERE ativo = 1
        ORDER BY id
        LIMIT 1
        """
    ).fetchone()

    solicitacao = conexao.execute(
        """
        SELECT id, codigo, status
        FROM solicitacoes
        WHERE ativo = 1
          AND status = 'PENDENTE'
        ORDER BY id
        LIMIT 1
        """
    ).fetchone()


if motorista is None:
    raise RuntimeError(
        "Nenhum motorista ativo encontrado."
    )

if veiculo is None:
    raise RuntimeError(
        "Nenhum veículo ativo encontrado."
    )

if solicitacao is None:
    raise RuntimeError(
        "Nenhuma solicitação PENDENTE encontrada."
    )


motorista_id = int(motorista["id"])
veiculo_id = int(veiculo["id"])
solicitacao_id = int(solicitacao["id"])

data_hora_futura = (
    datetime.now()
    + timedelta(days=4000)
).replace(
    hour=8,
    minute=0,
    second=0,
    microsecond=0,
).strftime(
    "%Y-%m-%d %H:%M:%S"
)


print("\n=== DADOS OPERACIONAIS ===")
print(
    "Solicitação:",
    solicitacao["codigo"],
    solicitacao["status"],
)
print(
    "Motorista:",
    motorista_id,
    motorista["nome"],
)
print(
    "Veículo:",
    veiculo_id,
    veiculo["placa"],
)
print(
    "Data futura:",
    data_hora_futura,
)


# ==========================================================
# AGENDAR
# ==========================================================

resultado_agendar = controller.agendar(
    solicitacao_id=solicitacao_id,
    data_hora_agendada=data_hora_futura,
    motorista_id=motorista_id,
    veiculo_id=veiculo_id,
)

exibir_resultado(
    "AGENDAR",
    resultado_agendar,
)

assert resultado_agendar.sucesso is True
assert resultado_agendar.dados["status"] == "AGENDADA"


# ==========================================================
# DISPONIBILIDADE
# ==========================================================

resultado_motorista = controller.motorista_disponivel(
    motorista_id=motorista_id,
    data_hora_agendada=data_hora_futura,
)

exibir_resultado(
    "MOTORISTA INDISPONÍVEL",
    resultado_motorista,
)

assert resultado_motorista.falhou is True
assert resultado_motorista.dados["disponivel"] is False


resultado_veiculo = controller.veiculo_disponivel(
    veiculo_id=veiculo_id,
    data_hora_agendada=data_hora_futura,
)

exibir_resultado(
    "VEÍCULO INDISPONÍVEL",
    resultado_veiculo,
)

assert resultado_veiculo.falhou is True
assert resultado_veiculo.dados["disponivel"] is False


# ==========================================================
# REAGENDAR
# ==========================================================

nova_data_hora = (
    datetime.strptime(
        data_hora_futura,
        "%Y-%m-%d %H:%M:%S",
    )
    + timedelta(hours=3)
).strftime(
    "%Y-%m-%d %H:%M:%S"
)

resultado_reagendar = controller.reagendar(
    solicitacao_id=solicitacao_id,
    nova_data_hora=nova_data_hora,
)

exibir_resultado(
    "REAGENDAR",
    resultado_reagendar,
)

assert resultado_reagendar.sucesso is True
assert (
    resultado_reagendar.dados["data_hora_agendada"]
    == nova_data_hora
)


# ==========================================================
# INICIAR
# ==========================================================

resultado_iniciar = controller.iniciar_coleta(
    solicitacao_id
)

exibir_resultado(
    "INICIAR",
    resultado_iniciar,
)

assert resultado_iniciar.sucesso is True
assert resultado_iniciar.dados["status"] == "EM_COLETA"


# ==========================================================
# CONCLUIR
# ==========================================================

resultado_concluir = controller.concluir_coleta(
    solicitacao_id
)

exibir_resultado(
    "CONCLUIR",
    resultado_concluir,
)

assert resultado_concluir.sucesso is True
assert resultado_concluir.dados["status"] == "CONCLUIDA"


# ==========================================================
# TRANSIÇÃO INVÁLIDA
# ==========================================================

resultado_reiniciar = controller.iniciar_coleta(
    solicitacao_id
)

exibir_resultado(
    "REINICIAR CONCLUÍDA",
    resultado_reiniciar,
)

assert resultado_reiniciar.falhou is True


print(
    "\n=== TESTE DO COLETAS AGENDADAS CONTROLLER CONCLUÍDO ==="
)