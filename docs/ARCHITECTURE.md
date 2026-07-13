# Arquitetura do Sistema

## 1. Visão geral

O sistema **Controle de Recolhimento de Caroço do Açaí** é uma aplicação desktop desenvolvida em Python com Flet.

A arquitetura adotada separa a aplicação em camadas, reduzindo o acoplamento entre interface, regras de negócio e persistência.

Fluxo principal:

```text
View
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
database.json
```

Os componentes visuais reutilizáveis ficam isolados na camada `components`.

---

## 2. Objetivos da arquitetura

A estrutura do projeto foi definida para:

- separar responsabilidades;
- facilitar manutenção;
- evitar duplicação de código;
- permitir testes isolados;
- facilitar a troca futura do banco JSON por SQLite, PostgreSQL ou outro banco;
- reutilizar campos, botões, diálogos e elementos de layout;
- manter as telas pequenas e legíveis.

---

## 3. Estrutura de diretórios

```text
controle_recolhimento_acai/
│
├── main.py
│
├── assets/
│   └── imagens e recursos visuais
│
├── config/
│   ├── __init__.py
│   ├── constants.py
│   └── settings.py
│
├── models/
│   ├── __init__.py
│   ├── usuario.py
│   └── solicitacao.py
│
├── repositories/
│   ├── __init__.py
│   └── json_repository.py
│
├── services/
│   ├── __init__.py
│   ├── base_service.py
│   ├── cpf_service.py
│   ├── email_service.py
│   ├── usuario_service.py
│   ├── solicitacao_service.py
│   ├── validation_service.py
│   └── google_sheets_service.py
│
├── controllers/
│   ├── __init__.py
│   ├── navigation_controller.py
│   ├── usuario_controller.py
│   └── solicitacao_controller.py
│
├── views/
│   ├── __init__.py
│   ├── home_view.py
│   ├── cadastro_view.py
│   ├── coleta_view.py
│   ├── painel_view.py
│   └── dashboard_view.py
│
├── components/
│   ├── __init__.py
│   │
│   ├── layout/
│   │   ├── __init__.py
│   │   ├── app_bar.py
│   │   ├── menu.py
│   │   └── cards.py
│   │
│   ├── fields/
│   │   ├── __init__.py
│   │   ├── base_field.py
│   │   ├── base_validated_field.py
│   │   ├── cpf_field.py
│   │   ├── email_field.py
│   │   ├── phone_field.py
│   │   ├── name_field.py
│   │   ├── address_field.py
│   │   ├── text_field.py
│   │   └── dropdown_field.py
│   │
│   ├── buttons/
│   │   ├── __init__.py
│   │   ├── primary_button.py
│   │   ├── secondary_button.py
│   │   └── danger_button.py
│   │
│   └── dialogs/
│       ├── __init__.py
│       ├── confirm_dialog.py
│       └── message_dialog.py
│
├── utils/
│   ├── __init__.py
│   ├── formatters.py
│   ├── validators.py
│   ├── messages.py
│   └── helpers.py
│
├── data/
│   └── database.json
│
├── docs/
│   └── ARCHITECTURE.md
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

Alguns arquivos da estrutura representam funcionalidades planejadas e podem ainda não estar implementados.

---

## 4. Responsabilidade das camadas

### 4.1 `main.py`

É o ponto de entrada da aplicação.

Responsabilidades:

- importar a função principal da interface;
- iniciar o Flet;
- não conter regras de negócio;
- não acessar diretamente o banco de dados.

Exemplo:

```python
import flet as ft

from views.home_view import construir_interface


if __name__ == "__main__":
    ft.run(main=construir_interface)
```

---

### 4.2 `config`

Contém configurações e constantes globais.

#### `constants.py`

Usado para informações fixas compartilhadas, como:

- nome da aplicação;
- versão;
- setores;
- status de solicitação;
- tipos de volume.

Exemplo:

```python
APP_NAME = "Controle de Recolhimento de Caroço do Açaí"

SETORES = [
    "Guamá",
    "Terra Firme",
    "Jurunas",
]
```

#### `settings.py`

Usado para configurações que podem variar entre ambientes:

- caminho do banco;
- nome da planilha;
- credenciais;
- configurações de e-mail;
- configurações da API do WhatsApp.

Dados sensíveis não devem ser escritos diretamente nesse arquivo. Devem vir do `.env`.

---

### 4.3 `models`

Representa as entidades da aplicação.

Os modelos não devem conter código de interface ou acesso direto ao banco.

#### `Usuario`

Representa um estabelecimento ou responsável cadastrado.

Campos previstos:

```text
id
nome
cpf
email
celular
celular_confirmado
endereco
bairro
setor
```

#### `Solicitacao`

Representa uma solicitação de coleta.

Campos previstos:

```text
id
usuario_id
tipo
quantidade
status
data_criacao
data_atualizacao
```

Os modelos podem possuir métodos como:

```python
to_dict()
from_dict()
```

---

### 4.4 `repositories`

Responsável exclusivamente pela persistência.

O repositório:

- lê o arquivo JSON;
- grava o arquivo JSON;
- garante a criação da estrutura inicial;
- não valida CPF;
- não valida e-mail;
- não conhece componentes Flet;
- não exibe mensagens.

Exemplo de fluxo:

```text
UsuarioService
    ↓
