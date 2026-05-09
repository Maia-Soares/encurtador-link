from abc import ABC, abstractmethod
from app.domain.entities import Link
from typing import Optional

class LinkRepositoryInterface(ABC):
    @abstractmethod
    def save(self, link: Link) -> Link: ...
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Link]: ...
    @abstractmethod
    def delete(self, slug: str) -> None: ...