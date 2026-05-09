from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Link:
    id: Optional[int] = None
    slug: str = ""
    original_url: str = ""
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    click_count: int = 0
    last_accessed: Optional[datetime] = None

    @property
    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
