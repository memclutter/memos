"""Tests for `memos doctor` consistency checks."""

from __future__ import annotations

from pathlib import Path

from memos.doctor import check_rules_index, check_shims
from memos.shims import find_repo_root, write_shims


def _make_repo(root: Path, rules: tuple[str, ...] = ("git.md",)) -> None:
    """A minimal OS repo: AGENTS.md indexing the given rules + one skill."""
    (root / "rules").mkdir()
    links = "\n".join(f"- [{name}](rules/{name})" for name in rules)
    (root / "AGENTS.md").write_text(f"# Index\n\n{links}\n")
    for name in rules:
        (root / "rules" / name).write_text(f"# {name}\n")
    skill = root / "skills" / "demo.thing.do"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: demo.thing.do\ndescription: Demo skill.\n---\n\nBody.\n"
    )


# --- check_shims ---------------------------------------------------------------


def test_check_shims_clean(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    write_shims(tmp_path)
    assert check_shims(tmp_path) == []


def test_check_shims_missing(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    write_shims(tmp_path)
    (tmp_path / ".claude" / "skills" / "demo.thing.do" / "SKILL.md").unlink()
    problems = check_shims(tmp_path)
    assert any("missing shim" in p for p in problems)


def test_check_shims_out_of_date(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    write_shims(tmp_path)
    shim = tmp_path / ".cursor" / "skills" / "demo.thing.do" / "SKILL.md"
    shim.write_text("tampered\n")
    problems = check_shims(tmp_path)
    assert any("out of date" in p for p in problems)


def test_check_shims_stale(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    write_shims(tmp_path)
    ghost = tmp_path / ".codex" / "skills" / "ghost"
    ghost.mkdir(parents=True)
    (ghost / "SKILL.md").write_text("orphan\n")
    problems = check_shims(tmp_path)
    assert any("stale shim" in p for p in problems)


# --- check_rules_index ---------------------------------------------------------


def test_check_rules_index_clean(tmp_path: Path) -> None:
    _make_repo(tmp_path, rules=("git.md", "go.md"))
    assert check_rules_index(tmp_path) == []


def test_check_rules_index_unindexed(tmp_path: Path) -> None:
    _make_repo(tmp_path, rules=("git.md",))
    (tmp_path / "rules" / "orphan.md").write_text("# orphan\n")  # not linked
    problems = check_rules_index(tmp_path)
    assert any("not indexed" in p and "orphan.md" in p for p in problems)


def test_check_rules_index_missing_target(tmp_path: Path) -> None:
    _make_repo(tmp_path, rules=("git.md",))
    # link a rule that doesn't exist on disk
    (tmp_path / "AGENTS.md").write_text("# Index\n\n- [ghost.md](rules/ghost.md)\n")
    problems = check_rules_index(tmp_path)
    assert any("missing rule" in p and "ghost.md" in p for p in problems)


# --- smoke ---------------------------------------------------------------------


def test_real_repo_is_healthy() -> None:
    root = find_repo_root()
    assert check_shims(root) == []
    assert check_rules_index(root) == []
