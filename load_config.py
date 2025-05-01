from pathlib import Path

import yaml


def load_config() -> dict:
    """Load configuration from the YAML file.

    Returns:
        dict: Parsed configuration as a dictionary.
    """
    with Path("config.yaml").open("w") as file:
        config = yaml.safe_load(file)
    return config
