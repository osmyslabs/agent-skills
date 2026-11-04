"""Exercise multi-package installation and the repository CLI, without agents."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from install import install_skill, HOSTS

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())


class CatalogTests(unittest.TestCase):
    def test_complete_packages_coexist_in_all_host_scopes(self):
        with tempfile.TemporaryDirectory(prefix="osmys-catalog-") as temporary:
            for host in HOSTS:
                for scope in ("project", "user"):
                    root = Path(temporary) / f"{host}-{scope}"
                    root.mkdir()
                    for source in SKILLS:
                        with self.subTest(host=host, scope=scope, skill=source.name):
                            result = install_skill(source, root, host, scope)
                            target = Path(result["destination"])
                            self.assertEqual(target.name, source.name)
                            expected = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
                            actual = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
                            self.assertEqual(actual, expected)
                            self.assertEqual((target / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
                            if host == "codex" and scope == "project":
                                standalone = Path(temporary) / f"standalone-{source.name}"
                                standalone.mkdir()
                                command = [sys.executable, "-B", str(target / "scripts/install.py"), "--agent", "claude", "--root", str(standalone), "--dry-run"]
                                planned = json.loads(subprocess.run(command, capture_output=True, text=True, check=True).stdout)
                                self.assertEqual(Path(planned["destination"]).name, source.name)
                                self.assertTrue(planned["dry_run"])
                                self.assertEqual(list(standalone.iterdir()), [])
                    self.assertEqual(len(list((root / HOSTS[host][scope]).iterdir())), len(SKILLS))

    def test_cli_selects_only_the_requested_skill_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="osmys-cli-") as temporary:
            source = SKILLS[-1]
            command = [sys.executable, "-B", str(ROOT / "scripts/install.py"), "--skill", source.name, "--agent", "codex", "--root", temporary]
            dry = subprocess.run([*command, "--dry-run"], capture_output=True, text=True, check=True)
            self.assertTrue(json.loads(dry.stdout)["dry_run"])
            self.assertEqual(list(Path(temporary).iterdir()), [])
            copied = subprocess.run(command, capture_output=True, text=True, check=True)
            target = Path(json.loads(copied.stdout)["destination"])
            self.assertEqual(target.name, source.name)
            self.assertEqual(len(list(target.parent.iterdir())), 1)
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)

    def test_cli_rejects_path_names_before_creating_destinations(self):
        with tempfile.TemporaryDirectory(prefix="osmys-cli-reject-") as temporary:
            for name in ("../outside", "UPPER", "a/b", "a--b"):
                command = [sys.executable, "-B", str(ROOT / "scripts/install.py"), "--skill", name, "--agent", "codex", "--root", temporary]
                self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(list(Path(temporary).iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
