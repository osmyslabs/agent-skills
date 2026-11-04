"""Offline integrity checks for fixture preparation, not behavioral skill evals."""

import json
from pathlib import Path
import tempfile
import unittest

from prepare import prepare
from inspect_run import inspect_run
from install import SKILL_NAME


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="osmys-eval-helper-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skill = self.root / "instructions"
        self.skill.mkdir()
        (self.skill / "SKILL.md").write_text(f"---\nname: {SKILL_NAME}\ndescription: Fixture instructions\n---\nSelected instruction snapshot\n", encoding="utf-8")
        (self.skill / "LICENSE").write_bytes(b"Fixture license notice\n")
        (self.skill / "references").mkdir()
        (self.skill / "references/guide.md").write_text("Conditional reference\n", encoding="utf-8")
        (self.skill / "evals").mkdir()
        (self.skill / "evals/private.json").write_text('{"answer": "withheld"}', encoding="utf-8")
        self.corpus = self.root / "cases.json"
        self.case = {
            "id": "example",
            "request": "Review this synthetic input.",
            "files": {"docs/input.txt": "Exact fixture bytes: café\n"},
            "checks": {"mutable_files": [], "allowed_new_prefixes": ["docs/"], "criteria": ["Private expected result"]},
        }
        self.write_corpus()

    def write_corpus(self):
        self.corpus.write_text(json.dumps({"schema_version": 1, "cases": [self.case]}), encoding="utf-8")

    def test_exact_inputs_and_selected_instructions_without_case_rubric(self):
        original = (self.skill / "SKILL.md").read_bytes()
        result = prepare(self.corpus, "example", self.skill, self.root / "run")
        workspace = result / "workspace"
        self.assertEqual((workspace / "docs/input.txt").read_bytes(), self.case["files"]["docs/input.txt"].encode("utf-8"))
        installed = workspace / f".agents/skills/{SKILL_NAME}"
        self.assertEqual((installed / "SKILL.md").read_bytes(), original)
        self.assertEqual((installed / "LICENSE").read_bytes(), (self.skill / "LICENSE").read_bytes())
        self.assertTrue((installed / "references/guide.md").is_file())
        self.assertFalse((installed / "evals").exists())
        manifest = json.loads((result / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["initial_files_sha256"]), {
            "docs/input.txt", f".agents/skills/{SKILL_NAME}/SKILL.md",
            f".agents/skills/{SKILL_NAME}/LICENSE",
            f".agents/skills/{SKILL_NAME}/references/guide.md",
        })
        for path in result.rglob("*"):
            if path.is_file():
                self.assertNotIn("Private expected result", path.read_text(encoding="utf-8"))
        self.assertEqual((self.skill / "SKILL.md").read_bytes(), original)
        self.assertTrue(inspect_run(result, self.corpus)["workspace_effect_check_passed"])
        (installed / "SKILL.md").write_text("Unauthorized instruction change\n", encoding="utf-8")
        inspection = inspect_run(result, self.corpus)
        self.assertFalse(inspection["workspace_effect_check_passed"])
        self.assertIn(f".agents/skills/{SKILL_NAME}/SKILL.md", inspection["forbidden_effects"])

    def test_existing_output_is_preserved(self):
        output = self.root / "prior-run"
        output.mkdir()
        sentinel = output / "evidence.txt"
        sentinel.write_bytes(b"prior evidence")
        with self.assertRaises(ValueError):
            prepare(self.corpus, "example", self.skill, output)
        self.assertEqual(sentinel.read_bytes(), b"prior evidence")
        self.assertEqual(list(output.iterdir()), [sentinel])

    def test_fixture_cannot_escape_workspace(self):
        sentinel = self.root / "outside.txt"
        sentinel.write_bytes(b"protected")
        for unsafe in ("../../outside.txt", "/absolute.txt", "X:/outside.txt", "..\\outside.txt", f".agents/skills/{SKILL_NAME}/SKILL.md"):
            with self.subTest(path=unsafe):
                self.case["files"] = {unsafe: "replace"}
                self.write_corpus()
                with self.assertRaises(ValueError):
                    prepare(self.corpus, "example", self.skill, self.root / "rejected-run")
                self.assertFalse((self.root / "rejected-run").exists())
                self.assertEqual(sentinel.read_bytes(), b"protected")

    def test_run_cannot_be_nested_inside_instruction_source(self):
        with self.assertRaises(ValueError):
            prepare(self.corpus, "example", self.skill, self.skill / "recursive-copy")
        self.assertFalse((self.skill / "recursive-copy").exists())

    def test_native_profiles_keep_instruction_bytes_and_protect_the_loaded_skill(self):
        self.case["files"]["AGENTS.md"] = "Read docs/input.txt; output only documentation.\n"
        self.write_corpus()
        expected = {
            "codex": (f".agents/skills/{SKILL_NAME}", "AGENTS.md", f"${SKILL_NAME}"),
            "claude": (f".claude/skills/{SKILL_NAME}", "CLAUDE.md", f"/{SKILL_NAME}"),
            "copilot": (f".github/skills/{SKILL_NAME}", ".github/copilot-instructions.md", f"Use {SKILL_NAME}"),
        }
        for host, (location, instructions, invocation) in expected.items():
            with self.subTest(host=host):
                run = prepare(self.corpus, "example", self.skill, self.root / host, host)
                workspace = run / "workspace"
                self.assertEqual((workspace / instructions).read_text(encoding="utf-8"), self.case["files"]["AGENTS.md"])
                if host != "codex":
                    self.assertFalse((workspace / "AGENTS.md").exists())
                self.assertIn(invocation, (run / "task.txt").read_text(encoding="utf-8"))
                self.assertTrue(inspect_run(run, self.corpus)["workspace_effect_check_passed"])
                installed = workspace / location / "SKILL.md"
                installed.write_text("Unauthorized edit\n", encoding="utf-8")
                check = inspect_run(run, self.corpus)
                self.assertIn(f"{location}/SKILL.md", check["forbidden_effects"])

    def test_fixture_cannot_replace_any_host_skill_location(self):
        for unsafe in (".claude/skills/fake/SKILL.md", ".copilot/skills/fake/SKILL.md", ".github/skills/fake/SKILL.md"):
            with self.subTest(path=unsafe):
                self.case["files"] = {unsafe: "replacement"}
                self.write_corpus()
                with self.assertRaises(ValueError):
                    prepare(self.corpus, "example", self.skill, self.root / "unsafe", "claude")
                self.assertFalse((self.root / "unsafe").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