JsonRepository
    ↓
database.json
```

No futuro, o `JsonRepository` poderá ser substituído por outro repositório sem exigir grandes alterações nas telas.

---

### 4.5 `services`

Contém regras de negócio e integrações externas.

#### `UsuarioService`

Responsável por:

- cadastrar;
- listar;
- buscar;
- atualizar;
- excluir;
- verificar duplicidade de CPF;
- verificar duplicidade de e-mail;
- verificar duplicidade de celular;
- gerar o próximo ID.

#### `CpfService`

Responsável por:

- remover caracteres não numéricos;
- formatar o CPF;
- validar os dígitos verificadores.

#### `EmailService`

Responsável por:

- normalizar o e-mail;
- validar o formato;
- detectar erros comuns de domínio;
- sugerir correções.

#### `UsuarioValidationService`

Centraliza a validação completa do usuário.

Ordem atual:

```text
campos obrigatórios
→ CPF
→ e-mail
→ celular
```

Ele também retorna os dados normalizados.

#### `SolicitacaoService`

Será responsável por:

- criar solicitações;
- listar solicitações;
- alterar status;
- cancelar;
- evitar solicitações duplicadas;
- concluir coletas.

#### `GoogleSheetsService`

Será responsável por:

- autenticar;
- acessar a planilha;
- exportar solicitações;
- tratar erros da API.

---

### 4.6 `controllers`

Fazem a ligação entre a interface e os serviços.

O controller:

- recebe dados da View;
- chama os serviços;
- monta modelos;
- devolve resultado e mensagem;
- não deve criar controles Flet;
- não deve acessar diretamente o JSON.

Exemplo:

```text
CadastroView
    ↓
UsuarioController
    ↓
UsuarioValidationService
    ↓
UsuarioService
```

#### `NavigationController`

Responsável por trocar o conteúdo exibido na área central da aplicação.

#### `UsuarioController`

Responsável pelas ações relacionadas ao usuário:

- cadastrar;
- listar;
- buscar;
- atualizar;
- excluir.

#### `SolicitacaoController`

Será responsável pelas operações de solicitação de coleta.

---

### 4.7 `views`

Contêm as telas da aplicação.

Uma View deve:

- montar o layout;
- receber interações;
- chamar controllers;
- mostrar mensagens;
- manter o mínimo possível de regra de negócio.

Uma View não deve:

- validar diretamente o algoritmo do CPF;
- acessar o JSON;
- conectar ao Google Sheets;
- enviar mensagens de WhatsApp;
- conter regras de duplicidade.

#### `HomeView`

Monta:

- AppBar;
- menu lateral;
- área central;
- controlador de navegação.

#### `CadastroView`

Responsável pelo formulário de estabelecimentos.

#### `ColetaView`

Responsável pela criação de solicitações de coleta.

#### `PainelView`

Responsável por listar e gerenciar solicitações.

#### `DashboardView`

Responsável por indicadores, totais e gráficos.

---

### 4.8 `components`

Contém componentes visuais reutilizáveis.

## Layout

Elementos estruturais:

- AppBar;
- NavigationRail;
- cards;
- divisores;
- cabeçalhos.

## Fields

Campos reutilizáveis.

### `BaseField`

Oferece comportamentos básicos:

```python
campo.value
campo.limpar()
campo.habilitar()
campo.desabilitar()
campo.mostrar_erro()
campo.mostrar_sucesso()
```

### `BaseValidatedField`

Adiciona:

- validação automática;
- evento `on_change`;
- evento `on_blur`;
- mensagem própria abaixo do campo;
- atualização visual compatível com Flet 0.85.3.

Estrutura visual:

```text
TextField
Mensagem de validação
```

### `CpfField`

Responsável por:

- aplicar máscara;
- validar;
- verificar duplicidade;
- exibir mensagem.

### Campos planejados

- `EmailField`;
- `PhoneField`;
- `NameField`;
- `AddressField`;
- `DropdownField`.

---

### 4.9 `utils`

Contém funções genéricas que não pertencem a uma entidade específica.

#### `formatters.py`

Exemplos:

- remover caracteres;
- manter somente dígitos;
- limpar texto;
- capitalizar.

#### `validators.py`

Validações simples e genéricas:

- campo obrigatório;
- número inteiro positivo;
- outras validações sem regra de negócio específica.

#### `messages.py`

Centraliza mensagens visuais, como `SnackBar`.

#### `helpers.py`

Funções auxiliares gerais.

---

## 5. Fluxo de cadastro

```text
Usuário preenche o formulário
        ↓
