import logging
import os

def setup_logging():

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "application.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove handlers antigos
    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    date_format = "%d/%m/%Y %H:%M"
    formatter = logging.Formatter(
        fmt=log_format,
        datefmt=date_format
    )

    # =========================
    # Handler para arquivo
    # =========================
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


# ============================================
# CRIA O LOGGER GLOBAL PARA IMPORT
# ============================================
# Executa a configuração automaticamente
logger = setup_logging()