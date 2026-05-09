from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[dict[str, Any]]: ...
    @abstractmethod
    def set(self, key: str, value: dict[str, Any], ttl_seconds: int = 3600) -> None: ...
    @abstractmethod
    def delete(self, key: str) -> None: ...
