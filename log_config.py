import logging
from logging.handlers import RotatingFileHandler
import os
folder_path = 'logs'
file_path = os.path.join(folder_path, 'scraper.log')

def setup_logging():
    # Ensure the logs directory exists
    os.makedirs(folder_path, exist_ok=True)
    # Configure logging 
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create handlers for both console and file output
    console_handler=logging.StreamHandler()
    file_handler=RotatingFileHandler(file_path, maxBytes=5*1024*1024, backupCount=5)
    # Set a common formatter for both handlers
    formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    # Apply the formatter to both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    # Set different logging levels for console and file handlers
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)