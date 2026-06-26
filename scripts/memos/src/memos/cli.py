"""memos — the OS CLI.

Helper commands that keep the personal OS running. Run through uv:

    uv run memos <command> [args]

Commands:
    shimify   Regenerate per-tool skill shims from the canonical skills/.
    doctor    Check OS consistency (shims in sync, rules indexed).
"""

from __future__ import annotations

import argparse
import sys

from .doctor import run_doctor
from .shims import TOOLS, find_repo_root, write_shims


def cmd_shimify(_args: argparse.Namespace) -> int:
    root = find_repo_root()
    n_skills, n_shims = write_shims(root)
    print(
        f"shimify: {n_skills} skill(s) -> {n_shims} shim(s) across {len(TOOLS)} tool(s)"
    )
    return 0


def cmd_doctor(_args: argparse.Namespace) -> int:
    return run_doctor()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="memos", description="The memos OS CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_shim = sub.add_parser("shimify", help="regenerate per-tool skill shims")
    p_shim.set_defaults(func=cmd_shimify)

    p_doctor = sub.add_parser("doctor", help="check OS consistency")
    p_doctor.set_defaults(func=cmd_doctor)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
