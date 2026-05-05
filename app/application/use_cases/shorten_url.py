from datetime import datetime
from app.domain.entities import Link
from app.domain.repositories import LinkRepositoryInterface
from app.domain.validators import validate_url, generate_slug

class ShortenUrlUseCase:
    def __init__(self, repo: LinkRepositoryInterface):
        self.repo = repo

    def execute(self, url: str, expires_at: datetime | None = None) -> Link:
        validate_url(url)
        slug = generate_slug()
        link = Link(
            slug=slug,
            original_url=url,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        return self.repo.save(link)