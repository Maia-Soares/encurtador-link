from unittest.mock import Mock
from app.application.use_cases.redirect_url import RedirectUrlUseCase
from app.domain.exceptions import SlugNotFoundError


def test_redirect_slug_not_found():
    repo = Mock()
    repo.get_by_slug.return_value = None
    cache = Mock()
    cache.get.return_value = None

    uc = RedirectUrlUseCase(repo, cache, ttl_seconds=3600)

    try:
        uc.execute("fake1234")
        assert False, "Deveria levantar SlugNotFoundError"
    except SlugNotFoundError:
        assert True  # ✅ Teste passa sem banco!
