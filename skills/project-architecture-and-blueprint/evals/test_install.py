"""Exercise local host placement and file-integrity guarantees, without agents."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install import HOSTS, SKILL_NAME, install_skill, installation_relative


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="osmys-portability-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "reviewed source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text(
            f"---\nname: {SKILL_NAME}\ndescription: Fixture instructions\n---\n"
            "Read [details](references/details.md).\n", encoding="utf-8")
        (self.source / "references").mkdir()
        (self.source / "references/details.md").write_text("Exact UTF-8 reference: café\n", encoding="utf-8")
        (self.source / "agents").mkdir()
        (self.source / "agents/openai.yaml").write_text('interface:\n  display_name: "Optional UI"\n', encoding="utf-8")
        (self.source / "evals").mkdir()
        (self.source / "evals/README.md").write_text("Maintainer resources\n", encoding="utf-8")

    def test_exact_portable_copy_for_all_host_and_scope_profiles(self):
        expected = {p.relative_to(self.source): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        locations = {
            ("codex", "project"): ".agents/skills/project-architecture-and-blueprint",
            ("codex", "user"): ".agents/skills/project-architecture-and-blueprint",
            ("claude", "project"): ".claude/skills/project-architecture-and-blueprint",
            ("claude", "user"): ".claude/skills/project-architecture-and-blueprint",
            ("copilot", "project"): ".github/skills/project-architecture-and-blueprint",
            ("copilot", "user"): ".copilot/skills/project-architecture-and-blueprint",
        }
        for agent in HOSTS:
            for scope in ("project", "user"):
                with self.subTest(agent=agent, scope=scope):
                    target_root = self.root / f"target {agent} {scope}"
                    target_root.mkdir()
                    result = install_skill(self.source, target_root, agent, scope)
                    target = target_root / locations[(agent, scope)]
                    self.assertEqual(Path(result["destination"]), target)
                    self.assertEqual({p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}, expected)
                    self.assertTrue((target / "references/details.md").is_file())
                    self.assertFalse((target_root / "CLAUDE.md").exists())
                    self.assertFalse((target_root / ".github/copilot-instructions.md").exists())
        self.assertEqual({p.relative_to(self.source): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}, expected)

    def test_dry_run_writes_nothing(self):
        target_root = self.root / "project"
        target_root.mkdir()
        result = install_skill(self.source, target_root, "claude", dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(list(target_root.iterdir()), [])

    def test_existing_installation_and_config_are_preserved(self):
        target_root = self.root / "project"
        destination = target_root / installation_relative("copilot")
        destination.mkdir(parents=True)
        marker = destination / "custom.md"
        marker.write_bytes(b"existing customization")
        config = target_root / ".github/copilot-instructions.md"
        config.write_bytes(b"existing product instructions")
        for dry_run in (False, True):
            with self.assertRaises(ValueError):
                install_skill(self.source, target_root, "copilot", dry_run=dry_run)
        self.assertEqual(marker.read_bytes(), b"existing customization")
        self.assertEqual(config.read_bytes(), b"existing product instructions")
        self.assertFalse((destination / "SKILL.md").exists())

    def test_invalid_source_reference_fails_before_writes(self):
        target_root = self.root / "project"
        target_root.mkdir()
        manifest = self.source / "SKILL.md"
        manifest.write_text(manifest.read_text(encoding="utf-8") + "[missing](references/absent.md)\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            install_skill(self.source, target_root, "codex")
        self.assertEqual(list(target_root.iterdir()), [])

    def test_recursive_installation_is_rejected(self):
        with self.assertRaises(ValueError):
            install_skill(self.source, self.source, "codex")
        self.assertFalse((self.source / ".agents").exists())

    def test_unknown_host_and_missing_root_do_not_create_directories(self):
        with self.assertRaises(ValueError):
            install_skill(self.source, self.root, "unknown")
        missing = self.root / "missing"
        with self.assertRaises(FileNotFoundError):
            install_skill(self.source, missing, "claude")
        self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
