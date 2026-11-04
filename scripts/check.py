"""Run the offline checks for every discovered skill; no model or network calls."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    subprocess.run([sys.executable, "-B", str(ROOT / "scripts/verify.py")], check=True)
    for skill in sorted((ROOT / "skills").iterdir()):
        if not skill.is_dir():
            continue
        print(f"Checking {skill.name}", flush=True)
        for script, arguments in (("prepare.py", ["--validate"]), ("test_prepare.py", []), ("test_install.py", [])):
            subprocess.run([sys.executable, "-B", str(skill / "evals" / script), *arguments], check=True, cwd=ROOT)
    subprocess.run([sys.executable, "-B", str(ROOT / "scripts/test_catalog.py")], check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
