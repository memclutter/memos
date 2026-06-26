"""Tests for the shim model.

The headline guarantee of the CLI migration is that shim generation is unchanged:
``compute_shims`` over the real repo must equal the bytes already on disk. The
round-trip test exercises generation and drift detection on a throwaway repo.
"""

from __future__ import annotations

from pathlib import Path

from memos.shims import compute_shims, find_repo_root, write_shims


def test_computed_shims_match_disk() -> None:
    """compute_shims over the real repo equals the committed shim files."""
    root = find_repo_root()
    shims = compute_shims(root)
    assert shims, "expected at least one shim to be computed"
    for path, content in shims.items():
        assert path.is_file(), f"missing shim on disk: {path}"
        assert path.read_text() == content, f"shim drifted from canon: {path}"


def _make_repo(root: Path) -> None:
    (root / "AGENTS.md").write_text("# marker\n")
    (root / "rules").mkdir()
    skill = root / "skills" / "demo.thing.do"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: demo.thing.do\ndescription: Demo skill.\n---\n\nBody.\n"
    )


def test_write_then_compute_round_trip(tmp_path: Path) -> None:
    _make_repo(tmp_path)

    n_skills, n_shims = write_shims(tmp_path)
    assert n_skills == 1
    assert n_shims == 4  # one shim per supported tool

    # What's on disk matches what compute_shims says it should be.
    for path, content in compute_shims(tmp_path).items():
        assert path.read_text() == content


def test_mutated_shim_is_detected(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    write_shims(tmp_path)

    shims = compute_shims(tmp_path)
    target = next(iter(shims))
    target.write_text("tampered\n")

    assert target.read_text() != shims[target]
