#!/usr/bin/env python3
"""Auto-versioning script for Frappe Factory.

Versioning scheme:
    MAJOR.MINOR.PATCH
    - MAJOR: new features (feat: / feature: commits)
    - MINOR: major fixes (fix: / bugfix: commits that are not trivial)
    - PATCH: minor fixes, docs, chores, tests, refactors

Usage:
    python scripts/bump_version.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INIT_FILE = ROOT / "frappe_factory" / "__init__.py"
HOOKS_FILE = ROOT / "frappe_factory" / "hooks.py"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"

VERSION_PATTERN = re.compile(r'__version__\s*=\s*"([^"]+)"')
APP_VERSION_PATTERN = re.compile(r'app_version\s*=\s*"([^"]+)"')

COMMIT_RULES = {
    "major": [
        r"^feat\b",
        r"^feature\b",
    ],
    "minor": [
        r"^fix\b",
        r"^bugfix\b",
        r"^hotfix\b",
        r"^security\b",
    ],
    "patch": [
        r"^docs\b",
        r"^chore\b",
        r"^style\b",
        r"^refactor\b",
        r"^test\b",
        r"^tests\b",
        r"^perf\b",
        r"^ci\b",
        r"^build\b",
    ],
}


def get_current_version() -> str:
    text = INIT_FILE.read_text()
    match = VERSION_PATTERN.search(text)
    if not match:
        raise RuntimeError(f"Could not find __version__ in {INIT_FILE}")
    return match.group(1)


def bump_version(current: str, level: str) -> str:
    major, minor, patch = map(int, current.split("."))
    if level == "major":
        major += 1
        minor = 0
        patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def get_commits_since_last_version(current: str) -> list[str]:
    """Return commit messages since the last tag matching the current version."""
    try:
        tag = f"v{current}"
        result = subprocess.run(
            ["git", "log", f"{tag}..HEAD", "--pretty=format:%s"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        # No tag yet; return all commits.
        result = subprocess.run(
            ["git", "log", "--pretty=format:%s"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def classify_bump(commits: list[str], strict: bool = False) -> str:
    """Return the highest bump level required by the commits.

    If strict=True, every commit must match a recognized conventional-commit prefix.
    """
    if not commits:
        return "patch"

    level = None
    invalid = []
    for commit in commits:
        lower = commit.lower()
        matched = False
        for rule in COMMIT_RULES["major"]:
            if re.search(rule, lower):
                return "major"
        for rule in COMMIT_RULES["minor"]:
            if re.search(rule, lower) and level in (None, "patch"):
                level = "minor"
                matched = True
        for rule in COMMIT_RULES["patch"]:
            if re.search(rule, lower) and level is None:
                level = "patch"
                matched = True
        if not matched:
            invalid.append(commit)

    if strict and invalid:
        print("ERROR: The following commits do not use a recognized conventional-commit prefix:")
        for commit in invalid:
            print(f"  - {commit}")
        print("Allowed prefixes: feat, feature, fix, bugfix, hotfix, security, docs, chore, style, refactor, test, tests, perf, ci, build")
        raise SystemExit(1)

    return level or "patch"


def update_version_files(new_version: str) -> None:
    # Update __init__.py
    text = INIT_FILE.read_text()
    updated = VERSION_PATTERN.sub(f'__version__ = "{new_version}"', text)
    INIT_FILE.write_text(updated)

    # Update hooks.py
    text = HOOKS_FILE.read_text()
    updated = APP_VERSION_PATTERN.sub(f'app_version = "{new_version}"', text)
    HOOKS_FILE.write_text(updated)


def update_changelog(new_version: str, commits: list[str], level: str) -> None:
    header = f"## [{new_version}] - {date.today().isoformat()}"
    body = f"\n\n### {'Feature' if level == 'major' else 'Major Fix' if level == 'minor' else 'Minor Fix'}\n\n"
    body += "\n".join(f"- {c}" for c in commits[:50]) or "- Maintenance update"

    if CHANGELOG_FILE.exists():
        existing = CHANGELOG_FILE.read_text()
    else:
        existing = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n"

    # Insert after the title/intro
    lines = existing.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("##"):
            insert_at = i
            break
        insert_at = i + 1

    lines.insert(insert_at, header + body)
    CHANGELOG_FILE.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Auto-version Frappe Factory")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without applying them")
    parser.add_argument("--level", choices=["major", "minor", "patch"], help="Force bump level")
    parser.add_argument("--strict", action="store_true", help="Require every commit to use a recognized conventional-commit prefix")
    args = parser.parse_args()

    current = get_current_version()
    commits = get_commits_since_last_version(current)
    level = args.level or classify_bump(commits, strict=args.strict)
    new_version = bump_version(current, level)

    print(f"Current version: {current}")
    print(f"Detected level:  {level}")
    print(f"New version:     {new_version}")
    print(f"Commits:         {len(commits)}")

    if args.dry_run:
        print("Dry run; no files modified.")
        return

    update_version_files(new_version)
    update_changelog(new_version, commits, level)
    print(f"Updated version to {new_version} in {INIT_FILE.name} and {HOOKS_FILE.name}")
    print(f"Updated {CHANGELOG_FILE.name}")
    print(f"Next step: git commit -am 'chore(release): v{new_version}' && git tag v{new_version}")


if __name__ == "__main__":
    main()
