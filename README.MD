# 🔗 Encurtador de URL

API REST para encurtamento de links com cache FastAPI, Redis, PostgreSQL e com foco em Clean Architecture

## 🚀 Como rodar

1. `docker compose up -d`
2. `python -m venv venv && source venv/bin/activate` (ou `venv\Scripts\activate` no Windows)
3. `pip install -r requirements.txt`
4. `alembic upgrade head`
5. `uvicorn app.interface.main:app --reload`

Acesse:

- API: http://localhost:8000/docs
- Testes: `pytest tests/ --cov=app.application`

## 📐 Arquitetura

- `domain/`: Regras puras (zero frameworks)
- `application/`: Casos de uso testáveis
- `infrastructure/`: Adaptadores (SQLAlchemy, Redis)
- `interface/`: FastAPI + Swagger
