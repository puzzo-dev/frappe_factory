#!/usr/bin/env sh
# Conventional-commit commit-msg hook for Frappe Factory.
# Install: cp scripts/commit-msg-hook.sh .git/hooks/commit-msg && chmod +x .git/hooks/commit-msg

COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(head -n 1 "$COMMIT_MSG_FILE")

# Allow merge commits, revert commits, and version bump commits
case "$COMMIT_MSG" in
    Merge*|Revert*|"chore(release):"*)
        exit 0
        ;;
esac

# Allowed prefixes
if ! echo "$COMMIT_MSG" | grep -Eq '^(feat|feature|fix|bugfix|hotfix|security|docs|chore|style|refactor|test|tests|perf|ci|build)(\(.+\))?!?: .+'; then
    echo "ERROR: Commit message must use a conventional-commit prefix." >&2
    echo "" >&2
    echo "Allowed formats:" >&2
    echo "  feat: add new feature" >&2
    echo "  fix: correct broken hook" >&2
    echo "  docs: update README" >&2
    echo "  chore: clean up imports" >&2
    echo "" >&2
    echo "Your message:" >&2
    echo "  $COMMIT_MSG" >&2
    exit 1
fi

exit 0
