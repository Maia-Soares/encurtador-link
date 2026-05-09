from unittest.mock import Mock
import pytest
from datetime import datetime
from app.application.use_cases.get_stats import GetStatsUseCase
from app.domain.exceptions import SlugNotFoundError
from app.domain.entities import Link


def test_get_stats_success():
    repo = Mock()
    agora = datetime(2026, 5, 10, 12, 0, 0)
    link = Link(
        slug="abc12345",
        original_url="https://exemplo.com",
        created_at=agora,
        expires_at=None,
        click_count=7,
        last_accessed=agora,
    )
    repo.get_by_slug.return_value = link

    uc = GetStatsUseCase(repo)
    resultado = uc.execute("abc12345")

    assert resultado["click_count"] == 7
    assert resultado["original_url"] == "https://exemplo.com"
    assert resultado["is_expired"] is False
    repo.get_by_slug.assert_called_once_with("abc12345")


def test_get_stats_not_found():
    repo = Mock()
    repo.get_by_slug.return_value = None

    uc = GetStatsUseCase(repo)

    with pytest.raises(SlugNotFoundError):
        uc.execute("slug_inexistente")
