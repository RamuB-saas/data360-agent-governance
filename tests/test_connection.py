import pytest

from data360_agent_governance import connection
from data360_agent_governance.config import ConfigError, Settings


def make_settings(key_path):
    return Settings(
        login_url="https://login.salesforce.com",
        client_id="abc123",
        username="dev@example.com",
        private_key_path=key_path,
    )


def test_connect_uses_jwt_flow_and_reads_key(tmp_path, monkeypatch):
    key_file = tmp_path / "test.key"
    key_file.write_text("FAKE-KEY-CONTENT")
    captured = {}

    def fake_connect(**kwargs):
        captured.update(kwargs)
        return "fake-connection"

    monkeypatch.setattr(connection.sfdc, "connect", fake_connect)

    result = connection.connect(make_settings(key_file))

    assert result == "fake-connection"
    assert captured["auth_type"] == "jwt"
    assert captured["jwt_private_key"] == "FAKE-KEY-CONTENT"
    assert captured["username"] == "dev@example.com"


def test_missing_key_file_gives_clear_error(tmp_path):
    with pytest.raises(ConfigError, match="Cannot read private key"):
        connection.connect(make_settings(tmp_path / "does-not-exist.key"))