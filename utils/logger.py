import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger('WhDashApp')
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler("error_log.txt", maxBytes=100000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
