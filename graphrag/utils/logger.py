import os
import sys

from loguru import logger
from loguru._logger import Logger


def setup_logger(
    name: str,
    log_file: str = "app.log",
) -> Logger:
    """Sets up a logger with the specified name, log file, and level.

    Args:
        name (str): Name of the logger (used in log messages).
        log_file (str): Path to the log file.
        default_level (str): Default logging level (DEBUG, INFO, WARNING, ERROR).

    Returns:
        logger: Configured logger instance.
    """
    log_level = os.getenv("LOG_LEVEL").upper()

    logger.remove()

    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> - "
            "<level>{level}</level> - "
            "<cyan>{name}</cyan> - "
            "<blue>{file}</blue> - "
            "<level>{message}</level>"
        ),
        filter=lambda record: record["extra"].get("name", "") == name,
        level=log_level,
    )

    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name} - {file} - {message}",
        filter=lambda record: record["extra"].get("name", "") == name,
        level=log_level,
        rotation="10 MB",
    )

    return logger.bind(name=name)
