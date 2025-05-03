import logging
import os


def setup_logger(name: str, log_file: str = "app.log", default_level: int = logging.INFO) -> logging.Logger:
    """Sets up a logger with the specified name, log file, and level.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        default_level (int): Default logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, default_level)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger
