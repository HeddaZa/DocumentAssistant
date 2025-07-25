from documentassistent.utils.logger import setup_logger


def test_logger_setup() -> None:
    logger = setup_logger(name="TestLogger", log_file="logs/test.log")
    assert logger is not None
