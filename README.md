# Fast API

API REST desenvolvida com FastAPI para cadastro de usuarios, autenticacao com
JWT e gerenciamento de tarefas.

## Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy Async
- Alembic
- PostgreSQL
- SQLite
- Poetry
- Pytest
- Ruff
- Docker e Docker Compose

## Funcionalidades

- Cadastro, listagem, atualizacao e remocao de usuarios
- Autenticacao com token JWT
- Refresh de token
- CRUD de tarefas por usuario autenticado
- Filtros e paginacao para listagens
- Migracoes de banco com Alembic
- Testes automatizados com cobertura

## Estrutura do projeto

```text
fast_api/
|-- fast_api/
|   |-- app.py
|   |-- database.py
|   |-- settings.py
|   |-- security.py
|   |-- models/
|   |-- router/
|   `-- schemas/
|-- migrations/
|-- tests/
|-- compose.yaml
|-- Dockerfile
|-- pyproject.toml
`-- README.md
```

## Variaveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///database.db
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Para usar PostgreSQL local ou via Docker, use uma URL no formato:

```env
DATABASE_URL=postgresql+psycopg://app_user:app_password@localhost:5436/app_db
```

## Como rodar localmente

Instale as dependencias:

```bash
poetry install
```

Execute as migracoes:

```bash
poetry run alembic upgrade head
```

Inicie a API:

```bash
poetry run task run
```

A aplicacao ficara disponivel em:

```text
http://localhost:8000
```

A documentacao interativa fica em:

```text
http://localhost:8000/docs
```

## Como rodar com Docker

Suba a aplicacao e o banco PostgreSQL:

```bash
docker compose up --build
```

O container da aplicacao executa as migracoes automaticamente antes de iniciar
o servidor.

Servicos expostos:

- API: `http://localhost:8000`
- PostgreSQL: `localhost:5436`

## Testes e qualidade

Rodar lint:

```bash
poetry run task lint
```

Formatar codigo:

```bash
poetry run task format
```

Rodar testes com cobertura:

```bash
poetry run task test
```

Apos os testes, o relatorio HTML de cobertura e gerado em `htmlcov/`.

## Principais rotas

### Geral

| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/test` | Rota simples de teste |

### Autenticacao

| Metodo | Rota | Descricao |
| --- | --- | --- |
| POST | `/auth/token` | Gera token de acesso |
| POST | `/auth/refresh_token` | Renova o token do usuario autenticado |

### Usuarios

| Metodo | Rota | Descricao |
| --- | --- | --- |
| POST | `/users/` | Cria um usuario |
| GET | `/users/` | Lista usuarios |
| GET | `/users/{phone}` | Busca usuario por telefone |
| PUT | `/users/{phone}` | Atualiza o usuario autenticado |
| DELETE | `/users/{phone}` | Remove o usuario autenticado |

### Tarefas

| Metodo | Rota | Descricao |
| --- | --- | --- |
| POST | `/todos/` | Cria uma tarefa |
| GET | `/todos/` | Lista tarefas do usuario autenticado |
| PATCH | `/todos/{todo_id}` | Atualiza parcialmente uma tarefa |
| DELETE | `/todos/{todo_id}` | Remove uma tarefa |

## Exemplos de uso

Criar usuario:

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "gustavo",
    "phone": "11999999999",
    "email": "gustavo@example.com",
    "password": "123456"
  }'
```

Gerar token:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=gustavo@example.com&password=123456"
```

Criar tarefa autenticada:

```bash
curl -X POST http://localhost:8000/todos/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI",
    "description": "Praticar rotas, autenticacao e testes",
    "state": "todo"
  }'
```

## Estados possiveis de uma tarefa

- `draft`
- `todo`
- `doing`
- `done`
- `trash`

## Migracoes

Criar uma nova migracao:

```bash
poetry run alembic revision --autogenerate -m "descricao_da_migracao"
```

Aplicar migracoes:

```bash
poetry run alembic upgrade head
```

Reverter a ultima migracao:

```bash
poetry run alembic downgrade -1
```
