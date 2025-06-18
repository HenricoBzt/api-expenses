# User Management & Financial Control API

API RESTful desenvolvida em **FastAPI** para gerenciamento de usuários, categorias, despesas, rendas mensais e geração de insights financeiros. Ideal para controle financeiro pessoal ou familiar.

---

## 🚀 Funcionalidades

- **Autenticação JWT** (login, refresh)
- **Usuários**: cadastro, listagem, atualização e remoção
- **Categorias**: CRUD e busca por nome
- **Despesas**: CRUD, integração com saldo mensal, status (pago, pendente, atrasado)
- **Renda Mensal**: CRUD, 1 por mês/usuário, update automático do saldo
- **Insights**: resumo mensal, gastos por categoria, percentual gasto, saldo disponível
- **Validações**: permissões, saldo, unicidade de renda mensal por mês/usuário
- **Separação de camadas**: routes, services, crud, schemas, models

---

## 🛠️ Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic](https://alembic.sqlalchemy.org/) (migrações)
- [Docker](https://www.docker.com/) & Docker Compose
- [Pytest](https://docs.pytest.org/) (testes)
- [Pydantic v2](https://docs.pydantic.dev/)

---

## 📦 Instalação

### 1. Clone o repositório

```sh
git clone https://github.com/henricobzt/User_managment_api.git
cd User_managment_api
```

### 2. Crie um ambiente virtual

```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```
### 3. Instale as dependências

```sh
pip install -r requirements.txt
```

### 4. Suba o docker compose

```sh
docker-compose up --build
```

### 5. Acesse a API
A API estará disponível em `http://localhost:8000`. Você pode acessar a documentação interativa em `http://localhost:8000/docs`.


## 📚 Endpoints Principais


| Método | Caminho                                 | Descrição                                 |
|--------|-----------------------------------------|-------------------------------------------|
| POST   | `/api/auth/token`                       | Login e geração de token JWT              |
| GET    | `/api/users/`                           | Lista todos os usuários                   |
| POST   | `/api/users/`                           | Cria um novo usuário                      |
| GET    | `/api/category/`                        | Lista todas as categorias                 |
| POST   | `/api/category/`                        | Cria uma nova categoria                   |
| GET    | `/api/expenses/`                        | Lista todas as despesas                   |
| POST   | `/api/expenses/`                        | Cria uma nova despesa                     |
| PATCH  | `/api/expenses/{id}`                    | Atualiza uma despesa                      |
| DELETE | `/api/expenses/{id}`                    | Remove uma despesa                        |
| GET    | `/api/monthly_income/`                  | Lista rendas mensais                      |
| POST   | `/api/monthly_income/`                  | Cria uma renda mensal                     |
| PATCH  | `/api/monthly_income/{id}`              | Atualiza uma renda mensal                 |
| DELETE | `/api/monthly_income/{id}`              | Remove uma renda mensal                   |
| GET    | `/api/insights/monthly`                 | Retorna resumo financeiro do mês          |
| GET    | `/api/insights/expenses_by_category`    | Retorna gastos agrupados por categoria    |


## 🧪 Testes
Em desenvolvimento. Em breve serão adicionados testes unitários e de integração.

