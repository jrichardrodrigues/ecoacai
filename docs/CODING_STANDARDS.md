# ZELURBIS

> **Tecnologia a serviço da sustentabilidade.**

# CODING_STANDARDS.md

**Versão:** 1.0.0  
**Status:** Oficial

---

# Prefácio

Este documento estabelece os padrões oficiais de desenvolvimento da plataforma ZELURBIS.

Seu objetivo é garantir que todo código produzido seja consistente, legível, reutilizável e preparado para evoluir.

> **Todo código deve ser escrito para quem irá mantê-lo amanhã.**

---

# 1. Introdução

Código é um ativo da organização.

Cada linha escrita deve refletir os valores da ZELURBIS: zelo, simplicidade, qualidade, transparência e melhoria contínua.

---

# 2. Filosofia de Desenvolvimento

Toda implementação deve priorizar:

- simplicidade;
- clareza;
- baixo acoplamento;
- alta coesão;
- reutilização;
- documentação contínua.

Evite soluções complexas quando uma solução simples resolver o mesmo problema.

---

# 3. Princípios da Engenharia ZELURBIS

1. Clareza acima da complexidade.
2. Duplicação é um defeito de arquitetura.
3. Cada responsabilidade possui um único lugar.
4. Componentes reutilizáveis antes de copiar código.
5. Funções pequenas.
6. Classes com responsabilidade única.
7. Refatoração contínua.
8. Documentação faz parte do desenvolvimento.

---

# 4. Organização do Projeto

A organização do código deverá seguir a arquitetura oficial:

- models
- repositories
- services
- controllers
- views
- components
- utils

Cada módulo deve possuir responsabilidade claramente definida.

---

# 5. Convenções Gerais

## Arquivos

Utilizar `snake_case`.

Exemplo:

usuario_service.py

## Classes

Utilizar `PascalCase`.

Exemplo:

UsuarioService

## Métodos

Utilizar `snake_case`.

Exemplo:

buscar_usuario()

## Constantes

Utilizar `UPPER_CASE`.

Exemplo:

APP_NAME

---

# 6. Models

Models representam entidades.

Não devem:

- acessar banco;
- criar interface;
- conter regras de negócio complexas.

---

# 7. Repositories

Responsáveis exclusivamente pela persistência.

Não devem:

- validar dados;
- criar componentes;
- exibir mensagens.

---

# 8. Services

Contêm regras de negócio.

Devem concentrar:

- validações;
- integrações;
- normalizações;
- cálculos.

---

# 9. Controllers

Ligam Views aos Services.

Não devem acessar diretamente o banco.

---

# 10. Views

Responsáveis apenas pela interface.

Não devem conter regras de negócio.

---

# 11. Components

Todo elemento reutilizável deve ser transformado em componente.

Exemplos:

- botões;
- campos;
- diálogos;
- layouts.

---

# 12. Tratamento de Erros

Nunca utilizar:

except Exception:
    pass

Todo erro deve ser tratado, registrado e retornar mensagem adequada ao usuário.

---

# 13. Logging

Registrar:

- erros;
- operações críticas;
- integrações externas.

Jamais registrar senhas, tokens ou dados sensíveis.

---

# 14. Testes

Todo desenvolvimento deve possuir testes compatíveis.

Prioridades:

- Services
- Repositories
- Controllers
- Components

---

# 15. Documentação

Toda classe pública deve possuir documentação.

Métodos complexos devem conter comentários explicando decisões arquiteturais e não o óbvio.

---

# 16. Git e Versionamento

Commits devem ser pequenos e objetivos.

Exemplos:

- feat:
- fix:
- refactor:
- docs:
- test:

---

# 17. Checklist de Desenvolvimento

Antes de concluir uma funcionalidade verificar:

- arquitetura respeitada;
- código limpo;
- testes executados;
- documentação atualizada;
- imports organizados;
- ausência de código morto.

---

# 18. Antipadrões

Evitar:

- duplicação;
- funções gigantes;
- classes com múltiplas responsabilidades;
- imports circulares;
- código comentado;
- números mágicos;
- acoplamento entre camadas.

---

# 19. Considerações Finais

O desenvolvimento da plataforma deve preservar os princípios estabelecidos neste documento.

A qualidade do software depende da disciplina aplicada diariamente pela equipe.

> **Toda solução começa com o zelo.**

> **Toda arquitetura deve facilitar a evolução.**

> **Todo código deve ser escrito para quem irá mantê-lo amanhã.**
