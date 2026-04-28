import logging
import os
import sys

# ============================================
# CONFIGURAÇÃO DO LOGGER GLOBAL
# ============================================

def setup_logging():
    """Configura o sistema de logging da aplicação."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "application.log")

    # Cria logger principal
    logger = logging.getLogger("module-seia")
    logger.setLevel(logging.DEBUG)

    # Remove handlers antigos se existirem
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formato do log
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    date_format = "%d/%m/%Y %H:%M:%S"
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para console (para ver logs no terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# ============================================
# CRIA O LOGGER GLOBAL (executa na importação)
# ============================================
logger = setup_logging()
