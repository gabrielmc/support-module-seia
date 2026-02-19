import logging
import os

def setup_logging():

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "application.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove handlers antigos (evita duplicação)
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
