from datetime import datetime
from app.domain.entities import Link
from app.domain.repositories import LinkRepositoryInterface
from app.domain.cache import CacheInterface
from app.domain.exceptions import SlugNotFoundError, LinkExpiredError

class RedirectUrlUseCase:
    def __init__(self, repo: LinkRepositoryInterface, cache: CacheInterface, ttl_seconds: int = 3600):
        self.repo = repo
        self.cache = cache
        self.ttl_seconds = ttl_seconds

    def execute(self, slug: str) -> Link:
        cached = self.cache.get(slug)
        if cached:
            link = Link(**cached)
        else:
            link = self.repo.get_by_slug(slug)
            if not link:
                raise SlugNotFoundError(f"Slug '{slug}' não encontrado")
            self.cache.set(slug, link.__dict__, self.ttl_seconds)

        if link.is_expired:
            raise LinkExpiredError(f"Link '{slug}' está expirado")

        link.click_count += 1
        link.last_accessed = datetime.utcnow()
        
        self.repo.save(link)
        self.cache.set(slug, link.__dict__, self.ttl_seconds)

        return link