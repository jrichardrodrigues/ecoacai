"""
config/constants.py

Constantes compartilhadas pela plataforma ECOAÇAÍ.

Todas as constantes utilizadas pela aplicação devem ser
centralizadas neste arquivo.

Plataforma: ZELURBIS
Projeto: EcoAçaí
Versão: 2.0.0
"""

from datetime import datetime

###############################################################################
# IDENTIDADE DA APLICAÇÃO
###############################################################################

APP_NAME = "ZELURBIS"
APP_VERSION = "1.0.0"

APP_SUBTITLE = (
    "Plataforma Inteligente de Gestão Ambiental"
)

###############################################################################
# IDENTIDADE VISUAL
###############################################################################

COR_FUNDO = "#F8F4F6"

COR_SUCESSO = "#2E7D32"
COR_ERRO = "#C62828"
COR_ALERTA = "#F9A825"

# =============================================================================
# IDENTIDADE VISUAL — ZELURBIS
# =============================================================================

VERDE_SIDEBAR = "#003F32"
VERDE_SIDEBAR_ATIVO = "#275E4B"
VERDE_DESTAQUE = "#8DBF32"


# =============================================================================
# IDENTIDADE VISUAL — MÓDULOS
# =============================================================================

COR_ECOACAI = "#781946"
COR_ECOOLEO = "#8F4903"
COR_ECOGARRAFAS = "#1D1E33"

###############################################################################
# DOMÍNIO
###############################################################################

SETORES = [
    "SETOR 1",
    "SETOR 2",
    "SETOR 3",
    "SETOR 4",
    "SETOR 5",
    "SETOR 6",
]


BAIRROS_SETORES = {
    # SETOR 1
    "Jurunas": "SETOR 1",
    "Condor": "SETOR 1",
    "Batista Campos": "SETOR 1",
    "Cremação": "SETOR 1",
    "Cidade Velha": "SETOR 1",
    "Campina": "SETOR 1",
    "Reduto": "SETOR 1",
    "Umarizal": "SETOR 1",

    # SETOR 2
    "Guamá": "SETOR 2",
    "Canudos": "SETOR 2",
    "Terra Firme": "SETOR 2",
    "São Brás": "SETOR 2",
    "Nazaré": "SETOR 2",
    "Marco": "SETOR 2",
    "Fátima": "SETOR 2",
    "Curió": "SETOR 2",
    "Souza": "SETOR 2",

    # SETOR 3
    "Pedreira": "SETOR 3",
    "Telégrafo": "SETOR 3",
    "Barreiro": "SETOR 3",
    "Sacramenta": "SETOR 3",
    "Miramar": "SETOR 3",
    "Val de Cans": "SETOR 3",
    "Pratinha": "SETOR 3",
    "Marambaia": "SETOR 3",

    # SETOR 4
    "Aurá": "SETOR 4",
    "Águas Lindas": "SETOR 4",
    "Guanabara": "SETOR 4",
    "Castanheira": "SETOR 4",
    "Cabanagem": "SETOR 4",
    "Mangueirão": "SETOR 4",
    "Benguí": "SETOR 4",
    "Una": "SETOR 4",

    # SETOR 5
    "Parque Verde": "SETOR 5",
    "Tapanã": "SETOR 5",
    "Coqueiro": "SETOR 5",
    "Tenoné": "SETOR 5",
    "P. Guajará": "SETOR 5",
    "Paracuri": "SETOR 5",
    "S. Clemente": "SETOR 5",
    "Cordeiro": "SETOR 5",

    # SETOR 6
    "P. Grossa": "SETOR 6",
    "Cruzeiro": "SETOR 6",
    "Agulha": "SETOR 6",
    "Campina de Icoaraci": "SETOR 6",
    "Água Boa": "SETOR 6",
    "Maracacuera": "SETOR 6",
    "Águas Negras": "SETOR 6",
    "Brasília": "SETOR 6",
    "S. João Outeiro": "SETOR 6",
    "Itaiteua": "SETOR 6",
}

