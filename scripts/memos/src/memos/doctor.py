"""OS consistency checks for `memos doctor`.

Each check is a pure function taking the repo root and returning a list of
human-readable problem strings (empty list = healthy). ``run_doctor`` runs them
all, prints a per-check summary, collects every problem, and returns a process
exit code (non-zero if anything is wrong). The command is **read-only**.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

from .shims import TOOLS, compute_shims, find_repo_root

# Markdown link target pointing at a rule file, e.g. `[x](rules/x.md)`.
_RULE_LINK = re.compile(r"\((?:\./)?rules/([A-Za-z0-9._-]+\.md)[)#]")


def check_shims(root: Path) -> list[str]:
    """Every canonical skill has a correct shim in each tool dir; none are stale."""
    problems: list[str] = []
    expected = compute_shims(root)

    for path, content in expected.items():
        rel = path.relative_to(root)
        if not path.is_file():
            problems.append(f"missing shim: {rel}")
        elif path.read_text() != content:
            problems.append(f"shim out of date: {rel} (run `uv run memos shimify`)")

    expected_paths = set(expected)
    for dirname in TOOLS.values():
        tool_skills = root / dirname / "skills"
        if not tool_skills.is_dir():
            continue
        for skill_dir in sorted(tool_skills.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md") not in expected_paths:
                rel = skill_dir.relative_to(root)
                problems.append(f"stale shim (no canonical skill): {rel}")
    return problems


def check_rules_index(root: Path) -> list[str]:
    """Every rules/*.md is linked from AGENTS.md, and every link resolves."""
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return [f"missing AGENTS.md at {root}"]

    linked = set(_RULE_LINK.findall(agents.read_text()))
    rules_dir = root / "rules"
    actual = {p.name for p in rules_dir.glob("*.md")} if rules_dir.is_dir() else set()

    problems: list[str] = []
    for name in sorted(actual - linked):
        problems.append(f"rule not indexed in AGENTS.md: rules/{name}")
    for name in sorted(linked - actual):
        problems.append(f"AGENTS.md links a missing rule: rules/{name}")
    return problems


_CHECKS: list[tuple[str, Callable[[Path], list[str]]]] = [
    ("shims", check_shims),
    ("rules index", check_rules_index),
]


def run_doctor(root: Path | None = None) -> int:
    root = root or find_repo_root()
    total = 0
    for label, check in _CHECKS:
        problems = check(root)
        total += len(problems)
        if problems:
            print(f"✗ {label}: {len(problems)} problem(s)")
            for problem in problems:
                print(f"    - {problem}")
        else:
            print(f"✓ {label}: ok")

    if total:
        print(f"\ndoctor: {total} problem(s) found")
        return 1
    print("\ndoctor: all checks passed")
    return 0
