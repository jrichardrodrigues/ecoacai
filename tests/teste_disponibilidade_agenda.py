from repositories.agenda_repository import AgendaRepository
from repositories.sqlite_database import SQLiteDatabase


database = SQLiteDatabase()
database.inicializar()

repository = AgendaRepository(database)


# ==========================================================
# LOCALIZA DADOS VÁLIDOS PARA O TESTE
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
        "Nenhum motorista ativo encontrado para o teste."
    )

if veiculo is None:
    raise RuntimeError(
        "Nenhum veículo ativo encontrado para o teste."
    )

if solicitacao is None:
    raise RuntimeError(
        "Nenhuma solicitação PENDENTE encontrada para o teste."
    )


motorista_id = motorista["id"]
veiculo_id = veiculo["id"]
solicitacao_id = solicitacao["id"]

data_hora_teste = "2099-01-15 08:00:00"


print("\n=== DADOS DO TESTE ===")

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
    veiculo["marca"],
    veiculo["modelo"],
)


# ==========================================================
# AGENDA UMA SOLICITAÇÃO COM MOTORISTA E VEÍCULO
# ==========================================================

print("\n=== PREPARAÇÃO DO CONFLITO ===")

resultado_agendamento = repository.agendar(
    solicitacao_id=solicitacao_id,
    data_hora_agendada=data_hora_teste,
    motorista_id=motorista_id,
    veiculo_id=veiculo_id,
)

print(
    "Solicitação agendada:",
    resultado_agendamento,
)

if not resultado_agendamento:
    raise RuntimeError(
        "Não foi possível preparar a solicitação para o teste."
    )


# ==========================================================
# MOTORISTA — CONFLITO NO MESMO HORÁRIO
# ==========================================================

print("\n=== MOTORISTA: MESMO HORÁRIO ===")

resultado_motorista = repository.motorista_disponivel(
    motorista_id=motorista_id,
    data_hora_agendada=data_hora_teste,
)

print(resultado_motorista)


# ==========================================================
# VEÍCULO — CONFLITO NO MESMO HORÁRIO
# ==========================================================

print("\n=== VEÍCULO: MESMO HORÁRIO ===")

resultado_veiculo = repository.veiculo_disponivel(
    veiculo_id=veiculo_id,
    data_hora_agendada=data_hora_teste,
)

print(resultado_veiculo)


# ==========================================================
# IGNORANDO A PRÓPRIA SOLICITAÇÃO
# ==========================================================

print("\n=== IGNORANDO A PRÓPRIA SOLICITAÇÃO ===")

motorista_ignorando = repository.motorista_disponivel(
    motorista_id=motorista_id,
    data_hora_agendada=data_hora_teste,
    solicitacao_ignorada_id=solicitacao_id,
)

veiculo_ignorando = repository.veiculo_disponivel(
    veiculo_id=veiculo_id,
    data_hora_agendada=data_hora_teste,
    solicitacao_ignorada_id=solicitacao_id,
)

print(
    "Motorista:",
    motorista_ignorando,
)

print(
    "Veículo:",
    veiculo_ignorando,
)


# ==========================================================
# FORA DA JANELA DE 60 MINUTOS
# ==========================================================

print("\n=== FORA DA JANELA DE CONFLITO ===")

horario_livre = "2099-01-15 10:01:00"

motorista_fora_janela = repository.motorista_disponivel(
    motorista_id=motorista_id,
    data_hora_agendada=horario_livre,
    janela_minutos=60,
)

veiculo_fora_janela = repository.veiculo_disponivel(
    veiculo_id=veiculo_id,
    data_hora_agendada=horario_livre,
    janela_minutos=60,
)

print(
    "Motorista:",
    motorista_fora_janela,
)

print(
    "Veículo:",
    veiculo_fora_janela,
)


# ==========================================================
# IDENTIFICADORES INVÁLIDOS
# ==========================================================

print("\n=== IDENTIFICADORES INVÁLIDOS ===")

print(
    repository.motorista_disponivel(
        motorista_id=-1,
        data_hora_agendada=data_hora_teste,
    )
)

print(
    repository.veiculo_disponivel(
        veiculo_id=-1,
        data_hora_agendada=data_hora_teste,
    )
)