from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional


class ShortenRequest(BaseModel):
    url: HttpUrl = Field(
        description="URL original a ser encurtada",
        examples=["https://www.google.com/search?q=python+fastapi"],
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="Data e hora de expiração (opcional). Use formato ISO.",
        examples=["2026-12-31T23:59:59"],
    )


class LinkResponse(BaseModel):
    short_url: str = Field(examples=["/aB3cD9eF"])
    slug: str = Field(examples=["aB3cD9eF"])


class StatsResponse(BaseModel):
    original_url: str = Field(
        examples=["https://www.google.com/search?q=python+fastapi"]
    )
    created_at: Optional[str] = Field(examples=["2026-05-08T10:30:00"])
    expires_at: Optional[str] = Field(examples=["2026-12-31T23:59:59"])
    click_count: int = Field(examples=[42])
    last_accessed: Optional[str] = Field(examples=["2026-05-08T14:22:10"])
    is_expired: bool = Field(examples=[False])
