"""Load and validate settings from environment variables."""
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

REQUIRED = ("SF_LOGIN_URL", "SF_CLIENT_ID", "SF_USERNAME", "SF_PRIVATE_KEY_PATH")

class ConfigError(Exception):
    """Raised when required settings are missing"""


@dataclass(frozen=True)
class Settings:
    SF_LOGIN_URL: str
    SF_CLIENT_ID: str
    SF_USERNAME: str
    SF_PRIVATE_KEY_PATH: Path
    dataspace: str | None = None

def load_settings(env: Mapping[str, str]) -> Settings:
    missing = [name for name in REQUIRED if not env.get(name)]
    if missing:
        raise ConfigError(f"Missing required settings: {', '.join(missing)}")
    return Settings(
        SF_LOGIN_URL=env["SF_LOGIN_URL"],
        SF_CLIENT_ID=env["SF_CLIENT_ID"],
        SF_USERNAME=env["SF_USERNAME"],
        SF_PRIVATE_KEY_PATH=Path(env["SF_PRIVATE_KEY_PATH"]),
        dataspace=env.get("SF_DATASPACE"),
    )