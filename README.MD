# 🔗 Encurtador de URL

API REST para encurtamento de links com FastAPI, cache Redis, PostgreSQL e com foco em Clean Architecture

## Funcionalidades

- ✅ Encurtar URLs com slugs únicos de 8 caracteres (`[A-Za-z0-9]`)
- ✅ Redirecionamento rápido com padrão **Cache-First** (Redis → PostgreSQL)
- ✅ Estatísticas em tempo real (total de cliques, último acesso, expiração)
- ✅ Links com data de expiração configurável
- ✅ Exclusão com invalidação imediata do cache
- ✅ Documentação interativa completa (Swagger/OpenAPI)

## Arquitetura

O projeto segue **Clean Architecture**, garantindo independência de frameworks e testabilidade:

| Camada            | Responsabilidade                                                         |
| ----------------- | ------------------------------------------------------------------------ |
| `domain/`         | Entidades, validações e contratos de repositório (zero imports externos) |
| `application/`    | Casos de uso puros, testáveis sem banco ou servidor HTTP                 |
| `infrastructure/` | Adaptadores: SQLAlchemy, Redis, Alembic                                  |
| `interface/`      | Entrega HTTP (FastAPI), schemas Pydantic e injeção de dependências       |

## Stack Tecnológica

| Camada     | Tecnologia                                        |
| ---------- | ------------------------------------------------- |
| API        | FastAPI + Uvicorn                                 |
| Banco      | PostgreSQL 15 (via Docker)                        |
| Cache      | Redis 7 (via Docker / Upstash)                    |
| Migrations | Alembic (versionado)                              |
| Config     | Pydantic Settings + `.env`                        |
| CI/CD      | GitHub Actions + Ruff + Pytest                    |
| Deploy     | Render (Web Service) + Upstash (Redis Serverless) |

## Como Rodar Localmente

### 1. Pré-requisitos

- Python 3.11+
- Docker + Docker Compose
- Git

### 2. Configuração

```bash
# Clone e acesse o projeto
git clone https://github.com/Maia-Soares/encurtador-link.git
cd encurtador-link

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
crie o arquivo env com suas credenciais locais
```

### 3. Inicie a Infraestrutura

```bash
docker compose up --build
```

⭐Acesse a documentação interativa: http://localhost:8000/docs

## Testes & Qualidade

- **Unitários:** `pytest tests/unit/` (zero dependência externa)
- **Integração:** `pytest tests/integration/` (com Docker real)
- **Cobertura:** ≥80% nos Use Cases (validado no CI)
- **Linting:** Ruff (formatação + análise estática)

Pipeline automático no push para `main`. Merge bloqueado se testes ou linting falharem.

## ⚠️ Nota Técnica: Testando o Endpoint de Redirecionamento no Swagger

O endpoint `GET /{slug}` retorna status `301` ou `302` com cabeçalho `Location`. O **Swagger UI tenta seguir redirecionamentos automaticamente**, o que pode exibir a mensagem `"Failed to fetch"` devido a políticas de segurança do navegador ao acessar domínios externos.

✅ **Isso não é um erro da API.** O redirecionamento funciona perfeitamente. Para validar:

1. Copie o slug retornado pelo `POST /shorten`
2. Cole diretamente na barra de endereços do navegador, ou
3. Use o terminal: `curl -I https://encurtador-link-dl1s.onrender.com/{slug}`

## 🌐 Deploy

API rodando em produção: https://encurtador-link-dl1s.onrender.com

📖 Documentação interativa (Swagger): **https://encurtador-link-dl1s.onrender.com/docs**

⚠️ _Importante: O serviço utiliza plano gratuito (Render), que entra em "cold start" após inatividade. O primeiro acesso pode levar ~10-15s para inicializar. Isso é um comportamento esperado da plataforma e não reflete na performance da arquitetura._

## 📬 Autor

Desenvolvido com foco em boas práticas, testabilidade e escalabilidade.  
 [LinkedIn](https://www.linkedin.com/in/maiisoares/) | 📧 [Email](maiana.a.soares@gmail.com)
