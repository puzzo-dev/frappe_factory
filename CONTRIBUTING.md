# Contributing to Frappe Factory

## Conventional Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/) to drive automatic versioning.

**Every commit message must start with a recognized prefix.** The commit-msg hook and CI will reject untagged commits.

### Allowed prefixes

| Prefix | Version bump | Use for |
|--------|-------------|---------|
| `feat:` | MAJOR | New features |
| `feature:` | MAJOR | New features (alias) |
| `fix:` | MINOR | Bug fixes |
| `bugfix:` | MINOR | Bug fixes (alias) |
| `hotfix:` | MINOR | Urgent fixes |
| `security:` | MINOR | Security fixes |
| `docs:` | PATCH | Documentation |
| `chore:` | PATCH | Maintenance |
| `style:` | PATCH | Formatting |
| `refactor:` | PATCH | Code refactoring |
| `test:` / `tests:` | PATCH | Tests |
| `perf:` | PATCH | Performance |
| `ci:` | PATCH | CI/CD |
| `build:` | PATCH | Build system |

### Examples

```bash
git commit -m "feat: add real-time plant floor renderer"
git commit -m "fix: correct telemetry timestamp parsing"
git commit -m "docs: update ThingsBoard webhook setup"
git commit -m "test: add sync API validation cases"
```

### Install the hooks

Auto-prefix + validate:

```bash
cp scripts/prepare-commit-msg-hook.sh .git/hooks/prepare-commit-msg
chmod +x .git/hooks/prepare-commit-msg

cp scripts/commit-msg-hook.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

Or use pre-commit:

```bash
pip install pre-commit
pre-commit install --hook-type prepare-commit-msg
pre-commit install --hook-type commit-msg
```

The `prepare-commit-msg` hook will analyze your staged changes and auto-prefix the commit message for you. The `commit-msg` hook will reject any message that still lacks a valid prefix.

To preview the suggested prefix without committing:

```bash
python scripts/suggest_commit_prefix.py
```

## Versioning

- `MAJOR.MINOR.PATCH`
- **MAJOR**: new features
- **MINOR**: major fixes
- **PATCH**: minor fixes, docs, tests, chores

To bump locally:

```bash
python scripts/bump_version.py --strict
```

## Pull Request Process

1. Branch from `develop`.
2. Use conventional commits for every commit.
3. Add or update tests for logic changes.
4. Ensure `bench --site <site> run-tests --app frappe_factory` passes.
5. Open a PR against `develop`.

## Code Style

- Python: Black, line length 120.
- Imports: isort with Black profile.
- Frappe DocType JSON: keep field order stable.
