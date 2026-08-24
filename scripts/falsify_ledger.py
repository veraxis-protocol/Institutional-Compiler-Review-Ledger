#!/usr/bin/env python3
"""Run bounded positive and negative Review Ledger cases in disposable copies."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(destination: Path) -> None:
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        dirs_exist_ok=True,
    )


def verify(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "verifier/ledger_core_verifier.py", "verify-all", *extra],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def expect(name: str, result: subprocess.CompletedProcess[str], code: int, fragment: str) -> None:
    combined = result.stdout + result.stderr
    if result.returncode != code or fragment not in combined:
        raise AssertionError(
            f"{name}: expected exit={code} containing {fragment!r}; "
            f"got exit={result.returncode}, output={combined!r}"
        )
    print(f"PASS {name}: exit={code} matched {fragment}")


def main() -> int:
    expect("valid ledger", verify(ROOT), 0, "MECHANICAL_VERIFICATION_PASS")

    with tempfile.TemporaryDirectory(prefix="ledger-path-") as temp:
        candidate = Path(temp) / "ledger"
        copy_repo(candidate)
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=candidate, text=True).strip()
        subprocess.run(["git", "switch", "-c", "evidence/falsification"], cwd=candidate, check=True, capture_output=True)
        with (candidate / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\nunauthorized implementer mutation\n")
        subprocess.run(["git", "add", "README.md"], cwd=candidate, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Falsification Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "fixture"],
            cwd=candidate,
            check=True,
            capture_output=True,
        )
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=candidate, text=True).strip()
        expect(
            "unauthorized path/role transition",
            verify(candidate, "--actor", "veraxis-protocol", "--branch", "evidence/falsification", "--base", base, "--head", head),
            1,
            "unauthorized paths for role IMPLEMENTER_EXECUTION",
        )

    with tempfile.TemporaryDirectory(prefix="ledger-manifest-") as temp:
        candidate = Path(temp) / "ledger"
        copy_repo(candidate)
        target = candidate / "stage-m1-closure/14-M1-CLOSURE-RETURN-FINAL.md"
        target.write_bytes(target.read_bytes() + b"\ntampered\n")
        expect("tampered manifest member", verify(candidate), 1, "byte mismatch")

    with tempfile.TemporaryDirectory(prefix="ledger-bootstrap-") as temp:
        candidate = Path(temp) / "ledger"
        copy_repo(candidate)
        policy_path = candidate / "policy/PATH-AUTHORITY.json"
        policy = json.loads(policy_path.read_text())
        policy["role_paths"]["BOOTSTRAP"] = ["bootstrap/**"]
        policy_path.write_text(json.dumps(policy, indent=2) + "\n")
        expect("retired BOOTSTRAP authority", verify(candidate), 1, "retired BOOTSTRAP authority is present")

    print("PASS bounded ledger falsification harness: 4/4 expected outcomes observed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

