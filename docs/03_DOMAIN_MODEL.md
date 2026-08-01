# ZELURBIS

> **Tecnologia a serviço da sustentabilidade.**

# DOMAIN_MODEL.md

**Versão:** 2.1.0  
**Status:** Modelo Base

---

# Histórico de Versões

| Versão | Status | Descrição |
|---------|--------|-----------|
| 2.0.0 | Oficial | Primeira consolidação do modelo de domínio. |
| 2.1.0 | Modelo Base | Estrutura expandida para documentação das entidades e regras de negócio. |

---

# 1. Objetivo

Este documento descreve o modelo de domínio da plataforma ZELURBIS, apresentando as entidades de negócio, seus relacionamentos e as principais regras que orientam a plataforma.

---

# 2. Visão Geral do Domínio

```text
Usuário
    │
    ├── Estabelecimento
    │        │
    │        └── Solicitação de Coleta
    │                     │
    │                     └── Agenda de Coleta
    │                               │
    │                               ├── Motorista
    │                               └── Veículo
```

---

# 3. Entidades do Domínio

Cada entidade deverá ser documentada utilizando o padrão abaixo.

## Nome da Entidade

### Descrição

Finalidade da entidade.

### Responsabilidades

- Responsabilidade 1
- Responsabilidade 2

### Principais Atributos

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|

### Relacionamentos

| Entidade | Tipo |
|-----------|------|

### Regras de Negócio

- Regra 1
- Regra 2

### Ciclo de Vida

```text
Criado
 ↓
Ativo
 ↓
Atualizado
 ↓
Inativo/Encerrado
```

---

# 4. Entidades Atuais da Plataforma

- Usuário
- Estabelecimento
- Motorista
- Veículo
- Solicitação de Coleta
- Agenda de Coleta

---

# 5. Princípios do Modelo de Domínio

- Uma entidade representa um conceito de negócio.
- Regras de negócio pertencem aos Services.
- Models representam estado e identidade.
- O domínio deve permanecer independente da interface.

---

# 6. Considerações Finais

O modelo de domínio deverá evoluir juntamente com a plataforma, preservando simplicidade, clareza e consistência.
