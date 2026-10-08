"""The only module that talks to the Data 360 connector library."""

import salesforce_datacloud_connector as sfdc

from .config import ConfigError, Settings


def connect(settings: Settings):
    """Open a Data 360 connection using the JWT bearer flow."""
    try:
        private_key = settings.private_key_path.read_text()
    except OSError as exc:
        raise ConfigError(f"Cannot read private key at {settings.private_key_path}") from exc
    return sfdc.connect(
        login_url=settings.login_url,
        auth_type="jwt",
        username=settings.username,
        client_id=settings.client_id,
        jwt_private_key=private_key,
        dataspace=settings.dataspace,
    )