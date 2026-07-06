"""ChatLark configuration helpers."""

from __future__ import annotations

from pathlib import Path

from chatenv import BaseEnvConfig, get_paths
from chatenv.configs import FeishuConfig


def get_env_root() -> Path:
    """Return the canonical ChatArch typed-env directory."""
    return get_paths().envs_dir


__all__ = ["BaseEnvConfig", "FeishuConfig", "get_env_root"]
