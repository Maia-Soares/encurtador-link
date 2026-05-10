from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.config import settings
from app.infrastructure.db import SessionLocal
from app.infrastructure.repositories.sqlalchemy_repo import SqlAlchemyLinkRepository
from app.infrastructure.cache.redis_cache import RedisCacheAdapter
from app.infrastructure.cache_client import redis_client
from app.application.use_cases.shorten_url import ShortenUrlUseCase
from app.application.use_cases.redirect_url import RedirectUrlUseCase
from app.application.use_cases.get_stats import GetStatsUseCase
from app.application.use_cases.delete_link import DeleteLinkUseCase
from app.domain.exceptions import InvalidURLError, SlugNotFoundError, LinkExpiredError
from app.interface.schemas import ShortenRequest, LinkResponse
from collections.abc import Iterator

app = FastAPI(title="Encurtador de URL", version="1.0.0")


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repo(db: Session = Depends(get_db)):
    return SqlAlchemyLinkRepository(db)


def get_cache():
    return RedisCacheAdapter(redis_client, ttl_seconds=settings.CACHE_TTL_SECONDS)


def get_shorten_uc(repo=Depends(get_repo)):
    return ShortenUrlUseCase(repo)


def get_redirect_uc(repo=Depends(get_repo), cache=Depends(get_cache)):
    return RedirectUrlUseCase(repo, cache, settings.CACHE_TTL_SECONDS)


def get_stats_uc(repo=Depends(get_repo)):
    return GetStatsUseCase(repo)


def get_delete_uc(repo=Depends(get_repo), cache=Depends(get_cache)):
    return DeleteLinkUseCase(repo, cache)


@app.post(
    "/shorten",
    summary="Encurta uma URL",
    description="Gera um slug único de 8 caracteres e retorna o link curto. Aceita expiração opcional.",
    response_model=LinkResponse,
    tags=["Links"],
)
def shorten(url_data: ShortenRequest, uc: ShortenUrlUseCase = Depends(get_shorten_uc)):
    try:
        link = uc.execute(url_data.url, url_data.expires_at)
        return {"short_url": f"/{link.slug}", "slug": link.slug}
    except InvalidURLError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/{slug}",
    summary="Redireciona para a URL original",
    description="Redireciona o usuário para a URL original associada ao slug fornecido.",
    responses={
        301: {"description": "Redirect permanente"},
        302: {"description": "Redirect temporário (link com expiração)"},
        404: {"description": "Slug não encontrado"},
        410: {"description": "Link expirado"}
    },
    tags=["Redirects"],
)
def redirect(slug: str, uc: RedirectUrlUseCase = Depends(get_redirect_uc)):
    try:
        link = uc.execute(slug)
        status_code = 302 if link.expires_at else 301
        return Response(
            status_code=status_code, headers={"Location": link.original_url}
        )
    except SlugNotFoundError:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    except LinkExpiredError:
        raise HTTPException(status_code=410, detail="Link expirado")


@app.get(
    "/{slug}/stats",
    summary="Estatísticas de um link",
    description="Retorna dados do link: URL original, criação, expiração, total de cliques e último acesso.",
    tags=["Stats"],
)
def stats(slug: str, uc: GetStatsUseCase = Depends(get_stats_uc)):
    try:
        return uc.execute(slug)
    except SlugNotFoundError:
        raise HTTPException(status_code=404, detail="Link não encontrado")


@app.delete(
    "/{slug}",
    summary="Remove um link",
    description="Exclui o link associado ao slug fornecido.",
    tags=["LinksDeleted"],
)
def delete(slug: str, uc: DeleteLinkUseCase = Depends(get_delete_uc)):
    uc.execute(slug)
    return {"message": "Link removido com sucesso"}
