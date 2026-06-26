"""Tests for `memos doctor` consistency checks."""

from __future__ import annotations

from pathlib import Path

from memos.doctor import check_project_layout, check_rules_index, check_shims
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


# --- check_project_layout ------------------------------------------------------


def _make_project(
    root: Path, name: str, *, self_: bool = False, with_repo_dir: bool = False
) -> None:
    """A minimal project folder with an AGENTS.md (optionally `self: true`)."""
    project = root / "projects" / name
    project.mkdir(parents=True)
    self_line = "self: true\n" if self_ else "self: false\n"
    (project / "AGENTS.md").write_text(f"---\nname: {name}\n{self_line}---\n\nBody.\n")
    if with_repo_dir:
        (project / "repo").mkdir()


def _write_gitmodules(root: Path, *paths: str) -> None:
    blocks = "".join(
        f'[submodule "{p}"]\n\tpath = {p}\n\turl = git@github.com:memclutter/x.git\n'
        for p in paths
    )
    (root / ".gitmodules").write_text(blocks)


def test_check_project_layout_clean(tmp_path: Path) -> None:
    _make_project(tmp_path, "dotfiles")
    _write_gitmodules(tmp_path, "projects/dotfiles/vcs/dotfiles")
    assert check_project_layout(tmp_path) == []


def test_check_project_layout_legacy_repo_dir(tmp_path: Path) -> None:
    _make_project(tmp_path, "dotfiles", with_repo_dir=True)
    _write_gitmodules(tmp_path, "projects/dotfiles/repo")
    problems = check_project_layout(tmp_path)
    assert any("legacy repo/" in p and "dotfiles" in p for p in problems)


def test_check_project_layout_submodule_outside_vcs(tmp_path: Path) -> None:
    _make_project(tmp_path, "dotfiles")
    _write_gitmodules(tmp_path, "projects/dotfiles/somewhere")
    problems = check_project_layout(tmp_path)
    assert any("outside vcs/" in p and "somewhere" in p for p in problems)


def test_check_project_layout_self_exempt(tmp_path: Path) -> None:
    # A self project may have neither vcs/ nor a submodule; a stray repo/ is ignored.
    _make_project(tmp_path, "memos", self_=True, with_repo_dir=True)
    assert check_project_layout(tmp_path) == []


# --- smoke ---------------------------------------------------------------------


def test_real_repo_is_healthy() -> None:
    root = find_repo_root()
    assert check_shims(root) == []
    assert check_rules_index(root) == []
    assert check_project_layout(root) == []
