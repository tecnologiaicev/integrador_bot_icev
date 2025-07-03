# Iceverino 1.0
# Documentação da API de Integração

Este repositório contém o código-fonte de uma API de integração desenvolvida em Flask, projetada para se comunicar com sistemas externos e fornecer dados específicos, como informações de usuários e disciplinas, baseadas em CPF.

## Visão Geral do Projeto

A API atua como um intermediário, recebendo requisições, autenticando-as via token e consultando dados em um sistema externo (provavelmente um Moodle ou sistema similar, inferido pela configuração do banco de dados). Os dados são então formatados e retornados como respostas JSON.

## Estrutura do Projeto

- `api.py`: Define os endpoints da API para consulta de dados de usuários (`/singup`) e disciplinas (`/disciplina`).
- `auth.py`: Contém a lógica de autenticação baseada em token (`Bearer Token`) para proteger os endpoints da API.
- `config.py`: Gerencia as configurações da aplicação, incluindo variáveis de ambiente para acesso ao banco de dados e credenciais da API externa.
- `extensions.py`: Inicializa extensões do Flask, como o SQLAlchemy para interação com o banco de dados.
- `wsgi.py`: Ponto de entrada da aplicação, responsável por criar e executar a instância do aplicativo Flask.

## Configuração do Ambiente

Para configurar e executar este projeto localmente, siga os passos abaixo:

### Pré-requisitos

Certifique-se de ter os seguintes itens instalados:

- Python 3.x
- pip (gerenciador de pacotes do Python)

### Instalação das Dependências

Crie um ambiente virtual (recomendado) e instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

**Nota:** Você precisará criar um arquivo `requirements.txt` com as dependências do projeto. Com base nos arquivos fornecidos, as dependências mínimas seriam `Flask`, `Flask-SQLAlchemy`, `PyMySQL`, `python-dotenv` e `requests`.

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
USER_DB=seu_usuario_do_banco
PASSWORD_DB=sua_senha_do_banco
IP_BANCO=seu_ip_do_banco
API_TOKEN=seu_token_secreto_para_autenticacao_da_api
BASE_URL=url_base_da_api_externa
USER=usuario_da_api_externa
SENHA=senha_da_api_externa
```

Certifique-se de preencher essas variáveis com as informações corretas do seu ambiente e das credenciais da API externa.

## Executando a Aplicação

Para iniciar a API, execute o arquivo `wsgi.py`:

```bash
python wsgi.py
```

A API estará disponível em `http://127.0.0.1:5000` (ou na porta configurada pelo Flask).

## Endpoints da API

### 1. Consulta de Dados de Usuário (Singup)

- **URL:** `/singup`
- **Método:** `POST`
- **Autenticação:** `Bearer Token` (o token deve ser o valor de `API_TOKEN` no `.env`)
- **Corpo da Requisição (JSON):**

  ```json
  {
    "cpf": "123.456.789-00"
  }
  ```

- **Resposta (JSON):** Retorna os dados do usuário consultado na API externa.

### 2. Consulta de Dados de Disciplina

- **URL:** `/disciplina`
- **Método:** `POST`
- **Autenticação:** `Bearer Token` (o token deve ser o valor de `API_TOKEN` no `.env`)
- **Corpo da Requisição (JSON):**

  ```json
  {
    "cpf": "123.456.789-00"
  }
  ```

- **Resposta (JSON):** Retorna os dados das disciplinas associadas ao CPF consultado na API externa.

## Como Verificar

Para verificar o funcionamento da API, você pode usar ferramentas como `curl` ou `Postman`.

### Exemplo com `curl`

Substitua `SEU_API_TOKEN` pelo valor configurado no seu arquivo `.env`.

#### Consulta de Dados de Usuário:

```bash
curl -X POST \\
  http://127.0.0.1:5000/singup \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer SEU_API_TOKEN" \\
  -d '{"cpf": "123.456.789-00"}'
```

#### Consulta de Dados de Disciplina:

```bash
curl -X POST \\
  http://127.0.0.1:5000/disciplina \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer SEU_API_TOKEN" \\
  -d '{"cpf": "123.456.789-00"}'
```

## Considerações para a Equipe de Verificação

- **Autenticação:** Certifiquem-se de que o `Bearer Token` está sendo enviado corretamente no cabeçalho `Authorization` para todas as requisições. A ausência ou um token inválido resultará em erros `401 Unauthorized` ou `403 Forbidden`.
- **Variáveis de Ambiente:** Verifiquem se todas as variáveis no arquivo `.env` estão configuradas corretamente, especialmente as credenciais para o banco de dados e para a API externa. Erros de conexão ou autenticação podem indicar problemas aqui.
- **Conectividade com API Externa:** A API depende de uma API externa para buscar os dados. Certifiquem-se de que o servidor onde a API está rodando tem conectividade com a `BASE_URL` configurada e que as credenciais (`USER` e `SENHA`) estão corretas.
- **Formato do CPF:** O CPF é um parâmetro crucial. Testem com CPFs válidos e inválidos para observar o comportamento da API e as mensagens de erro retornadas.
- **Tratamento de Erros:** Observem as mensagens de erro retornadas pela API em diferentes cenários (e.g., CPF não encontrado, erro na API externa, erro interno do servidor). A API foi projetada para retornar mensagens detalhadas em caso de falha na requisição externa.
- **Logs:** Verifiquem os logs da aplicação (saída do console ou logs configurados) para identificar quaisquer erros internos ou mensagens de depuração que possam auxiliar na análise.

---

**Data:** 3 de julho de 2025


