"""Utility for loading prompts from YAML configuration files."""

from functools import cache
from pathlib import Path
from typing import Any, cast

import yaml

from documentassistent.exceptions import PromptLoadError, ThisFileNotFoundError
from documentassistent.utils.logger import setup_logger

logger = setup_logger(name="PromptLoader", log_file="logs/prompt_loader.log")


@cache
def load_prompt_config(prompt_name: str) -> dict[str, Any]:
    """Load a prompt configuration from YAML file."""
    prompt_path = Path(__file__).parent / f"{prompt_name}.yaml"

    if not prompt_path.exists():
        msg = f"Prompt file not found: {prompt_path}"
        logger.error(msg)
        raise ThisFileNotFoundError(msg)

    try:
        with prompt_path.open() as f:
            config = yaml.safe_load(f)
            logger.debug(
                "Loaded prompt configuration, {}: {}",
                prompt_name,
                config.get("version"),
            )
            return cast("dict[str, Any]", config)
    except Exception as e:
        msg = f"Failed to load prompt {prompt_name}: {e}"
        logger.exception(msg)
        raise PromptLoadError(msg) from e


def get_prompt(prompt_name: str, **kwargs: Any) -> str:
    """Get a formatted prompt string."""
    config = load_prompt_config(prompt_name)

    # Build the full prompt
    prompt_parts = []

    if "system" in config:
        prompt_parts.append(config["system"])

    if "user_template" in config:
        user_text = config["user_template"].format(**kwargs)
        prompt_parts.append(user_text)

    prompt = "\n".join(prompt_parts)

    logger.debug("Generated prompt '{}' with length {}", prompt_name, len(prompt))

    return prompt
