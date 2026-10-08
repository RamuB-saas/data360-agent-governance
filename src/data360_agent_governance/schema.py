"""Read table structure (metadata only, never row data)."""

from .sql import validate_table_name


class TableNotFoundError(Exception):
    """Raised when the requested table does not exist."""


def list_columns(conn, table: str) -> list[str]:
    """Return the column names of a table using metadata only."""
    name = validate_table_name(table)
    metadata = conn.get_table_metadata(name)
    if metadata is None:
        raise TableNotFoundError(f"Table not found: {name}")
    return [field.name for field in metadata.fields]