from data360_agent_governance.cli import main


def test_invalid_table_name_returns_2(capsys):
    code = main(["check", "--table", "a;DROP TABLE x"], env={})
    assert code == 2
    assert "Invalid table name" in capsys.readouterr().err


def test_missing_settings_returns_2_and_lists_them(capsys):
    code = main(["check", "--table", "Individual__dlm"], env={})
    assert code == 2
    assert "SF_CLIENT_ID" in capsys.readouterr().err