from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT_ENV = "CAMERA_BASED_RGBWW_OPTIMIZER_DATA_ROOT"


def resolve_project_tmp_dir(
    env: Mapping[str, str] | None = None, *, platform: str | None = None,
) -> Path:
    values = os.environ if env is None else env
    override = values.get(DATA_ROOT_ENV)
    if override:
        return Path(override).expanduser()
    current_platform = os.name if platform is None else platform
    return Path("D:/rgbww-optimizer") if current_platform == "nt" else Path(
        "/Volumes/4T/temp/rgbww-optimizer"
    )


PROJECT_TMP_DIR = resolve_project_tmp_dir()
