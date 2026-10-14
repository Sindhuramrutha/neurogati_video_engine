"""`pipeline credentials`: provider API keys, from the command line.

Its own module so `cli.py` stays inside its length budget; `cli.build_parser`
adds these commands the same way it adds its own.
"""

from __future__ import annotations

import argparse
import sys

from pipeline.cli import emit
from pipeline.operations import OperationFailed


def command_credentials_show(args: argparse.Namespace) -> int:
    from pipeline.credentials import describe_credentials

    return emit(describe_credentials(), args)


def command_credentials_set(args: argparse.Namespace) -> int:
    """Set a credential without it appearing in shell history.

    The value is read from stdin rather than taken as an argument, because an
    argument lands in `.bash_history` and in the process list where any other
    user on the machine can read it.
    """
    from pipeline.credentials import save_credentials

    value = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    if not value and not args.clear:
        raise OperationFailed(
            f"Pipe the value in: echo -n '<value>' | pipeline credentials set {args.name}\n"
            f"Or pass --clear to remove it."
        )
    return emit(save_credentials({args.name: "" if args.clear else value}), args)


def add_credentials_commands(sub, add_parser) -> None:
    credentials = sub.add_parser("credentials", help="provider API keys")
    credentials_sub = credentials.add_subparsers(dest="credentials_command", required=True)

    p = add_parser(credentials_sub, "show", help="status of every key, masked")
    p.set_defaults(fn=command_credentials_show)

    p = add_parser(credentials_sub, "set", help="set one key, reading the value from stdin")
    p.add_argument("name", help="e.g. LLM_API_KEY")
    p.add_argument("--clear", action="store_true", help="remove it instead")
    p.set_defaults(fn=command_credentials_set)
