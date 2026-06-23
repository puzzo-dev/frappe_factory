#!/usr/bin/env sh
# Auto-prefix commit messages with a conventional-commit prefix.
# Install: cp scripts/prepare-commit-msg-hook.sh .git/hooks/prepare-commit-msg && chmod +x .git/hooks/prepare-commit-msg

COMMIT_MSG_FILE="$1"
COMMIT_SOURCE="$2"

# Do not overwrite merge commits, squash messages, or rebase messages
if [ -n "$COMMIT_SOURCE" ]; then
    exit 0
fi

# Only rewrite if Python is available
if command -v python3 >/dev/null 2>&1; then
    python3 scripts/suggest_commit_prefix.py --rewrite "$COMMIT_MSG_FILE"
fi

exit 0
