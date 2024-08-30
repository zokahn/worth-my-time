import logging
import os
from logging.handlers import RotatingFileHandler
from src.rag_agent.config import config

LOG_DIR = config.get('LOG_DIR')
LOG_LEVEL = config.get('LOG_LEVEL')

def configure_logging():
    log_file = os.path.join(LOG_DIR, 'rag_agent.log')
    os.makedirs(LOG_DIR, exist_ok=True)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger('rag_agent')
    logger.setLevel(getattr(logging, LOG_LEVEL))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = configure_logging()
