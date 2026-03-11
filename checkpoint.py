import os
import logging
logger=logging.getLogger(__name__)
def save_checkpoint(page, file_path):
    with open(file_path, 'w') as f:
        f.write(str(page))
def load_checkpoint(file_path):
    if not os.path.exists(file_path):
        logger.info("No checkpoint file found. Starting from the first page.")
        return 1
    with open(file_path, 'r') as f:
        page= f.read().strip()
        return int(page)+1 if page.isdigit() else 1
    
    