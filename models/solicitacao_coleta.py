from dataclasses import dataclass
from typing import Any


STATUS_SOLICITADA = "SOLICITADA"

# Compatibilidade temporária com módulos antigos.
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

UNIDADE_SACAS = "SACAS"
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

    # ==========================================================
    # IDENTIFICAÇÃO
    # ==========================================================

    id: int | None = None
    codigo: str = ""

    # ==========================================================
    # RELACIONAMENTOS DA NOVA ARQUITETURA
    # ==========================================================

    organizacao_id: int | None = None
    empresa_parceira_id: int | None = None
    usuario_criacao_id: int | None = None

    # ==========================================================
    # COMPATIBILIDADE COM O MODELO LEGADO
    # ==========================================================

    estabelecimento_id: int | None = None
    motorista_id: int | None = None
    veiculo_id: int | None = None

    # ==========================================================
    # RESÍDUO
    # ==========================================================

    tipo_residuo: str = TIPO_RESIDUO_CAROCO_ACAI
    unidade_medida: str = UNIDADE_SACAS
    origem: str = ORIGEM_GERADOR

    # ==========================================================
    # PLANEJAMENTO
    # ==========================================================

    quantidade_sacas_prevista: int = 0
    quantidade_kg_previsto: float = 0.0

    # ==========================================================
    # EXECUÇÃO
    # ==========================================================

    quantidade_sacas_coletada: int = 0
    quantidade_kg_coletado: float = 0.0

    # ==========================================================
    # DATAS
    # ==========================================================

    data_solicitacao: str | None = None
    data_hora_agendada: str | None = None
    data_hora_inicio: str | None = None
    data_hora_chegada: str | None = None
    data_hora_conclusao: str | None = None

    # ==========================================================
    # OPERAÇÃO
    # ==========================================================

    status: str = STATUS_SOLICITADA
    prioridade: str = PRIORIDADE_NORMAL

    # ==========================================================
    # OBSERVAÇÕES
    # ==========================================================

    observacao_cliente: str = ""
    observacao_operacional: str = ""

    # ==========================================================
    # LOCALIZAÇÃO
    # ==========================================================

    latitude: float | None = None
    longitude: float | None = None

    # ==========================================================
    # CONTROLE
    # ==========================================================

    ativo: bool = True
    criado_em: str | None = None
    atualizado_em: str | None = None

    # ==========================================================
    # PROPRIEDADES
    # ==========================================================

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

    # ==========================================================
    # CONVERSÃO
    # ==========================================================

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
            "unidade_medida": self.unidade_medida,
            "origem": self.origem,
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
    def from_row(
        cls,
        row: Any,
    ) -> "SolicitacaoColeta":
        if row is None:
            raise ValueError(
                "Não é possível criar uma solicitação "
                "a partir de uma linha vazia."
            )

        chaves = set(row.keys())

        def obter(
            nome: str,
            padrao: Any = None,
        ) -> Any:
            return row[nome] if nome in chaves else padrao

        return cls(
            id=obter("id"),
            codigo=obter("codigo", "") or "",
            organizacao_id=obter("organizacao_id"),
            empresa_parceira_id=obter(
                "empresa_parceira_id"
            ),
            usuario_criacao_id=obter(
                "usuario_criacao_id"
            ),
            estabelecimento_id=obter(
                "estabelecimento_id"
            ),
            motorista_id=obter("motorista_id"),
            veiculo_id=obter("veiculo_id"),
            tipo_residuo=obter(
                "tipo_residuo",
                TIPO_RESIDUO_CAROCO_ACAI,
            ),
            unidade_medida=obter(
                "unidade_medida",
                UNIDADE_SACAS,
            ),
            origem=obter(
                "origem",
                ORIGEM_GERADOR,
            ),
            quantidade_sacas_prevista=obter(
                "quantidade_sacas_prevista",
                0,
            ),
            quantidade_kg_previsto=obter(
                "quantidade_kg_previsto",
                0.0,
            ),
            quantidade_sacas_coletada=obter(
                "quantidade_sacas_coletada",
                0,
            ),
            quantidade_kg_coletado=obter(
                "quantidade_kg_coletado",
                0.0,
            ),
            data_solicitacao=obter(
                "data_solicitacao"
            ),
            data_hora_agendada=obter(
                "data_hora_agendada"
            ),
            data_hora_inicio=obter(
                "data_hora_inicio"
            ),
            data_hora_chegada=obter(
                "data_hora_chegada"
            ),
            data_hora_conclusao=obter(
                "data_hora_conclusao"
            ),
            status=obter(
                "status",
                STATUS_SOLICITADA,
            ),
            prioridade=obter(
                "prioridade",
                PRIORIDADE_NORMAL,
            ),
            observacao_cliente=obter(
                "observacao_cliente",
                "",
            ) or "",
            observacao_operacional=obter(
                "observacao_operacional",
                "",
            ) or "",
            latitude=obter("latitude"),
            longitude=obter("longitude"),
            ativo=bool(obter("ativo", 1)),
            criado_em=obter("criado_em"),
            atualizado_em=obter(
                "atualizado_em"
            ),
        )

    @classmethod
    def from_dict(
        cls,
        dados: dict,
    ) -> "SolicitacaoColeta":
        campos_validos = cls.__dataclass_fields__.keys()

        dados_filtrados = {
            campo: valor
            for campo, valor in dados.items()
            if campo in campos_validos
        }

        return cls(**dados_filtrados)