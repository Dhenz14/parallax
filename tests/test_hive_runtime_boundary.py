import json

from parallax import cli
from parallax_utils import version_check


class _FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps({"tag_name": "v0.1.2"}).encode("utf-8")


def test_release_check_defaults_to_hive_fork(monkeypatch):
    calls = []

    def fake_urlopen(url, timeout):
        calls.append((url, timeout))
        return _FakeResponse()

    monkeypatch.delenv("PARALLAX_RELEASE_API_URL", raising=False)
    monkeypatch.setattr(version_check.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(version_check, "get_current_version", lambda: "0.1.2")

    version_check.check_latest_release()

    assert calls == [(version_check.DEFAULT_RELEASE_API_URL, 4)]
    assert "Dhenz14/parallax" in version_check.DEFAULT_RELEASE_API_URL


def test_release_check_allows_operator_override(monkeypatch):
    calls = []
    override = "https://example.invalid/releases/latest"

    def fake_urlopen(url, timeout):
        calls.append((url, timeout))
        return _FakeResponse()

    monkeypatch.setenv("PARALLAX_RELEASE_API_URL", override)
    monkeypatch.setattr(version_check.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(version_check, "get_current_version", lambda: "0.1.2")

    version_check.check_latest_release()

    assert calls == [(override, 4)]


def test_package_info_upload_requires_explicit_url(monkeypatch):
    calls = []

    def fake_post(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.delenv("PARALLAX_PACKAGE_INFO_UPLOAD_URL", raising=False)
    monkeypatch.setattr(cli.requests, "post", fake_post)

    assert cli.upload_package_info({"version": "0.1.2"}) is False
    assert calls == []


def test_package_info_upload_uses_operator_url(monkeypatch):
    calls = []
    upload_url = "https://example.invalid/parallax/upload"

    def fake_post(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setenv("PARALLAX_PACKAGE_INFO_UPLOAD_URL", upload_url)
    monkeypatch.setattr(cli.requests, "post", fake_post)

    assert cli.upload_package_info({"version": "0.1.2"}) is True
    assert calls[0][0] == (upload_url,)
    assert calls[0][1]["json"] == {"version": "0.1.2"}
