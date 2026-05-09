from datetime import datetime, timedelta
from unittest.mock import Mock
import pytest
from app.application.use_cases.redirect_url import RedirectUrlUseCase
from app.domain.exceptions import SlugNotFoundError, LinkExpiredError
from app.domain.entities import Link


def test_redirect_cache_hit():
    repo = Mock()
    cache = Mock()
    cached_link = Link(
        slug="test1234", original_url="https://google.com", click_count=0)
    cache.get.return_value = cached_link.__dict__
    cache.get.return_value["expires_at"] = None

    uc = RedirectUrlUseCase(repo, cache, ttl_seconds=3600)
    result = uc.execute("test1234")

    assert result.original_url == "https://google.com"
    repo.get_by_slug.assert_not_called()


def test_redirect_not_found():
    repo = Mock()
    repo.get_by_slug.return_value = None
    cache = Mock()
    cache.get.return_value = None

    uc = RedirectUrlUseCase(repo, cache)

    with pytest.raises(SlugNotFoundError):
        uc.execute("fake1234")


def test_redirect_expired():
    repo = Mock()
    cache = Mock()
    expired = Link(
        slug="exp12345",
        original_url="https://x.com",
        expires_at=datetime.utcnow() - timedelta(hours=1)
    )
    cache.get.return_value = expired.__dict__
    cache.get.return_value["expires_at"] = expired.expires_at

    uc = RedirectUrlUseCase(repo, cache)

    with pytest.raises(LinkExpiredError):
        uc.execute("exp12345")
