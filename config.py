import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# Scraping configuration
WIKIPEDIA_BASE_URL = 'https://en.wikipedia.org'
MAX_ARTICLES = 5
DELAY_BETWEEN_REQUESTS = 1  # seconds

# File paths
DATA_DIR = 'data'
LOGS_DIR = 'logs'
