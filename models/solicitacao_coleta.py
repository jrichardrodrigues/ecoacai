from dataclasses import dataclass
from typing import Any


STATUS_SOLICITADA = "SOLICITADA"
STATUS_PENDENTE = STATUS_SOLICITADA
STATUS_EM_ANALISE = "EM_ANALISE"
STATUS_AGENDADA = "AGENDADA"
STATUS_EM_DESLOCAMENTO = "EM_DESLOCAMENTO"
STATUS_EM_COLETA = "EM_COLETA"
STATUS_CONCLUIDA = "CONCLUIDA"
STATUS_CANCELADA = "CANCELADA"
STATUS_RECUSADA = "RECUSADA"

PRIORIDADE_NORMAL = "NORMAL"
PRIORIDADE_URGENTE = "URGENTE"
PRIORIDADE_PROGRAMADA = "PROGRAMADA"

TIPO_RESIDUO_CAROCO_ACAI = "CAROCO_ACAI"

FORMA_SACA = "SACA"
FORMA_BAG = "BAG"

OPERACAO_MANUAL = "MANUAL"
OPERACAO_MUNCK = "MUNCK"

PESO_MEDIO_SACA_KG = 50.0
PESO_MEDIO_BAG_KG = 1000.0

UNIDADE_SACAS = "SACAS"
UNIDADE_BAGS = "BAGS"
UNIDADE_KG = "KG"
UNIDADE_UNIDADES = "UNIDADES"
UNIDADE_METRO_CUBICO = "M3"
UNIDADE_CACAMBAS = "CACAMBAS"

ORIGEM_GERADOR = "GERADOR"
ORIGEM_GESTOR = "GESTOR"
ORIGEM_APP = "APP"
ORIGEM_API = "API"


