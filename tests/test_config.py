from pathlib import Path

import pytest

from data360_agent_governance.config import ConfigError, load_settings

VALID = {
    "SF_LOGIN_URL": "https://login.salesforce.com",
    "SF_CLIENT_ID": "abc123",
    "SF_USERNAME": "dev@example.com",
    "SF_PRIVATE_KEY_PATH": "/home/me/.secrets/d360.key",
}


def test_load_settings_reads_values():
    settings = load_settings(VALID)
    assert settings.username == "dev@example.com"
    assert settings.private_key_path == Path("/home/me/.secrets/d360.key")
    assert settings.dataspace is None


def test_dataspace_is_optional_but_read_when_present():
    settings = load_settings({**VALID, "SF_DATASPACE": "default"})
    assert settings.dataspace == "default"


def test_all_missing_settings_are_reported_together():
    with pytest.raises(ConfigError) as excinfo:
        load_settings({"SF_LOGIN_URL": "https://login.salesforce.com"})
    message = str(excinfo.value)
    assert "SF_CLIENT_ID" in message
    assert "SF_USERNAME" in message
    assert "SF_PRIVATE_KEY_PATH" in message