import pytest

from data360_agent_governance.sql import validate_table_name


@pytest.mark.parametrize("name", ["UnifiedIndividual__dlm", "ssot__Individual__dlm", "T1"])
def test_valid_names_pass_through(name):
    assert validate_table_name(name) == name


@pytest.mark.parametrize(
    "name",
    ["", "1abc", "a b", "a;DROP TABLE x", "a-b", "a.b", "x' OR '1'='1"],
)
def test_invalid_names_are_rejected(name):
    with pytest.raises(ValueError):
        validate_table_name(name)