"""
Constantes da aplicação.
"""

APP_NAME = "ECOAÇAÍ"
APP_VERSION = "1.0.0"

APP_SUBTITLE = (
    "Plataforma Inteligente de Gestão Ambiental"
)

COR_PRIMARIA = "#781946"
COR_SECUNDARIA = "#A42B69"

COR_FUNDO = "#F8F4F6"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#2D1B25"

COR_SUCESSO = "#2E7D32"
COR_ERRO = "#C62828"
COR_ALERTA = "#F9A825"

SETORES = [
    "Guamá",
    "Terra Firme",
    "Jurunas",
    "Condor",
    "Cremação",
    "Marco",
    "Nazaré",
    "São Brás",
    "Canudos",
    "Pedreira",
    "Marambaia",
    "Bengui",
    "Tapanã",
    "Icoaraci",
    "Batista Campos",
    "Umarizal",
    "Souza",
    "Cidade Velha",
    "Sacramenta",
    "Telegráfo",
    "Curió-Utinga",
]

# ============================
# STATUS DAS SOLICITAÇÕES
# ============================

STATUS_SOLICITACAO_PENDENTE = "PENDENTE"
STATUS_SOLICITACAO_AGENDADA = "AGENDADA"
STATUS_SOLICITACAO_EM_DESLOCAMENTO = "EM_DESLOCAMENTO"
STATUS_SOLICITACAO_EM_COLETA = "EM_COLETA"
STATUS_SOLICITACAO_CONCLUIDA = "CONCLUIDA"
STATUS_SOLICITACAO_CANCELADA = "CANCELADA"

STATUS_SOLICITACOES = [
    (
        STATUS_SOLICITACAO_PENDENTE,
        "Pendente",
    ),
    (
        STATUS_SOLICITACAO_AGENDADA,
        "Agendada",
    ),
    (
        STATUS_SOLICITACAO_EM_DESLOCAMENTO,
        "Em deslocamento",
    ),
    (
        STATUS_SOLICITACAO_EM_COLETA,
        "Em coleta",
    ),
    (
        STATUS_SOLICITACAO_CONCLUIDA,
        "Concluída",
    ),
    (
        STATUS_SOLICITACAO_CANCELADA,
        "Cancelada",
    ),
]

# ============================
# STATUS DOS VEÍCULOS
# ============================

STATUS_VEICULO_DISPONIVEL = "DISPONIVEL"
STATUS_VEICULO_EM_COLETA = "EM_COLETA"
STATUS_VEICULO_MANUTENCAO = "MANUTENCAO"
STATUS_VEICULO_INATIVO = "INATIVO"

STATUS_VEICULOS = [
    (STATUS_VEICULO_DISPONIVEL, "Disponível"),
    (STATUS_VEICULO_EM_COLETA, "Em coleta"),
    (STATUS_VEICULO_MANUTENCAO, "Manutenção"),
    (STATUS_VEICULO_INATIVO, "Inativo"),
]

# ===========================
# VEÍCULOS
# ===========================

MARCAS_VEICULOS = [
    "Volkswagen",
    "Mercedes-Benz",
    "Volvo",
    "Scania",
    "Iveco",
    "DAF",
    "JAC",
    "BYD",
    "Agrale",
    "Outra",
]

TIPOS_VEICULOS = [
    "Toco",
    "Truck",
    "Bitruck",
    "Carreta",
]

CAPACIDADES_VEICULOS = [
    6,
    8,
    10,
    12,
    15,
    18,
    20,
    25,
    30,
]

from datetime import datetime

ANOS_VEICULOS = [
    str(ano)
    for ano in range(
        datetime.now().year,
        1989,
        -1,
    )
]