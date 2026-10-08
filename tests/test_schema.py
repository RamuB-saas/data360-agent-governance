from types import SimpleNamespace

import pytest

from data360_agent_governance.schema import TableNotFoundError, list_columns


class FakeConn:
    def __init__(self, metadata):
        self._metadata = metadata
        self.asked_for = None

    def get_table_metadata(self, name):
        self.asked_for = name
        return self._metadata


def test_list_columns_returns_field_names():
    meta = SimpleNamespace(fields=[SimpleNamespace(name="Id__c"), SimpleNamespace(name="Email__c")])
    conn = FakeConn(meta)
    assert list_columns(conn, "Individual__dlm") == ["Id__c", "Email__c"]
    assert conn.asked_for == "Individual__dlm"


def test_unknown_table_raises():
    with pytest.raises(TableNotFoundError):
        list_columns(FakeConn(None), "Nope__dlm")


def test_bad_name_is_rejected_before_any_lookup():
    conn = FakeConn(None)
    with pytest.raises(ValueError):
        list_columns(conn, "a;DROP TABLE x")
    assert conn.asked_for is None