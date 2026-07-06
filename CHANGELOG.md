# Changelog

## 2026-07-06

### Added

- Migrated ChatTool's Lark bot helper core into ChatLark: `LarkBot`, `MessageContext`, message payload helpers, markdown/docx block helpers, `ChatSession`, `chatlark info/send/chat`, and `chatlark serve echo/ai/webhook`.
- Added optional `llm` extra for ChatTool-backed AI chat sessions while keeping the base ChatLark package free of a hard ChatTool dependency.

### Changed

- Bumped the package from placeholder `0.0.1` to first functional line `0.1.0`.
- Standardized CI and PyPI Trusted Publisher release workflow: publish now validates tag/version alignment, requires release runs to come from `main`, fails on duplicate PyPI versions, runs tests, builds distributions, and runs `twine check` before OIDC publishing.

## YYYY-MM-DD

### Added

### Changed

### Fixed
