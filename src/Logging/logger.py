# src/Logging/logger.py

import logging
import os
from datetime import datetime

"""
Logger setup module to configure and return a consistent logger
across the entire AI Web Scraper project. Logs are stored in the /logs directory.
"""

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate log file with timestamp
LOG_FILE = f"{LOG_DIR}/scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logger
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Expose logger
logger = logging.getLogger(__name__)
