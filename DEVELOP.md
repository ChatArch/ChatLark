# Development Guide

## CLI Rules

- Use `chatstyle>=0.1.0,<0.2.0` and `chatenv>=0.2.0,<0.3.0` as the canonical CLI interaction runtime.
- Prefer `CommandSchema`, `CommandField`, `add_interactive_option()`, and `resolve_command_inputs()` for new commands.
- Missing required args should auto-enter interactive mode when recoverable.
- `-i` forces interactive mode; `-I` disables prompting and must fail fast.
- Prompt defaults must match actual execution defaults.
- Sensitive values must stay masked in prompts and summaries.
- Prefer lazy imports in CLI wiring and keep implementation imports local when possible.

## Docs and Tests

- Use doc-first CLI testing.
- Put real CLI coverage under `tests/cli-tests/`.
- Put mock/fake CLI coverage under `tests/mock-cli-tests/`.
- Keep `README.md`, `docs/`, and `CHANGELOG.md` in sync with user-facing changes.

## Automation

- Keep automation small and reviewable.
- Prefer commands that can run in CI without interactive prompts.
- Ensure generated defaults are safe for local development.

## Release Workflow

- Release through `.github/workflows/publish.yml` using PyPI Trusted Publisher/OIDC; do not commit PyPI tokens or configure password-based uploads.
- Tag releases from commits already contained in `origin/main`, using `v<package-version>` where `<package-version>` matches `src/chatlark/__init__.py`.
- Manual publish runs must also be dispatched from `main`.
- The publish workflow must run tests, build the distribution, and run `twine check` before invoking `pypa/gh-action-pypi-publish`.
- If the package version already exists on PyPI, bump the version before publishing; the workflow should fail instead of silently skipping the upload.
- The current PyPI Publisher for `ChatArch/ChatLark` is configured with workflow `publish.yml` and environment `(Any)`, so the workflow intentionally does not set a GitHub `environment` claim.
