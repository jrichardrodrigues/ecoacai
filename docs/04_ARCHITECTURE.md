# ZELURBIS

> **Tecnologia a serviço da sustentabilidade.**

# ARCHITECTURE.md

**Versão:** 2.1.0  
**Status:** Oficial

---

# Histórico de Versões

| Versão | Status | Descrição |
|---------|--------|-----------|
| 1.0.0 | Oficial | Primeira arquitetura da plataforma. |
| 2.0.0 | Oficial | Consolidação da arquitetura em camadas da ZELURBIS. |
| 2.1.0 | Oficial | Inclusão da organização dos componentes, fluxo arquitetural, dependências entre camadas, organização das Views e evolução arquitetural. |

---

# 1. Introdução

A arquitetura da ZELURBIS foi concebida para sustentar o desenvolvimento de uma plataforma tecnológica voltada à gestão urbana sustentável.

Mais do que organizar código, ela estabelece princípios que garantem evolução contínua, reutilização de componentes, baixo acoplamento e facilidade de manutenção.

A primeira solução desenvolvida sobre esta arquitetura é o EcoAçaí, mas toda a estrutura foi planejada para acomodar novas soluções preservando consistência.

---

# 2. Filosofia da Arquitetura

> **Uma boa arquitetura não limita a evolução. Ela a torna possível.**

Toda decisão arquitetural deve privilegiar:

- simplicidade;
- clareza;
- baixo acoplamento;
- alta coesão;
- reutilização;
- documentação contínua;
- evolução incremental.

---

# 3. Visão Geral da Plataforma

```text
                    ZELURBIS

               Plataforma Corporativa

        EcoAçaí   |   Futuras Soluções   |   APIs

Views
   ↓
Controllers
   ↓
Services
   ↓
Repositories
   ↓
SQLite (ou outro mecanismo de persistência)
```

---

# 4. Arquitetura em Camadas

Fluxo principal:

Views → Controllers → Services → Repositories → Banco de Dados

Cada camada conhece apenas a imediatamente inferior.

---

# 5. Princípios Arquiteturais

- Separação de responsabilidades;
- Componentização;
- Reutilização;
- Independência da persistência;
- Independência da interface;
- Escalabilidade;
- Testabilidade;
- Baixo acoplamento;
- Alta coesão.

---

# 6. Estrutura Física da Plataforma

```text
ecoacai/

assets/
components/
config/
controllers/
data/
database/
docs/
models/
repositories/
services/
tests/
utils/
views/
```

---

# 7. Organização dos Componentes

```text
components/

buttons/
cards/
dialogs/
fields/
layout/
tables/
```

Todo elemento reutilizável deve ser transformado em componente.

---

# 8. Organização dos Utilitários

```text
utils/

date_utils.py
validators.py
formatters.py
messages.py
```

Os utilitários não devem depender das Views.

---

# 9. Fluxo Arquitetural das Operações

```text
Usuário
 ↓
View
 ↓
Controller
 ↓
Service
 ↓
Repository
 ↓
Banco de Dados
 ↓
Repository
 ↓
Service
 ↓
Controller
 ↓
View
 ↓
Usuário
```

---

# 10. Dependências Arquiteturais

Permitidas:

Views → Controllers → Services → Repositories

Proibidas:

- View → Repository
- Controller → Banco de Dados
- Service → Componentes gráficos

---

# 11. Organização das Views

```text
CONSTRUÇÃO

CARREGAMENTO

EVENTOS

VALIDAÇÕES

AUXILIARES
```

---

# 12. Organização dos Testes

```text
tests/

repositories/
services/
controllers/
views/
components/
```

---

# 13. Evolução Arquitetural

```text
JSON
 ↓
SQLite
 ↓
Agenda
 ↓
Dashboard
 ↓
Componentização
 ↓
Documentação Técnica
 ↓
Futuras APIs
 ↓
Novas Soluções
```

---

# 14. Princípios de Evolução

Toda decisão arquitetural deve:

- simplificar a plataforma;
- reduzir acoplamento;
- facilitar manutenção;
- incentivar reutilização;
- preservar a arquitetura;
- permitir evolução futura.

---

# 15. Considerações Finais

A arquitetura da ZELURBIS estabelece princípios para garantir a evolução sustentável da plataforma.

> **Uma boa arquitetura não limita a evolução. Ela a torna possível.**

> **Arquitetura consistente reduz a complexidade do futuro.**
