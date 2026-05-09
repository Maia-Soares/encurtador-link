from datetime import datetime
from unittest.mock import Mock
import pytest
from app.application.use_cases.shorten_url import ShortenUrlUseCase
from app.domain.exceptions import InvalidURLError
from app.domain.entities import Link


def test_shorten_valid_url():
    repo = Mock()
    repo.save.return_value = Link(
        slug="aB3cD9eF", original_url="https://google.com")

    uc = ShortenUrlUseCase(repo)
    result = uc.execute("https://google.com")

    assert result.slug == "aB3cD9eF"
    repo.save.assert_called_once()


def test_shorten_invalid_url():
    repo = Mock()
    uc = ShortenUrlUseCase(repo)

    with pytest.raises(InvalidURLError):
        uc.execute("não-é-uma-url")
