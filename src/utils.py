import time
import logging
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_filename = f"logs/scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def safe_request_delay(delay=1):
    """Add delay between requests to be respectful"""
    time.sleep(delay)

def ensure_data_directory():
    """Ensure data directory exists"""
    if not os.path.exists('data'):
        os.makedirs('data')
