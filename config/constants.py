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

APP_NAME = "ECOAÇAÍ"
APP_VERSION = "1.0.0"

APP_SUBTITLE = (
    "Plataforma Inteligente de Gestão Ambiental"
)

###############################################################################
# IDENTIDADE VISUAL
###############################################################################

COR_PRIMARIA = "#781946"
COR_SECUNDARIA = "#A42B69"

COR_FUNDO = "#F8F4F6"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#2D1B25"

COR_SUCESSO = "#2E7D32"
COR_ERRO = "#C62828"
COR_ALERTA = "#F9A825"

###############################################################################
# DOMÍNIO
###############################################################################

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
    PENDENTE = "PENDENTE"
    AGENDADA = "AGENDADA"
    EM_COLETA = "EM_COLETA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"

    OPCOES = [
        (PENDENTE, "Pendente"),
        (AGENDADA, "Agendada"),
        (EM_COLETA, "Em coleta"),
        (CONCLUIDA, "Concluída"),
        (CANCELADA, "Cancelada"),
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