Campos reutilizáveis validam em tempo real
        ↓
CadastroView reúne os valores
        ↓
UsuarioController recebe os dados
        ↓
UsuarioValidationService valida e normaliza
        ↓
UsuarioService verifica duplicidade e cadastra
        ↓
JsonRepository grava no database.json
        ↓
Controller devolve sucesso ou erro
        ↓
CadastroView exibe a mensagem
```

---

## 6. Regras de dependência

Para evitar acoplamento circular, as dependências devem seguir esta direção:

```text
Views
  ↓
Controllers
  ↓
Services
  ↓
Repositories
  ↓
Models
```

Os componentes podem usar serviços específicos para validação visual, mas não devem acessar diretamente o repositório.

### Permitido

```python
CadastroView -> UsuarioController
UsuarioController -> UsuarioService
UsuarioService -> JsonRepository
CpfField -> CpfService
```

### Evitar

```python
CadastroView -> JsonRepository
JsonRepository -> CadastroView
Model -> Flet
Service -> SnackBar
```

---

## 7. Convenções de código

### Arquivos

Usar `snake_case`:

```text
usuario_service.py
cadastro_view.py
cpf_field.py
```

### Classes

Usar `PascalCase`:

```python
UsuarioService
CadastroView
CpfField
```

### Funções e métodos

Usar `snake_case`:

```python
cadastrar_usuario()
validar_cpf()
mostrar_mensagem()
```

### Constantes

Usar letras maiúsculas:

```python
APP_NAME
SETORES
STATUS_SOLICITACAO
```

### Métodos internos

Prefixar com `_`:

```python
_validar_cpf()
_normalizar_dados()
_criar_banco()
```

---

## 8. Tratamento de erros

Erros técnicos devem ser tratados na camada responsável.

Exemplos:

- erro de leitura do JSON: repository;
- erro de autenticação no Google: service;
- CPF inválido: validation service;
- erro visual: View ou utilitário de mensagens.

Evitar:

```python
except Exception:
    pass
```

Quando necessário, registrar o erro e retornar uma mensagem amigável.

---

## 9. Configurações sensíveis

Nunca versionar:

- senha de e-mail;
- token do WhatsApp;
- credenciais do Google;
- chaves de API;
- arquivo `.env`;
- arquivos de credenciais privadas.

Exemplo de `.env.example`:

```env
GOOGLE_CREDENTIALS_FILE=
GOOGLE_SPREADSHEET_NAME=
EMAIL_SENDER=
EMAIL_APP_PASSWORD=
WHATSAPP_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
```

---

## 10. Estratégia de testes

Cada sprint deve terminar com um teste.

Tipos atuais:

- scripts temporários executados pela raiz;
- teste visual dos componentes;
- teste de serviços;
- teste de persistência.

No futuro, os testes temporários deverão ser substituídos por testes automatizados com `pytest`.

Estrutura futura:

```text
tests/
├── test_cpf_service.py
├── test_email_service.py
├── test_usuario_service.py
├── test_validation_service.py
└── test_json_repository.py
```

---

## 11. Estratégia de limpeza

A limpeza deverá ocorrer após a migração completa para os novos componentes.

Serão revisados:

- arquivos `_legacy`;
- módulos duplicados;
- pastas e arquivos vazios;
- imports não utilizados;
- testes temporários;
- código comentado;
- funções não chamadas;
- dependências não utilizadas;
- conflitos entre arquivo e diretório com o mesmo nome.

Exemplos de conflitos que devem ser eliminados:

```text
components/fields.py
components/fields/
```

```text
components/dialogs.py
components/dialogs/
```

Ao final da limpeza, deve existir apenas a estrutura nova.

---

## 12. Decisões atuais

- Flet usado na versão 0.85.3.
- Persistência inicial em JSON.
- Navegação por `NavigationRail`.
- Validação visual realizada por mensagem própria abaixo do campo.
- CPF, e-mail e celular devem possuir validação em tempo real.
- O celular será preparado para confirmação por WhatsApp.
- As credenciais externas serão carregadas via `.env`.
- A interface não acessará diretamente o banco.
- A limpeza do código legado ocorrerá após a migração dos componentes.

---

## 13. Próximas implementações

Ordem recomendada:

1. `EmailField`;
2. `PhoneField`;
3. `NameField`;
4. `AddressField`;
5. `DropdownField`;
6. refatoração da `CadastroView`;
7. limpeza dos arquivos legados;
8. serviço e tela de solicitações;
9. painel;
10. dashboard;
11. Google Sheets;
12. confirmação via WhatsApp;
13. testes automatizados;
14. documentação final e empacotamento.
