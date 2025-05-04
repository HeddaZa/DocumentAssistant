import logging
import os
import sys


def setup_logger(name: str, log_file: str = "app.log", default_level: int = logging.INFO) -> logging.Logger:
    """Sets up a logger with the specified name, log file, and level."""
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, default_level)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create formatter without the extra field
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Add file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
