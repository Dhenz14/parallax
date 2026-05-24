import pytest
from fastapi import HTTPException
from starlette.requests import Request

from router.main import normalize_endpoint_base_url, require_admin


def _request_from(host: str, headers: dict[str, str] | None = None) -> Request:
    raw_headers = []
    for key, value in (headers or {}).items():
        raw_headers.append((key.lower().encode("latin-1"), value.encode("latin-1")))
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/endpoints",
            "headers": raw_headers,
            "client": (host, 12345),
        }
    )


def test_admin_without_token_allows_loopback(monkeypatch):
    monkeypatch.delenv("PARALLAX_ROUTER_ADMIN_TOKEN", raising=False)

    require_admin(_request_from("127.0.0.1"))


def test_admin_without_token_rejects_remote(monkeypatch):
    monkeypatch.delenv("PARALLAX_ROUTER_ADMIN_TOKEN", raising=False)

    with pytest.raises(HTTPException) as exc:
        require_admin(_request_from("203.0.113.8"))

    assert exc.value.status_code == 401


def test_admin_token_required_when_configured(monkeypatch):
    monkeypatch.setenv("PARALLAX_ROUTER_ADMIN_TOKEN", "secret-token")

    with pytest.raises(HTTPException):
        require_admin(_request_from("127.0.0.1", {"authorization": "Bearer wrong"}))

    require_admin(_request_from("203.0.113.8", {"authorization": "Bearer secret-token"}))


def test_endpoint_url_normalization_accepts_loopback_root():
    assert normalize_endpoint_base_url("http://127.0.0.1:3001/") == "http://127.0.0.1:3001"


@pytest.mark.parametrize(
    "raw_url",
    [
        "ftp://127.0.0.1:3001",
        "http://user:pass@127.0.0.1:3001",
        "http://127.0.0.1:3001/v1",
        "http://127.0.0.1:3001?x=1",
        "http://169.254.169.254/latest/meta-data",
    ],
)
def test_endpoint_url_normalization_rejects_unsafe_targets(raw_url):
    with pytest.raises(ValueError):
        normalize_endpoint_base_url(raw_url)
