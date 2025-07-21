from documentassistent.utils.logger import setup_logger
from load_config import load_config

logger = setup_logger(
    name="InvoiceAgent",
    log_file="logs/invoice_agent.log",
)
CONFIG = load_config("config.yaml")

logger.info("InvoiceAgent initialized with configuration", extra={"config": CONFIG})
