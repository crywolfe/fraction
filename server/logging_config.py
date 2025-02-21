import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # # Create a rotating file handler for detailed logs
    # file_handler = RotatingFileHandler(
    #     os.path.join(log_dir, 'llm_generation.log'),
    #     maxBytes=10*1024*1024,  # 10 MB
    #     backupCount=5
    # )
    # file_handler.setLevel(logging.INFO)
    # file_handler.setFormatter(logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # ))

    # Add the file handler to the root logger
    # logging.getLogger().addHandler(file_handler)

    return logging.getLogger(__name__)

# Create a logger for this module
logger = setup_logging()