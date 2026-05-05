from app.domain.repositories import LinkRepositoryInterface
from app.domain.cache import CacheInterface

class DeleteLinkUseCase:
    def __init__(self, repo: LinkRepositoryInterface, cache: CacheInterface):
        self.repo = repo
        self.cache = cache

    def execute(self, slug: str) -> None:
        self.repo.delete(slug)
        self.cache.delete(slug)