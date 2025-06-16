from __future__ import annotations

import os
import platform
from pathlib import Path

from deltav.config.errors import UnsupportedPlatformError

SUPPORTED_PLATFORMS = ['Linux', 'Darwin', 'Windows']


def expand_path(p: Path) -> Path:
    _p = os.path.expandvars(p)
    _p = os.path.expandvars(p)
    return Path(_p)


def get_current_platform() -> str:
    this_platform = platform.system()
    if this_platform not in SUPPORTED_PLATFORMS:
        raise UnsupportedPlatformError(f'Deltav does not support running on {this_platform}.')
    return this_platform


def get_default_config_paths() -> list[Path]:
    DEFAULT_CONFIG_PATHS: dict[str, list[Path]] = {
        'Linux': [
            Path('$XDG_CONFIG_HOME/deltav/config.toml'),
            Path('$HOME/.config/deltav/config.toml'),
            Path('$HOME/.deltav/config.toml'),
            Path('$HOME/deltav/config.toml'),
            Path('$HOME/deltav.toml'),
        ],
        'Darwin': [
            Path('$XDG_CONFIG_HOME/deltav/config.toml'),
            Path('$HOME/.config/deltav/config.toml'),
            Path('$HOME/.deltav/config.toml'),
            Path('$HOME/deltav/config.toml'),
            Path('$HOME/deltav.toml'),
        ],
        'Windows': [Path('')],
    }
    return [expand_path(p) for p in DEFAULT_CONFIG_PATHS[get_current_platform()]]


def get_default_log_path() -> Path:
    DEFAULT_LOG_DIRS: dict[str, Path] = {
        'Linux': Path('$HOME/.local/share/deltav'),
        'Darwin': Path('$HOME/.local/share/deltav'),
        'Windows': Path(''),
    }
    return expand_path(DEFAULT_LOG_DIRS[get_current_platform()])


def get_default_db_path() -> Path:
    DEFAULT_DB_DIRS: dict[str, Path] = {
        'Linux': Path('$HOME/.local/state/deltav'),
        'Darwin': Path('$HOME/.local/state/deltav'),
        'Windows': Path(''),
    }
    return expand_path(DEFAULT_DB_DIRS[get_current_platform()])
