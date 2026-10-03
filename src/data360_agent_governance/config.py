"""Load and validate settings from environment variables."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

REQUIRED = ("SF_LOGIN_URL", "SF_CLIENT_ID", "SF_USERNAME", "SF_PRIVATE_KEY_PATH")


class ConfigError(Exception):
    """Raised when required settings are missing."""


@dataclass(frozen=True)
class Settings:
    login_url: str
    client_id: str
    username: str
    private_key_path: Path
    dataspace: str | None = None


def load_settings(env: Mapping[str, str]) -> Settings:
    missing = [name for name in REQUIRED if not env.get(name)]
    if missing:
        raise ConfigError("Missing required settings: " + ", ".join(missing))
    return Settings(
        login_url=env["SF_LOGIN_URL"],
        client_id=env["SF_CLIENT_ID"],
        username=env["SF_USERNAME"],
        private_key_path=Path(env["SF_PRIVATE_KEY_PATH"]),
        dataspace=env.get("SF_DATASPACE") or None,
    )