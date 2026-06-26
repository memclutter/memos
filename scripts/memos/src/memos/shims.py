"""Skill shim model: discover canonical skills and generate per-tool shims.

The canonical skills live in ``<root>/skills/<name>/SKILL.md``. Each supported
tool gets a generated shim under ``<root>/<tool-dir>/skills/<name>/SKILL.md`` that
points back to the canonical file. Shim generation is split into a pure
``compute_shims`` (path -> content, no I/O) and ``write_shims`` (the side effects),
so the output can be checked without touching the filesystem.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

import yaml

# Tool -> directory that holds that tool's generated skill shims.
TOOLS = {
    "claude": ".claude",
    "cursor": ".cursor",
    "opencode": ".opencode",
    "codex": ".codex",
}

# Canonical frontmatter keys that are carried into every shim.
GENERAL_KEYS = ("name", "description")

# Files/dirs that mark the OS repo root.
_ROOT_MARKERS = ("AGENTS.md", "rules")


def find_repo_root(start: Path | None = None) -> Path:
    """Ascend from ``start`` (default: this file) to the OS repo root.

    The root is the first ancestor that holds both ``AGENTS.md`` and ``rules/``.
    """
    here = (start or Path(__file__)).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "rules").is_dir():
            return candidate
    raise RuntimeError(
        f"repo root not found above {here} (no AGENTS.md + rules/ ancestor)"
    )


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter dict, body) for a markdown file with YAML frontmatter."""
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body.lstrip("\n")


def _load_skills(skills_dir: Path) -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    if not skills_dir.is_dir():
        return skills
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        fm, _ = _split_frontmatter(skill_md.read_text())
        name = fm.get("name")
        if name != skill_md.parent.name:
            raise SystemExit(
                f"skill name '{name}' must equal folder '{skill_md.parent.name}' "
                f"({skill_md})"
            )
        skills.append(fm)
    return skills


def _shim_text(fm: dict[str, Any], tool: str, shim_dir: Path, skills_dir: Path) -> str:
    name = fm["name"]
    out = {k: fm[k] for k in GENERAL_KEYS if k in fm}
    out.update((fm.get("x-shim") or {}).get(tool, {}))  # tool-specific extras

    canonical = skills_dir / name / "SKILL.md"
    rel = os.path.relpath(canonical, shim_dir)

    fm_yaml = yaml.safe_dump(out, sort_keys=False, allow_unicode=True).strip()
    return (
        f"---\n{fm_yaml}\n---\n\n"
        f"# {name}\n\n"
        f"> Generated shim — do not edit. "
        f"Source of truth: `skills/{name}/SKILL.md`.\n\n"
        f"Read and follow the canonical skill instructions before doing anything:\n"
        f"[{rel}]({rel})\n"
    )


def compute_shims(root: Path) -> dict[Path, str]:
    """Map every shim file path to its exact content. Pure: no filesystem writes."""
    skills_dir = root / "skills"
    skills = _load_skills(skills_dir)
    shims: dict[Path, str] = {}
    for tool, dirname in TOOLS.items():
        tool_skills = root / dirname / "skills"
        for fm in skills:
            shim_dir = tool_skills / fm["name"]
            shims[shim_dir / "SKILL.md"] = _shim_text(fm, tool, shim_dir, skills_dir)
    return shims


def write_shims(root: Path) -> tuple[int, int]:
    """Regenerate all shims on disk. Returns (skill count, shim count)."""
    skills = _load_skills(root / "skills")
    shims = compute_shims(root)
    for dirname in TOOLS.values():
        tool_skills = root / dirname / "skills"
        if tool_skills.exists():
            shutil.rmtree(tool_skills)  # fully owned + regenerated each run
    for path, content in shims.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return len(skills), len(shims)
