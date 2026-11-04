#!/usr/bin/env python3
"""Copy this reviewed local skill into a selected host location; never overwrite."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import sys
from urllib.parse import unquote, urlsplit

PACKAGE = Path(__file__).resolve().parents[1]
SKILL_NAME = PACKAGE.name if (PACKAGE / "SKILL.md").is_file() else "project-architecture-and-blueprint"
HOSTS = {
    "codex": {
        "project": ".agents/skills", "user": ".agents/skills",
        "instructions": "AGENTS.md", "invocation": "$" + SKILL_NAME,
    },
    "claude": {
        "project": ".claude/skills", "user": ".claude/skills",
        "instructions": "CLAUDE.md", "invocation": "/" + SKILL_NAME,
    },
    "copilot": {
        "project": ".github/skills", "user": ".copilot/skills",
        "instructions": ".github/copilot-instructions.md", "invocation": SKILL_NAME,
    },
}


def validate_name(name):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError("Skill name must be a lowercase slug of at most 64 characters")
    return name


def manifest_name(source):
    text = (source / "SKILL.md").read_text(encoding="utf-8")
    header = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    name = re.search(r"(?m)^name: ([^\r\n]+)\r?$", header[1]) if header else None
    if not name or not re.search(r"(?m)^description: \S[^\r\n]*\r?$", header[1]):
        raise ValueError("Source manifest needs a canonical name and nonempty description")
    return validate_name(name[1])


def invocation_for(agent, name):
    return {"codex": "$", "claude": "/", "copilot": ""}[agent] + validate_name(name)


def installation_relative(agent, scope="project", name=SKILL_NAME):
    if agent not in HOSTS or scope not in ("project", "user"):
        raise ValueError("Select a documented agent and project/user scope")
    return Path(HOSTS[agent][scope]) / validate_name(name)


def linked_path(path):
    if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def package_files(source):
    """Check the complete relocatable package before writing a destination."""
    source = source.resolve(strict=True)
    manifest_name(source)
    files = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if any(part in (".git", "__pycache__") for part in relative.parts) or path.suffix in (".pyc", ".pyo"):
            continue
        if linked_path(path) or not path.resolve().is_relative_to(source):
            raise ValueError(f"Linked or external package entry is unsupported: {relative}")
        if path.is_file():
            files.append(path)
    for path in files:
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                parsed = urlsplit(target)
                if parsed.scheme in ("http", "https", "mailto"):
                    continue
                if parsed.scheme or parsed.netloc or "\\" in parsed.path:
                    raise ValueError(f"Unsupported package reference: {target}")
                if not parsed.path:
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve()
                if not resolved.is_relative_to(source) or not resolved.is_file():
                    raise ValueError(f"Missing or external package reference: {target}")
    return source, files


def install_skill(source, root, agent, scope="project", dry_run=False):
    source, files = package_files(source)
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Installation root must be an existing directory")
    relative = installation_relative(agent, scope, manifest_name(source))
    destination = root / relative
    current = root
    for part in relative.parts:
        current = current / part
        if linked_path(current):
            raise ValueError("Installation cannot traverse a symlink or junction")
    if not destination.resolve().is_relative_to(root):
        raise ValueError("Installation must stay inside the selected root")
    if destination.exists():
        raise ValueError("Skill destination already exists; preserve it and review upgrades explicitly")
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        raise ValueError("Source and installation destination must not contain one another")
    hashes = {path.relative_to(source).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation protects existing installs, including empty folders.
        destination.mkdir(exist_ok=False)
        for path in files:
            target = destination / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            if hashlib.sha256(target.read_bytes()).hexdigest() != hashes[path.relative_to(source).as_posix()]:
                raise OSError(f"Copied bytes differ; inspect the partial new installation at {destination}")
    return {
        "agent": agent, "scope": scope, "destination": str(destination),
        "dry_run": dry_run, "files_sha256": hashes,
        "status": "planned only" if dry_run else "copied and byte-verified; native host loading not implied",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    is_package = (PACKAGE / "SKILL.md").is_file()
    parser.add_argument("--skill", required=not is_package, help="Catalog skill name; required from the repository installer")
    parser.add_argument("--agent", choices=HOSTS, required=True)
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--root", type=Path, required=True, help="Existing project directory or explicitly chosen user home")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if is_package:
        if args.skill and args.skill != SKILL_NAME:
            parser.error("This package installer installs only its own skill")
        source = PACKAGE
    else:
        source = PACKAGE / "skills" / validate_name(args.skill)
        if linked_path(source):
            raise ValueError("Catalog source cannot be a symlink or junction")
    print(json.dumps(install_skill(source, args.root, args.agent, args.scope, args.dry_run), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"Installation failed: {error}. A newly created partial copy, if any, is left for inspection; no existing installation was replaced.", file=sys.stderr)
        sys.exit(1)
