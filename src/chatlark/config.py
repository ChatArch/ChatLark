"""ChatLark configuration helpers."""

from __future__ import annotations

from pathlib import Path

from chatenv import BaseEnvConfig, EnvStore, FeishuConfig, get_paths


def get_env_root() -> Path:
    """Return the canonical ChatArch typed-env directory."""
    return get_paths().envs_dir


def get_env_store() -> EnvStore:
    """Return ChatEnv's canonical typed-profile store."""
    return EnvStore(get_env_root())


__all__ = ["BaseEnvConfig", "FeishuConfig", "get_env_root", "get_env_store"]
