"""
Configuration loading utilities.

This module provides backward-compatible config loading.
For new code, prefer using documentassistent.config.ConfigManager.
"""

from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import yaml

from documentassistent.utils.logger import setup_logger

logger = setup_logger(name="ConfigLoader")


@lru_cache(maxsize=1)
def load_config(config_path: str = "config.yaml") -> dict[str, Any]:
    """
    Load configuration from the YAML file (legacy function).

    For new code, use:
        from documentassistent.config import ConfigManager
        config = ConfigManager().load()

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Dictionary with configuration values
    """
    logger.info(
        "Loading configuration from {}",
        config_path,
    )
    try:
        with Path(config_path).open("r") as file:
            config = yaml.safe_load(file)
            typed_config = cast("dict[str, Any]", config)
            logger.debug(
                "Configuration loaded: {}",
                typed_config,
            )
            return typed_config
    except Exception:
        logger.exception("Failed to load configuration.")
        raise
