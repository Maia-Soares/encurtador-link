import pytest
import time
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.interface.main import app
from app.infrastructure.db import SessionLocal
from app.infrastructure.models import LinkModel
from app.infrastructure.cache_client import redis_client

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    db = SessionLocal()
    db.query(LinkModel).delete()
    db.commit()
    redis_client.flushdb()
    yield
    db.query(LinkModel).delete()
    db.commit()
    redis_client.flushdb()
    db.close()


@pytest.mark.integration
def test_fluxo_completo_encurtar_redirecionar_deletar():
    resp = client.post("/shorten", json={"url": "https://github.com"})
    assert resp.status_code == 200
    slug = resp.json()["slug"]
    assert len(slug) == 8

    resp = client.get(f"/{slug}", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["Location"].rstrip(
        "/") == "https://github.com".rstrip("/")

    resp = client.get(f"/{slug}/stats")
    assert resp.status_code == 200
    assert resp.json()["click_count"] == 1

    resp = client.delete(f"/{slug}")
    assert resp.status_code == 200

    resp = client.get(f"/{slug}", follow_redirects=False)
    assert resp.status_code == 404


@pytest.mark.integration
def test_link_com_expiracao_retorna_302_e_410():
    expires_in = datetime.utcnow() + timedelta(seconds=5)
    resp = client.post(
        "/shorten", json={"url": "https://python.org", "expires_at": expires_in.isoformat()})
    slug = resp.json()["slug"]

    resp = client.get(f"/{slug}", follow_redirects=False)
    assert resp.status_code == 302

    time.sleep(6)

    resp = client.get(f"/{slug}", follow_redirects=False)
    assert resp.status_code == 410
