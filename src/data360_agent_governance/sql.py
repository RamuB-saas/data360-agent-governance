"""Small helpers for building safe SQL."""

import re

_TABLE_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


def validate_table_name(name: str) -> str:
    """Return the name if it is a plain identifier, otherwise raise ValueError."""
    if not _TABLE_RE.fullmatch(name):
        raise ValueError(f"Invalid table name: {name!r}")
    return name