#!/usr/bin/env python3
"""Materialize one offline skill case without exposing its grading criteria."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install import HOSTS, installation_relative


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(value, allow_instruction_paths=False):
    path = PurePosixPath(value)
    if not value or not path.parts or path.is_absolute() or ".." in path.parts or "\\" in value or ":" in value:
        raise ValueError(f"Unsafe fixture path: {value!r}")
    if not allow_instruction_paths and (
        path.parts[0] in (".agents", ".claude", ".copilot")
        or path.parts[:2] == (".github", "skills")
    ):
        raise ValueError("Fixture paths cannot replace the selected skill instructions")
    return path


def load_cases(path):
    corpus = json.loads(path.read_text(encoding="utf-8"))
    if corpus.get("schema_version") != 1:
        raise ValueError("Unsupported evaluation corpus version")
    seen = set()
    for case in corpus["cases"]:
        case_id = case["id"]
        if not case_id or case_id in seen or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in case_id):
            raise ValueError(f"Invalid or duplicate case ID: {case_id!r}")
        seen.add(case_id)
        if not case["request"].strip() or not case["checks"]["criteria"]:
            raise ValueError(f"Case needs a request and review criteria: {case_id}")
        for name, content in case["files"].items():
            safe_relative(name)
            if not isinstance(content, str):
                raise ValueError(f"Fixture content must be text: {name}")
        for name in case["checks"]["mutable_files"]:
            safe_relative(name)
            if name not in case["files"]:
                raise ValueError(f"Mutable file is absent from fixture: {name}")
        for prefix in case["checks"]["allowed_new_prefixes"]:
            safe_relative(prefix)
    return corpus


def prepare(corpus_path, case_id, skill, output, host="codex"):
    corpus = load_cases(corpus_path)
    selected = next((case for case in corpus["cases"] if case["id"] == case_id), None)
    if selected is None:
        raise ValueError(f"Unknown case: {case_id}")
    installed_relative = installation_relative(host)
    skill = skill.resolve(strict=True)
    output = output.resolve()
    if output.exists():
        raise ValueError("Output already exists; keep prior evidence and choose a fresh path")
    if output.is_relative_to(skill) or skill.is_relative_to(output):
        raise ValueError("Evaluation output and instruction source must not contain one another")
    # Copy only runtime instructions; the evaluator must not receive the rubric,
    # previous conclusions, other cases or a source baseline/candidate label.
    instruction_files = [skill / "SKILL.md"]
    # Preserve the applicable notice even in the reduced instruction snapshot.
    if (skill / "LICENSE").is_file():
        instruction_files.append(skill / "LICENSE")
    for directory in ("references", "agents"):
        if (skill / directory).is_dir():
            instruction_files.extend(sorted((skill / directory).rglob("*")))
    instruction_files = [path for path in instruction_files if path.is_file()]
    if not (skill / "SKILL.md").is_file():
        raise ValueError("Instruction source needs SKILL.md")
    if any(path.is_symlink() or not path.resolve().is_relative_to(skill) for path in instruction_files):
        raise ValueError("Instruction files must stay inside their package")
    workspace = output / "workspace"
    installed = workspace / installed_relative
    for source in instruction_files:
        target = installed / source.relative_to(skill)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    instruction_mapping = {}
    for name, content in selected["files"].items():
        original_path = safe_relative(name)
        if name == "AGENTS.md" and host != "codex":
            name = HOSTS[host]["instructions"]
            instruction_mapping[original_path.as_posix()] = name
        target = workspace.joinpath(*safe_relative(name).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    prompt = (
        f"Use {HOSTS[host]['invocation']} from "
        f"{installed_relative.as_posix()}/SKILL.md to complete this task.\n\n"
        + selected["request"]
        + "\n\nEvaluation environment: operate only in this isolated workspace. "
        "Use local files only; do not browse, use providers, install dependencies, "
        "access accounts or create commits. Record unavailable evidence honestly. "
        "Keep any evaluation handoff outside the workspace, in the sibling handoff.md.\n"
    )
    (output / "task.txt").write_text(prompt, encoding="utf-8", newline="\n")
    manifest = {
        "schema_version": 1,
        "case_id": case_id,
        "host_profile": host,
        "fixture_instruction_mapping": instruction_mapping,
        "package_scope": "instruction snapshot only; maintenance corpus/helpers withheld, not a complete package-installation test",
        "corpus_sha256": digest(corpus_path),
        "task_sha256": digest(output / "task.txt"),
        "instruction_sha256": {
            path.relative_to(skill).as_posix(): digest(path) for path in instruction_files
        },
        "initial_files_sha256": {
            path.relative_to(workspace).as_posix(): digest(path)
            for path in sorted(workspace.rglob("*")) if path.is_file()
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case")
    parser.add_argument("--skill", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--host", choices=HOSTS, default="codex")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    corpus_path = Path(__file__).with_name("cases.json")
    if args.validate:
        corpus = load_cases(corpus_path)
        print(f"Evaluation corpus valid: {len(corpus['cases'])} cases; no agent execution implied.")
        return
    if not args.case or not args.output:
        parser.error("--case and --output are required for preparation")
    print(prepare(corpus_path, args.case, args.skill, args.output, args.host))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Evaluation preparation failed: {error}", file=sys.stderr)
        sys.exit(1)
