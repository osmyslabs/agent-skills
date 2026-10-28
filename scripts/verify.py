"""Check the public repository and its independently installable skill package.

Uses only Python 3.10+ standard library. Does not run an agent or fetch links.
"""

from __future__ import annotations

import ast
from pathlib import Path
import re
import stat
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "project-architecture-and-blueprint"
EXCLUDED = {".git", "build", "__pycache__", ".idea"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
PERSONAL_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/]+Users[\\/]+[^\s<>\"']+|/home/[a-z0-9_.-]+/|/Users/[a-z0-9_.-]+/)"
)


def repository_files(directory: Path):
    for entry in sorted(directory.iterdir()):
        if entry.name in EXCLUDED:
            continue
        attributes = entry.lstat()
        if entry.is_symlink() or (
            getattr(attributes, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        ):
            raise ValueError(f"Linked filesystem entry: {entry.relative_to(ROOT)}")
        if entry.is_dir():
            yield from repository_files(entry)
        else:
            yield entry


def main() -> None:
    manifest = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not manifest.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    frontmatter = manifest.split("---", 2)[1]
    fields = dict(re.findall(r"^([a-z-]+): (.+)$", frontmatter, re.MULTILINE))
    if fields.get("name") != SKILL.name:
        raise ValueError("Canonical skill name differs from its folder")
    if not 1 <= len(fields.get("description", "")) <= 1024:
        raise ValueError("Expected a nonempty description of at most 1024 characters")
    if fields.get("license") != "MIT":
        raise ValueError("Expected MIT license in skill frontmatter")
    if (ROOT / "LICENSE").read_bytes() != (SKILL / "LICENSE").read_bytes():
        raise ValueError("Installed skill must carry the complete repository license")
    for required in ("references", "agents", "evals", "scripts"):
        if not (SKILL / required).is_dir():
            raise ValueError(f"Missing package directory: {required}")

    files = list(repository_files(ROOT))
    link_count = 0
    python_count = 0
    for path in files:
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        if PERSONAL_PATH.search(text):
            raise ValueError(f"Personal absolute path found in {relative}")
        if path.suffix == ".py":
            ast.parse(text, filename=str(relative))
            python_count += 1
        if path.suffix != ".md":
            continue
        boundary = SKILL if path.is_relative_to(SKILL) else ROOT
        for raw in MARKDOWN_LINK.findall(text):
            target = raw.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            parts = urlsplit(target)
            if parts.scheme in {"https", "http", "mailto"} or not parts.path:
                continue
            if parts.scheme or parts.netloc or Path(parts.path).is_absolute():
                raise ValueError(f"Unsupported local link in {relative}: {target}")
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(boundary):
                raise ValueError(f"Link leaves its distribution boundary in {relative}: {target}")
            if not destination.exists():
                raise ValueError(f"Missing local link target in {relative}: {target}")
            link_count += 1
    print(
        f"Verified {len(files)} UTF-8 files, {link_count} local Markdown links, "
        f"{python_count} Python sources and matching MIT notices. "
        "No agent execution or external-link validation performed."
    )


if __name__ == "__main__":
    main()
