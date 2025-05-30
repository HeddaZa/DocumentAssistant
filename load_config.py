from pathlib import Path
from typing import Any, cast

import yaml

from documentassistent.utils.logger import setup_logger

logger = setup_logger(name="ConfigLoader")


def load_config(config_path: str = "config.yaml") -> dict[str, Any]:
    """Load configuration from the YAML file."""
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
