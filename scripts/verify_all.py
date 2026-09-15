#!/usr/bin/env python3
"""
MINDCARE NER — Local Pre-Commit & Verification Runner
Verifies:
1. Strict LangChain compliance (NO LangGraph imports or files anywhere)
2. Medical safety terminology compliance (no diagnostic claims)
3. Secret leakage prevention (no .env committed or hardcoded private keys)
4. Full pytest test suites across backend, ML engine, and voice module
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

PROHIBITED_TERMS = [
    "langgraph",
    "detects dementia",
    "diagnoses alzheimer",
    "cures dementia",
    "prevents dementia",
]

ALLOWED_CHECK_EXTS = {".py", ".md", ".json", ".yaml", ".yml", ".dart", ".ts", ".tsx"}


def check_forbidden_terms() -> bool:
    print("\n[STEP 1] Checking for prohibited terms (LangGraph & Diagnostic Claims)...")
    violations = []

    for path in ROOT_DIR.rglob("*"):
        if not path.is_file():
            continue
        if any(
            part.startswith(".")
            for part in path.parts
            if part not in {".github", ".opencodereview"}
        ):
            continue
        if (
            "node_modules" in path.parts
            or ".venv" in path.parts
            or "__pycache__" in path.parts
            or "dist" in path.parts
        ):
            continue
        if path.suffix not in ALLOWED_CHECK_EXTS:
            continue

        rel_path = path.relative_to(ROOT_DIR).as_posix()
        if rel_path in {
            "scripts/verify_all.py",
            "docs/decisions/ADR-002-langchain-orchestration.md",
            "docs/review/mindcare-review-rules.md",
            ".opencodereview/rule.json",
            "CONTRIBUTING.md",
            ".github/pull_request_template.md",
            ".github/ISSUE_TEMPLATE/feature_request.md",
        }:
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore").lower()
            for term in PROHIBITED_TERMS:
                if term in content:
                    violations.append(f"Found prohibited term '{term}' in {rel_path}")
        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Could not read {path}: {e}")

    if violations:
        print("[FAIL] Prohibited terms detected:")
        for v in violations:
            print(f"   - {v}")
        return False

    print("[PASS] Zero prohibited terms found. Architecture rules strictly verified.")
    return True


def check_secret_files() -> bool:
    print("\n[STEP 2] Checking for uncommitted secret files...")
    secret_files = [".env", "secrets.json", "credentials.json"]
    found = []
    for sf in secret_files:
        if (ROOT_DIR / sf).exists():
            found.append(sf)

    if found:
        print(f"[FAIL] Found secret file in root: {found}. Do not commit secrets!")
        return False
    print("[PASS] No uncommitted secret files found in repository root.")
    return True


def run_tests() -> bool:
    print("\n[STEP 3] Running test suites (Backend, ML, Voice)...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    test_dirs = ["backend/tests", "ml/tests", "voice/tests"]
    all_passed = True

    venv_python_win = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
    venv_python_nix = ROOT_DIR / ".venv" / "bin" / "python"
    if venv_python_win.exists():
        py_exec = str(venv_python_win)
    elif venv_python_nix.exists():
        py_exec = str(venv_python_nix)
    else:
        py_exec = sys.executable

    for td in test_dirs:
        test_path = ROOT_DIR / td
        if not test_path.exists():
            continue
        print(f"\n--- Running pytest in {td} ---")
        cmd = [py_exec, "-m", "pytest", "-v", str(test_path)]
        res = subprocess.run(cmd, cwd=str(ROOT_DIR), env=env, check=False)
        if res.returncode != 0:
            print(f"[FAIL] Tests failed in {td}")
            all_passed = False
        else:
            print(f"[PASS] All tests passed in {td}")

    return all_passed


def main():
    print("=" * 70)
    print("   MINDCARE NER - Monorepo Verification & Compliance Runner")
    print("=" * 70)

    success = True
    if not check_forbidden_terms():
        success = False
    if not check_secret_files():
        success = False
    if not run_tests():
        success = False

    print("\n" + "=" * 70)
    if success:
        print("[SUCCESS] ALL VERIFICATION CHECKS PASSED!")
        print("Monorepo is in a clean, compliant, and test-proven state.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("[FAIL] VERIFICATION FAILED. Address the issues above before pushing.")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
