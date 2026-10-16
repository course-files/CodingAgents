"""Check that a student's machine is ready for the Coding Agents lab.

Run with:  python check_setup.py
Works on Windows, Linux and macOS (no shell script, so no line-ending issues).
"""

from __future__ import annotations

import shutil
import subprocess
import sys


def version_of(command: list[str]) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (result.stdout or result.stderr).strip()
    return output.splitlines()[0] if output else None


def main() -> int:
    ok = True
    print("Coding Agents lab: setup check\n")

    if sys.version_info >= (3, 10):
        print(f"[ OK ] Python {sys.version.split()[0]}")
    else:
        ok = False
        print(f"[FAIL] Python 3.10 or newer is required (found {sys.version.split()[0]})")

    for name, command, required in [
        ("Git", ["git", "--version"], True),
        ("VS Code CLI", ["code", "--version"], False),
    ]:
        found = shutil.which(command[0]) and version_of(command)
        if found:
            print(f"[ OK ] {name}: {found}")
        elif required:
            ok = False
            print(f"[FAIL] {name} was not found on PATH")
        else:
            print(f"[WARN] {name} was not found on PATH (optional; see Step 1)")

    try:
        import pytest  # noqa: F401

        print(f"[ OK ] pytest {pytest.__version__}")
    except ImportError:
        ok = False
        print("[FAIL] pytest is not installed. Run: python -m pip install -r requirements.txt")

    print("\nAll required tools are present." if ok else "\nFix the FAIL items before Step 1.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
