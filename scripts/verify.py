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
SKILLS = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
INDEX = ROOT / "llms.txt"
PUBLIC_RAW_PREFIX = "https://raw.githubusercontent.com/osmyslabs/agent-skills/main/"
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
    if not SKILLS:
        raise ValueError("Expected at least one skill in the catalog")
    for skill in SKILLS:
        manifest = (skill / "SKILL.md").read_text(encoding="utf-8")
        if not manifest.startswith("---\n"):
            raise ValueError(f"{skill.name}: missing YAML frontmatter")
        fields = dict(re.findall(r"^([a-z-]+): (.+)$", manifest.split("---", 2)[1], re.MULTILINE))
        if fields.get("name") != skill.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name) or len(skill.name) > 64:
            raise ValueError(f"{skill.name}: invalid canonical name")
        if not 1 <= len(fields.get("description", "")) <= 1024 or fields.get("license") != "MIT":
            raise ValueError(f"{skill.name}: expected a description and MIT license")
        if (ROOT / "LICENSE").read_bytes() != (skill / "LICENSE").read_bytes():
            raise ValueError(f"{skill.name}: missing complete repository license")
        for required in ("references", "agents", "evals", "scripts"):
            if not (skill / required).is_dir():
                raise ValueError(f"{skill.name}: missing {required}")
        if (skill / "scripts/install.py").read_bytes() != (ROOT / "scripts/install.py").read_bytes():
            raise ValueError(f"{skill.name}: installer differs from the maintained repository copy")
        route = f"skills/{skill.name}/SKILL.md"
        if any(route not in (ROOT / name).read_text(encoding="utf-8") for name in ("README.md", "llms.txt")):
            raise ValueError(f"{skill.name}: missing from a public catalog entry point")
    if not INDEX.is_file():
        raise ValueError("Missing root documentation index: llms.txt")

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
        if path.suffix != ".md" and path != INDEX:
            continue
        boundary = next((skill for skill in SKILLS if path.is_relative_to(skill)), ROOT)
        for raw in MARKDOWN_LINK.findall(text):
            target = raw.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if path == INDEX and target.startswith(PUBLIC_RAW_PREFIX):
                # Verify owned raw-document URLs against the current checkout.
                target = target[len(PUBLIC_RAW_PREFIX):]
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
        f"Verified {len(files)} UTF-8 files, {link_count} repository document links, "
        f"{python_count} Python sources and {len(SKILLS)} independently licensed skills. "
        "No agent execution or external-link validation performed."
    )


if __name__ == "__main__":
    main()
