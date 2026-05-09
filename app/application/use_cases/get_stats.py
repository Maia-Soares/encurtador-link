from app.domain.repositories import LinkRepositoryInterface
from app.domain.exceptions import SlugNotFoundError


class GetStatsUseCase:
    def __init__(self, repo: LinkRepositoryInterface):
        self.repo = repo

    def execute(self, slug: str) -> dict:
        link = self.repo.get_by_slug(slug)
        if not link:
            raise SlugNotFoundError(f"Slug '{slug}' não encontrado")
        return {
            "original_url": link.original_url,
            "created_at": link.created_at.isoformat() if link.created_at else None,
            "expires_at": link.expires_at.isoformat() if link.expires_at else None,
            "click_count": link.click_count,
            "last_accessed": link.last_accessed.isoformat()
            if link.last_accessed
            else None,
            "is_expired": link.is_expired,
        }
