## Projeto 1 — Encurtador de URL

### Contexto

Construir uma API REST para encurtamento de URLs com painel de estatísticas.
O projeto simula um produto real e exige que cada decisão técnica seja justificada.

### Stack obrigatória

| Camada          | Tecnologia              |
| --------------- | ----------------------- |
| API             | FastAPI                 |
| Banco de dados  | PostgreSQL              |
| Cache           | Redis                   |
| Containerização | Docker + Docker Compose |
| Arquitetura     | Clean Architecture      |
| Pipeline        | GitHub Actions          |

### Requisitos Funcionais

**RF01 — Encurtar URL**
O usuário envia uma URL longa via `POST /shorten`. A API valida se é uma URL válida, gera um slug único de 8 caracteres e retorna a URL encurtada. O usuário pode opcionalmente informar uma data de expiração.

**RF02 — Redirecionar**
Ao acessar `GET /{slug}`, a API busca a URL original **prioritariamente no cache Redis** e, somente em caso de cache miss, consulta o PostgreSQL. Faz redirect `301`. Se o slug não existir, retorna `404`. Se o link estiver expirado, retorna `410 Gone`.

**RF03 — Contar acessos**
A cada redirect bem-sucedido, o sistema incrementa o contador de cliques do link.

**RF04 — Estatísticas do link**
`GET /{slug}/stats` retorna os dados do link: URL original, data de criação, expiração, total de cliques e data do último acesso.

**RF05 — Deletar link**
`DELETE /{slug}` remove o link. Acessos posteriores retornam `404`.

### Requisitos Não Funcionais

**RNF01 — Clean Architecture obrigatória**
O código deve estar separado em camadas: `domain`, `application`, `infrastructure` e `interface`. Nenhuma regra de negócio pode depender de FastAPI, SQLAlchemy ou qualquer framework. Os use cases devem ser testáveis sem banco de dados.

**RNF02 — Banco via Docker**
O PostgreSQL deve rodar exclusivamente via Docker Compose. É proibido usar SQLite ou banco em memória na aplicação principal.

**RNF03 — Migrations versionadas**
Todo schema do banco deve ser criado e versionado via Alembic. É proibido usar `Base.metadata.create_all()` fora de testes.

**RNF04 — Testes automatizados**
Cobertura mínima de 80% nos use cases. Os testes de unidade não podem subir banco nem servidor HTTP. Os testes de integração usam banco real via Docker.

**RNF05 — GitHub Actions no push**
Todo push para `main` deve disparar o workflow de CI: instalar dependências, rodar linting (`ruff`) e executar os testes. O merge só pode acontecer com o pipeline verde.

**RNF06 — Variáveis de ambiente**
Nenhuma credencial, URL de banco ou segredo pode estar hardcoded. Tudo via `.env` com `pydantic-settings`.

**RNF07 — Documentação automática**
A API deve ter Swagger funcional em `/docs` com todos os endpoints, schemas e exemplos de request/response preenchidos.

**RNF08 — Cache Redis obrigatório**
O Redis deve rodar via Docker Compose. A consulta de slug no endpoint `GET /{slug}` é **obrigatoriamente** mediada por cache Redis com TTL configurável via variável de ambiente (`CACHE_TTL_SECONDS`). É proibido consultar o banco diretamente sem passar pelo cache. Ao deletar um link (`DELETE /{slug}`), a entrada correspondente deve ser invalidada imediatamente no Redis.

### Restrições técnicas

- O slug deve ter exatamente 8 caracteres, usando apenas letras maiúsculas, letras minúsculas e dígitos (0–9) — nenhum outro caractere é permitido (sem hífen, underscore, símbolo ou espaço). O alfabeto resultante tem exatamente 62 símbolos possíveis por posição
- O redirect deve ser `301` para URLs permanentes e `302` para links com expiração
- Proibido usar ORM na camada de domain — repositórios só na infra
- Proibido consultar o PostgreSQL no endpoint de redirect sem antes verificar o Redis

---
