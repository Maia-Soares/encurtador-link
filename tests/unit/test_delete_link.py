from unittest.mock import Mock
from app.application.use_cases.delete_link import DeleteLinkUseCase


def test_delete_link_sucesso():
    repo = Mock()
    cache = Mock()

    uc = DeleteLinkUseCase(repo, cache)
    uc.execute("del98765")

    repo.delete.assert_called_once_with("del98765")
    cache.delete.assert_called_once_with("del98765")
