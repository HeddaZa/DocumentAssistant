from pathlib import Path

import yaml

from graphrag.utils.logger import setup_logger

logger = setup_logger(name="ConfigLoader")


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from the YAML file."""
    logger.info("Loading configuration from %s", config_path)
    try:
        with Path(config_path).open("r") as file:
            config = yaml.safe_load(file)
            logger.debug("Configuration loaded: %s", config)
            return config
    except Exception:
        logger.exception("Failed to load configuration.")
        raise
