import logging
from logging.handlers import RotatingFileHandler

def get_logger(name, format=None, level=None):
    # logger
    logger = logging.getLogger(name)  # it is creating an object of logger with name logging_advanced
    # logger = logging.getLogger(__name__) # it not going
    if level is not None:
        logger.setLevel(level)
    else:
        logger.setLevel(logging.DEBUG)
    # handler
    # file_handler = logging.FileHandler('custom_logfile.log', encoding='utf-8')
    rotating_file_handler = RotatingFileHandler('custom_logfile.log', maxBytes=600, backupCount=3)
    # logging.RotatingFileHandler(rotating_file_handler)

    # formatter
    if format is not None:
        formatter = logging.Formatter(format)
    else:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # file_handler.setFormatter(formatter)
    rotating_file_handler.setFormatter(formatter)

    # adding handler to logger object
    # logger.addHandler(file_handler)
    logger.addHandler(rotating_file_handler)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger