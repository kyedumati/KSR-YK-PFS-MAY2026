import logging

# logger
logger = logging.getLogger(__name__) # it is creating an object of logger with name logging_advanced
# logger = logging.getLogger(__name__) # it not going
logger.setLevel(logging.DEBUG)
# handler
# file_handler = logging.FileHandler('custom_logfile.log', encoding='utf-8')
rotating_file_handler = logging.handlers.RotatingFileHandler('custom_logfile.log', maxBytes=600, backupCount=3)
# formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)



# adding handler to logger object
logger.addHandler(file_handler)


# console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


logger.info("Expense added: 120rs tea")
logger.debug("adding expense")

