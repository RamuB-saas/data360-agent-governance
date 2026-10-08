"""Command-line interface."""

import argparse
import os
import sys
from collections.abc import Mapping

import salesforce_datacloud_connector as sfdc
from dotenv import load_dotenv

from .config import ConfigError, load_settings
from .connection import connect
from .schema import TableNotFoundError, list_columns
from .sql import validate_table_name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="data360-agent-governance")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="Connect and list the columns of a table")
    check.add_argument("--table", required=True, help="Table (DMO) API name")
    return parser


def main(argv: list[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if env is None:
        load_dotenv()
        env = os.environ
    try:
        table = validate_table_name(args.table)  # fail fast, before any network call
        conn = connect(load_settings(env))
        columns = list_columns(conn, table)
    except (ConfigError, ValueError, TableNotFoundError, sfdc.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(f"Connected. {table} has {len(columns)} columns:")
    for name in columns:
        print(f"  {name}")
    return 0