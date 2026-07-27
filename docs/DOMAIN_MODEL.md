# DOMAIN MODEL

# ZELURBIS

> Modelo de Domínio da Plataforma

---

## 1. Introdução

O Modelo de Domínio descreve os conceitos fundamentais da plataforma ZELURBIS de forma independente da tecnologia, estabelecendo uma linguagem comum para analistas, desenvolvedores e gestores.

## 2. Objetivos

- Representar o negócio.
- Padronizar a linguagem.
- Guiar a implementação.
- Favorecer reutilização.
- Sustentar a evolução da plataforma.

## 3. Visão Geral

```text
ZELURBIS
│
├── Plataforma
├── EcoAçaí
├── EcoEntulho
├── EcoPoda
└── EcoRecicla
```

## 4. Contextos de Domínio

- Plataforma
- EcoAçaí
- Logística
- Operacional
- Administrativo

## 5. Contexto Plataforma

### Usuário
Representa qualquer pessoa autorizada a utilizar a plataforma.

### Perfil
Define o conjunto de permissões de um usuário.

### Permissão
Representa uma autorização específica dentro do sistema.

### Notificação
Comunicações enviadas pela plataforma.

### Auditoria
Registro das operações relevantes.

## 6. Contexto EcoAçaí

### Estabelecimento
Origem das solicitações de coleta.

### Cooperativa
Gerencia e distribui as operações.

### Empresa Parceira
Executa operações em conjunto com a cooperativa.

## 7. Contexto Logístico

- Motorista
- Veículo
- Rota
- Agenda

## 8. Contexto Operacional

- Solicitação
- Coleta
- Pesagem
- Destinação
- Histórico

Estados da Solicitação:

- Aberta
- Em análise
- Agendada
- Em coleta
- Finalizada
- Cancelada

## 9. Contexto Administrativo

- Dashboard
- Relatórios
- Indicadores

## 10. Relacionamentos

```text
Usuário
 ├── possui Perfil
 ├── possui Permissões
 └── realiza operações

Estabelecimento
 └── cria Solicitações

Solicitação
 └── gera Coleta

Coleta
 ├── possui Pesagem
 └── possui Destinação

Motorista
 └── executa Coletas

Cooperativa
 └── gerencia Solicitações
```

## 11. Agregados

- Usuário
- Estabelecimento
- Solicitação

## 12. Objetos de Valor

- Endereço
- Telefone
- E-mail
- Localização

## 13. Eventos de Domínio

- Usuário cadastrado
- Estabelecimento cadastrado
- Solicitação criada
- Solicitação agendada
- Coleta iniciada
- Coleta finalizada
- Pesagem registrada
- Destinação confirmada

## 14. Regras de Negócio

- Usuários devem estar autenticados.
- Um estabelecimento pode possuir várias solicitações.
- Uma solicitação gera no máximo uma coleta.
- Toda coleta deve possuir motorista.
- Toda coleta deve registrar a pesagem.
- Operações relevantes devem ser auditadas.

## 15. Fluxo Operacional

```text
Estabelecimento
      ↓
Solicita coleta
      ↓
Cooperativa
      ↓
Agenda
      ↓
Motorista
      ↓
Coleta
      ↓
Pesagem
      ↓
Destinação
      ↓
Finalização
```

## 16. Glossário

**Estabelecimento** — Local onde ocorre a geração do material.

**Solicitação** — Pedido formal de coleta.

**Coleta** — Execução operacional da solicitação.

**Pesagem** — Registro do peso coletado.

**Destinação** — Destino final do material.

## Considerações Finais

Este documento estabelece a base conceitual da plataforma ZELURBIS. Todas as implementações técnicas devem refletir os conceitos aqui definidos.

> **Toda solução começa com o zelo.**
