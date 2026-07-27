# ZELURBIS

> **Tecnologia a serviço da sustentabilidade.**

# ARCHITECTURE.md

**Versão:** 2.0.0  
**Status:** Oficial

---

# 1. Introdução

A arquitetura da **ZELURBIS** foi concebida para sustentar o desenvolvimento de uma plataforma tecnológica voltada à gestão urbana sustentável.

Mais do que organizar código, ela estabelece princípios que garantem evolução contínua, reutilização de componentes, baixo acoplamento e facilidade de manutenção.

A primeira solução desenvolvida sobre esta arquitetura é o **EcoAçaí**, mas toda a estrutura foi planejada para acomodar novas soluções sem comprometer sua consistência.

---

# 2. Filosofia da Arquitetura

A arquitetura da ZELURBIS é guiada por um princípio simples:

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
      Tecnologia a serviço da sustentabilidade.

                        │
        ┌───────────────┼───────────────┐
        │               │               │
     EcoAçaí      Futuras Soluções      APIs
                        │
──────────────────────────────────────────────────

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

A plataforma adota arquitetura em camadas, separando responsabilidades entre Interface, Controle, Regras de Negócio e Persistência.

Fluxo principal:

```text
Views
  ↓
Controllers
  ↓
Services
  ↓
Repositories
  ↓
Banco de Dados
```

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

# 6. Estrutura de Diretórios

A estrutura física do projeto deve refletir a arquitetura lógica da plataforma.

Principais diretórios:

- assets/
- config/
- models/
- repositories/
- services/
- controllers/
- views/
- components/
- utils/
- data/
- docs/

A organização poderá evoluir sem alterar os princípios arquiteturais definidos neste documento.

---

# 7. Componentização

Todos os elementos reutilizáveis devem permanecer isolados em componentes independentes.

Exemplos:

- campos;
- botões;
- diálogos;
- layouts;
- cartões;
- menus.

---

# 8. Persistência

A camada de persistência deve permanecer independente da tecnologia utilizada.

Atualmente a plataforma utiliza SQLite, porém sua arquitetura permite evolução futura para outros mecanismos de armazenamento sem impacto significativo nas demais camadas.

---

# 9. Segurança

As configurações sensíveis devem permanecer fora do código-fonte.

Devem ser armazenadas em `.env` e nunca versionadas.

---

# 10. Escalabilidade

A arquitetura foi concebida para permitir a inclusão de novas soluções da plataforma ZELURBIS preservando padrões de engenharia, reutilização e manutenção.

---

# 11. Convenções

- Arquivos em snake_case;
- Classes em PascalCase;
- Constantes em UPPER_CASE;
- Métodos internos prefixados por "_".

---

# 12. Decisões Arquiteturais

Toda decisão arquitetural deverá responder positivamente às seguintes perguntas:

1. Simplifica a plataforma?
2. Reduz acoplamento?
3. Facilita manutenção?
4. Permite evolução?
5. Mantém consistência com a identidade da ZELURBIS?

---

# 13. Considerações Finais

A arquitetura da ZELURBIS não descreve apenas como o software está organizado.

Ela registra os princípios que orientam sua evolução.

Assim como o propósito institucional é guiado pelo zelo, a engenharia da plataforma é guiada pela simplicidade, pela clareza e pela capacidade de evoluir continuamente.

> **Toda solução começa com o zelo.**  
> **Toda arquitetura deve facilitar a evolução.**
