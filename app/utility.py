import logging

from services.database_manager import DatabaseManager

db = DatabaseManager("database.json")

# Configure logging
log_file = 'cn_manager.log'
log_level = logging.INFO
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Create a file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)

# Create a formatter
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)