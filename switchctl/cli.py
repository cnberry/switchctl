from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from switchctl.config import (
    DEFAULT_CONFIG_PATH,
    load_raw_config,
    redacted_config,
    resolve_config_path,
    write_default_config,
)
from switchctl.errors import SwitchctlError
from switchctl.formatters import render_list, render_status
from switchctl.service import SwitchService

VERB_COMMANDS = {"on": True, "off": False, "enable": True, "disable": False}


def add_selector_args(parser: argparse.ArgumentParser, *, include_selector: bool) -> None:
    if include_selector:
        parser.add_argument("selector", nargs="?", default=None, help="target id")
    parser.add_argument("--room", help="filter by room")
    parser.add_argument("--role", help="filter by role")
    parser.add_argument("--tag", dest="tags", action="append", help="filter by tag (repeatable)")
    parser.add_argument(
        "--all", action="store_true", dest="all_targets", help="select all matching targets"
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="switchctl", description="Terminal-first switch-backed endpoint control"
    )
    parser.add_argument("--config", type=Path, help="config file path override")

    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list")
    add_selector_args(list_parser, include_selector=False)

    status_parser = sub.add_parser("status")
    add_selector_args(status_parser, include_selector=True)

    doctor_parser = sub.add_parser("doctor")
    add_selector_args(doctor_parser, include_selector=True)

    for command in VERB_COMMANDS:
        verb = sub.add_parser(command)
        add_selector_args(verb, include_selector=True)
        verb.add_argument("--yes", action="store_true")

    config = sub.add_parser("config")
    config_sub = config.add_subparsers(dest="config_command", required=True)
    config_sub.add_parser("init")
    config_sub.add_parser("show")

    return parser


def dump_json(data) -> None:
    print(json.dumps(data, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "config":
        if args.config_command == "init":
            path = write_default_config(args.config or DEFAULT_CONFIG_PATH)
            print(path)
            return 0
        if args.config_command == "show":
            path = resolve_config_path(args.config)
            write_default_config(path)
            dump_json(redacted_config(load_raw_config(path)))
            return 0

    try:
        service = SwitchService(args.config)
        common = {
            "selector": getattr(args, "selector", None),
            "room": getattr(args, "room", None),
            "role": getattr(args, "role", None),
            "tags": getattr(args, "tags", None),
            "all_targets": getattr(args, "all_targets", False),
        }

        if args.command == "list":
            rows = service.list_targets(**common)
            if args.json:
                dump_json([row.to_safe_dict() for row in rows])
            else:
                print(render_list(rows))
            return 0

        if args.command == "status":
            rows = service.status(**common)
            if args.json:
                dump_json([row.to_dict() for row in rows])
            else:
                print(render_status(rows))
            return 0

        if args.command == "doctor":
            rows = service.doctor(**common)
            if args.json:
                dump_json([row.to_dict() for row in rows])
            else:
                print(render_status(rows))
            return 0

        if args.command in VERB_COMMANDS:
            rows = service.set_enabled(VERB_COMMANDS[args.command], yes=args.yes, **common)
            if args.json:
                dump_json([row.to_dict() for row in rows])
            else:
                print(render_status(rows))
            return 0

    except SwitchctlError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
