# Changelog

## 2026-07-06

### Added

- Migrated ChatTool's Lark bot helper core into ChatLark: `LarkBot`, `MessageContext`, message payload helpers, markdown/docx block helpers, `ChatSession`, `chatlark info/send`, and `chatlark serve echo/webhook`.
- Added migration review tests for the non-model `LarkBot` method surface, ChatTool dependency decoupling, and ChatEnv Feishu config reuse.

### Changed

- Bumped the package from placeholder `0.0.1` to first functional line `0.1.0`, then to patch `0.1.1` for migration-boundary cleanup.
- Model-calling CLI surfaces are intentionally deferred; `chatlark chat`, `chatlark serve ai`, and the `chatlark[llm]` ChatTool optional extra were removed from the default package boundary.
- Standardized CI and PyPI Trusted Publisher release workflow: publish now validates tag/version alignment, requires release runs to come from `main`, fails on duplicate PyPI versions, runs tests, builds distributions, and runs `twine check` before OIDC publishing.

## YYYY-MM-DD

### Added

### Changed

### Fixed