@dataclass(slots=True)
class SolicitacaoColeta:
    """Representa uma solicitação de coleta da ZELURBIS."""

    id: int | None = None
    codigo: str = ""

    organizacao_id: int | None = None
    empresa_parceira_id: int | None = None
    usuario_criacao_id: int | None = None

    estabelecimento_id: int | None = None
    motorista_id: int | None = None
    veiculo_id: int | None = None

    tipo_residuo: str = TIPO_RESIDUO_CAROCO_ACAI
    forma_acondicionamento: str = FORMA_SACA
    origem: str = ORIGEM_GERADOR
    unidade_medida: str = UNIDADE_SACAS

    quantidade_prevista: int = 0
    peso_estimado_kg: float = 0.0
    tipo_operacao: str = OPERACAO_MANUAL

    quantidade_sacas_prevista: int = 0
    quantidade_kg_previsto: float = 0.0

    quantidade_sacas_coletada: int = 0
    quantidade_kg_coletado: float = 0.0

    data_solicitacao: str | None = None
    data_hora_agendada: str | None = None
    data_hora_inicio: str | None = None
    data_hora_chegada: str | None = None
    data_hora_conclusao: str | None = None

    status: str = STATUS_SOLICITADA
    prioridade: str = PRIORIDADE_NORMAL

    observacao_cliente: str = ""
    observacao_operacional: str = ""

    latitude: float | None = None
    longitude: float | None = None

    ativo: bool = True
    criado_em: str | None = None
    atualizado_em: str | None = None

    def __post_init__(self) -> None:
        self.forma_acondicionamento = (
            str(self.forma_acondicionamento or FORMA_SACA)
            .strip()
            .upper()
        )

        if self.forma_acondicionamento not in {
            FORMA_SACA,
            FORMA_BAG,
        }:
            self.forma_acondicionamento = FORMA_SACA

        self.tipo_residuo = (
            str(self.tipo_residuo or TIPO_RESIDUO_CAROCO_ACAI)
            .strip()
            .upper()
        )
        self.origem = str(self.origem or ORIGEM_GERADOR).strip().upper()
        self.status = str(self.status or STATUS_SOLICITADA).strip().upper()
        self.prioridade = str(self.prioridade or PRIORIDADE_NORMAL).strip().upper()

        if self.quantidade_prevista <= 0:
            self.quantidade_prevista = self.quantidade_sacas_prevista

        self.atualizar_planejamento()

    @property
    def numero(self) -> str:
        if self.codigo:
            return self.codigo
        if self.id is None:
            return "COL-NOVA"
        return f"COL-{self.id:06d}"

    @property
    def concluida(self) -> bool:
        return self.status == STATUS_CONCLUIDA

    @property
    def em_andamento(self) -> bool:
        return self.status in {
            STATUS_EM_DESLOCAMENTO,
            STATUS_EM_COLETA,
        }

    @property
    def solicitada(self) -> bool:
        return self.status == STATUS_SOLICITADA

    @property
    def em_analise(self) -> bool:
        return self.status == STATUS_EM_ANALISE

    @property
    def agendada(self) -> bool:
        return self.status == STATUS_AGENDADA

    @property
    def cancelada(self) -> bool:
        return self.status == STATUS_CANCELADA

    @property
    def recusada(self) -> bool:
        return self.status == STATUS_RECUSADA

    @property
    def peso_medio_por_unidade_kg(self) -> float:
        if self.forma_acondicionamento == FORMA_BAG:
            return PESO_MEDIO_BAG_KG
        return PESO_MEDIO_SACA_KG

    @property
    def requer_munck(self) -> bool:
        return self.tipo_operacao == OPERACAO_MUNCK

    def calcular_peso_estimado(self) -> float:
        quantidade = max(0, int(self.quantidade_prevista or 0))
        self.peso_estimado_kg = (
            quantidade * self.peso_medio_por_unidade_kg
        )
        return self.peso_estimado_kg

    def atualizar_tipo_operacao(self) -> str:
        if self.forma_acondicionamento == FORMA_BAG:
            self.tipo_operacao = OPERACAO_MUNCK
            self.unidade_medida = UNIDADE_BAGS
        else:
            self.tipo_operacao = OPERACAO_MANUAL
            self.unidade_medida = UNIDADE_SACAS
        return self.tipo_operacao

    def sincronizar_campos_legados(self) -> None:
        """Mantém compatibilidade temporária com o banco antigo."""

        self.quantidade_kg_previsto = self.peso_estimado_kg

        if self.forma_acondicionamento == FORMA_SACA:
            self.quantidade_sacas_prevista = (
                self.quantidade_prevista
            )
        else:
            # Valor técnico temporário para satisfazer a restrição
            # legada CHECK (quantidade_sacas_prevista > 0).
            self.quantidade_sacas_prevista = 0

    def atualizar_planejamento(self) -> None:
        self.atualizar_tipo_operacao()
        self.calcular_peso_estimado()
        self.sincronizar_campos_legados()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "organizacao_id": self.organizacao_id,
            "empresa_parceira_id": self.empresa_parceira_id,
            "usuario_criacao_id": self.usuario_criacao_id,
            "estabelecimento_id": self.estabelecimento_id,
            "motorista_id": self.motorista_id,
            "veiculo_id": self.veiculo_id,
            "tipo_residuo": self.tipo_residuo,
            "forma_acondicionamento": self.forma_acondicionamento,
            "origem": self.origem,
            "unidade_medida": self.unidade_medida,
            "quantidade_prevista": self.quantidade_prevista,
            "peso_estimado_kg": self.peso_estimado_kg,
            "tipo_operacao": self.tipo_operacao,
            "quantidade_sacas_prevista": self.quantidade_sacas_prevista,
            "quantidade_kg_previsto": self.quantidade_kg_previsto,
            "quantidade_sacas_coletada": self.quantidade_sacas_coletada,
            "quantidade_kg_coletado": self.quantidade_kg_coletado,
            "data_solicitacao": self.data_solicitacao,
            "data_hora_agendada": self.data_hora_agendada,
            "data_hora_inicio": self.data_hora_inicio,
            "data_hora_chegada": self.data_hora_chegada,
            "data_hora_conclusao": self.data_hora_conclusao,
            "status": self.status,
            "prioridade": self.prioridade,
            "observacao_cliente": self.observacao_cliente,
            "observacao_operacional": self.observacao_operacional,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "ativo": self.ativo,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }

    @classmethod
    def from_row(cls, row: Any) -> "SolicitacaoColeta":
        if row is None:
            raise ValueError(
                "Não é possível criar uma solicitação "
                "a partir de uma linha vazia."
            )

        chaves = set(row.keys())

        def obter(nome: str, padrao: Any = None) -> Any:
            return row[nome] if nome in chaves else padrao

        forma = obter("forma_acondicionamento", FORMA_SACA)
        quantidade_legada = obter("quantidade_sacas_prevista", 0)
        quantidade_prevista = obter(
            "quantidade_prevista",
            quantidade_legada,
        )

        return cls(
            id=obter("id"),
            codigo=obter("codigo", "") or "",
            organizacao_id=obter("organizacao_id"),
            empresa_parceira_id=obter("empresa_parceira_id"),
            usuario_criacao_id=obter("usuario_criacao_id"),
            estabelecimento_id=obter("estabelecimento_id"),
            motorista_id=obter("motorista_id"),
            veiculo_id=obter("veiculo_id"),
            tipo_residuo=obter(
                "tipo_residuo",
                TIPO_RESIDUO_CAROCO_ACAI,
            ),
            forma_acondicionamento=forma,
            origem=obter("origem", ORIGEM_GERADOR),
            unidade_medida=obter("unidade_medida", UNIDADE_SACAS),
            quantidade_prevista=quantidade_prevista,
            peso_estimado_kg=obter(
                "peso_estimado_kg",
                obter("quantidade_kg_previsto", 0.0),
            ),
            tipo_operacao=obter(
                "tipo_operacao",
                OPERACAO_MUNCK if forma == FORMA_BAG else OPERACAO_MANUAL,
            ),
            quantidade_sacas_prevista=quantidade_legada,
            quantidade_kg_previsto=obter("quantidade_kg_previsto", 0.0),
            quantidade_sacas_coletada=obter("quantidade_sacas_coletada", 0),
            quantidade_kg_coletado=obter("quantidade_kg_coletado", 0.0),
            data_solicitacao=obter("data_solicitacao"),
            data_hora_agendada=obter("data_hora_agendada"),
            data_hora_inicio=obter("data_hora_inicio"),
            data_hora_chegada=obter("data_hora_chegada"),
            data_hora_conclusao=obter("data_hora_conclusao"),
            status=obter("status", STATUS_SOLICITADA),
            prioridade=obter("prioridade", PRIORIDADE_NORMAL),
            observacao_cliente=obter("observacao_cliente", "") or "",
            observacao_operacional=obter("observacao_operacional", "") or "",
            latitude=obter("latitude"),
            longitude=obter("longitude"),
            ativo=bool(obter("ativo", 1)),
            criado_em=obter("criado_em"),
            atualizado_em=obter("atualizado_em"),
        )

    @classmethod
    def from_dict(cls, dados: dict) -> "SolicitacaoColeta":
        campos_validos = cls.__dataclass_fields__.keys()
        dados_filtrados = {
            campo: valor
            for campo, valor in dados.items()
            if campo in campos_validos
        }
        return cls(**dados_filtrados)
