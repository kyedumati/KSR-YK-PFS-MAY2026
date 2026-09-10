import logging

logging.basicConfig(filename='logs/logfile.log', filemode="w", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler = logging.FileHandler(filename='logfile.log', encoding='utf-8')
# file_handler.setFormatter(formatter)



# logging.basicConfig()

# logging.debug("This is a debug message")
# logging.info("Hello World")
# logging.warning("Hello World")
# logging.error("Hello World")
# logging.critical("Hello World")

logging.info("Expense added: 120rs tea")
logging.error("Cound not read expense csv files")