###############################################################################
# STATUS DAS SOLICITAÇÕES
###############################################################################


class StatusSolicitacao:
    PENDENTE = "PENDENTE"
    AGENDADA = "AGENDADA"
    EM_DESLOCAMENTO = "EM_DESLOCAMENTO"
    EM_COLETA = "EM_COLETA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"

    OPCOES = [
        (PENDENTE, "Pendente"),
        (AGENDADA, "Agendada"),
        (EM_DESLOCAMENTO, "Em deslocamento"),
        (EM_COLETA, "Em coleta"),
        (CONCLUIDA, "Concluída"),
        (CANCELADA, "Cancelada"),
    ]

    @classmethod
    def descricao(cls, status: str) -> str:
        descricoes = dict(cls.OPCOES)
        return descricoes.get(status, status)


###############################################################################
# STATUS DAS COLETAS
###############################################################################


class StatusColeta:
    SOLICITADA = "SOLICITADA"
    EM_ANALISE = "EM_ANALISE"
    AGENDADA = "AGENDADA"
    EM_DESLOCAMENTO = "EM_DESLOCAMENTO"
    EM_COLETA = "EM_COLETA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"
    RECUSADA = "RECUSADA"

    OPCOES = [
        (SOLICITADA, "Solicitada"),
        (EM_ANALISE, "Em análise"),
        (AGENDADA, "Agendada"),
        (EM_DESLOCAMENTO, "Em deslocamento"),
        (EM_COLETA, "Em coleta"),
        (CONCLUIDA, "Concluída"),
        (CANCELADA, "Cancelada"),
        (RECUSADA, "Recusada"),
    ]

    @classmethod
    def descricao(cls, status: str) -> str:
        descricoes = dict(cls.OPCOES)
        return descricoes.get(status, status)


###############################################################################
# STATUS DOS VEÍCULOS
###############################################################################


class StatusVeiculo:
    DISPONIVEL = "DISPONIVEL"
    EM_COLETA = "EM_COLETA"
    MANUTENCAO = "MANUTENCAO"
    INATIVO = "INATIVO"

    OPCOES = [
        (DISPONIVEL, "Disponível"),
        (EM_COLETA, "Em coleta"),
        (MANUTENCAO, "Manutenção"),
        (INATIVO, "Inativo"),
    ]

    @classmethod
    def descricao(cls, status: str) -> str:
        descricoes = dict(cls.OPCOES)
        return descricoes.get(status, status)


###############################################################################
# COMPATIBILIDADE COM NOMES ANTERIORES
###############################################################################

# Solicitações
STATUS_SOLICITACAO_PENDENTE = StatusSolicitacao.PENDENTE
STATUS_SOLICITACAO_AGENDADA = StatusSolicitacao.AGENDADA
STATUS_SOLICITACAO_EM_DESLOCAMENTO = (
    StatusSolicitacao.EM_DESLOCAMENTO
)
STATUS_SOLICITACAO_EM_COLETA = StatusSolicitacao.EM_COLETA
STATUS_SOLICITACAO_CONCLUIDA = StatusSolicitacao.CONCLUIDA
STATUS_SOLICITACAO_CANCELADA = StatusSolicitacao.CANCELADA

STATUS_SOLICITACOES = StatusSolicitacao.OPCOES

# Veículos
STATUS_VEICULO_DISPONIVEL = StatusVeiculo.DISPONIVEL
STATUS_VEICULO_EM_COLETA = StatusVeiculo.EM_COLETA
STATUS_VEICULO_MANUTENCAO = StatusVeiculo.MANUTENCAO
STATUS_VEICULO_INATIVO = StatusVeiculo.INATIVO

STATUS_VEICULOS = StatusVeiculo.OPCOES

###############################################################################
# CATÁLOGO DE VEÍCULOS
###############################################################################

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

ANOS_VEICULOS = [
    str(ano)
    for ano in range(
        datetime.now().year,
        1989,
        -1,
    )
]
