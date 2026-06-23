#!/usr/bin/env python3
"""Suggest or auto-apply a Conventional Commit prefix based on staged changes.

Usage:
    # Print suggested prefix for staged changes
    python scripts/suggest_commit_prefix.py

    # Auto-prefix the current commit message file (used by prepare-commit-msg hook)
    python scripts/suggest_commit_prefix.py --rewrite <commit-msg-file>

Rules:
    - New DocTypes / new API endpoints / new pages      -> feat
    - Test files or test changes                        -> test
    - README, CHANGELOG, CONTRIBUTING, docs             -> docs
    - .github/workflows, .pre-commit-config.yaml        -> ci
    - Version/changelog bumps, release scripts            -> chore
    - Changes to existing logic with bug keywords         -> fix
    - Code restructuring without behavior change          -> refactor
    - Formatting / linting only                         -> style
    - Anything else                                       -> chore
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BUG_KEYWORDS = [
    "fix", "bug", "repair", "correct", "resolve", "broken", "crash", "error",
    "exception", "fail", "failure", "invalid", "missing", "wrong", "patch",
]

REFACTOR_KEYWORDS = [
    "refactor", "restructure", "rename", "move", "extract", "simplify",
    "clean up", "cleanup", "decouple",
]

STYLE_KEYWORDS = [
    "format", "lint", "whitespace", "trailing", "black", "isort", "style",
]

PERF_KEYWORDS = [
    "performance", "optimize", "cache", "speed", "faster", "slow",
]


def get_staged_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


def get_staged_diff() -> str:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--no-ext-diff"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.lower()
    except subprocess.CalledProcessError:
        return ""


def classify_prefix(files: list[str], diff: str) -> str:
    # Test files first
    if any(re.search(r"test_.*\.py$|tests?/", f) for f in files):
        return "test"

    # CI / GitHub Actions
    if any(f.startswith(".github/") or f in {".pre-commit-config.yaml", ".gitignore"} for f in files):
        return "ci"

    # Docs
    if any(
        f.lower().endswith((".md", ".rst", ".txt"))
        or f.lower() in {"readme", "changelog", "contributing"}
        for f in files
    ):
        return "docs"

    # Versioning / release scripts
    if any(f in {"scripts/bump_version.py", "scripts/commit-msg-hook.sh", "scripts/suggest_commit_prefix.py"} for f in files):
        return "chore"

    # Style-only
    if any(k in diff for k in STYLE_KEYWORDS):
        return "style"

    # Performance
    if any(k in diff for k in PERF_KEYWORDS):
        return "perf"

    # Refactor
    if any(k in diff for k in REFACTOR_KEYWORDS):
        return "refactor"

    # Bug fix
    if any(k in diff for k in BUG_KEYWORDS):
        return "fix"

    # New files / features (heuristic)
    if any(f.startswith(("frappe_factory/", "frappe_factory/frappe_factory/")) and f.endswith(".json") for f in files):
        return "feat"
    if any(f.startswith("frappe_factory/frappe_factory/page/") for f in files):
        return "feat"
    if any(f.startswith("frappe_factory/frappe_factory/doctype/") and f.endswith(".json") for f in files):
        return "feat"

    # Default
    return "chore"


def rewrite_message(prefix: str, commit_msg_file: Path) -> None:
    text = commit_msg_file.read_text()
    lines = text.splitlines()
    if not lines:
        first = ""
        rest = []
    else:
        first = lines[0]
        rest = lines[1:]

    # Skip if already prefixed or is a special commit
    if re.match(r"^(feat|feature|fix|bugfix|hotfix|security|docs|chore|style|refactor|test|tests|perf|ci|build)(\(.+\))?!?: ", first):
        return
    if first.startswith(("Merge ", "Revert ", "chore(release):")):
        return
    if not first.strip():
        first = f"{prefix}: update"
    else:
        first = f"{prefix}: {first[0].lower()}{first[1:]}"

    commit_msg_file.write_text("\n".join([first] + rest) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Suggest or apply a conventional commit prefix")
    parser.add_argument("--rewrite", type=Path, help="Commit message file to rewrite")
    parser.add_argument("--strict", action="store_true", help="Exit with error if no staged changes")
    args = parser.parse_args()

    files = get_staged_files()
    diff = get_staged_diff()

    if not files and args.strict:
        print("ERROR: No staged changes found.")
        raise SystemExit(1)

    if not files:
        print("No staged changes found; default prefix: chore")
        prefix = "chore"
    else:
        prefix = classify_prefix(files, diff)

    print(f"Suggested prefix: {prefix}")
    if args.rewrite:
        rewrite_message(prefix, args.rewrite)
        print(f"Rewrote {args.rewrite} with prefix '{prefix}'")


if __name__ == "__main__":
    main()
