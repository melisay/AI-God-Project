import os
import json
import time
import hashlib
import logging
from threading import Lock

# Constants
BASE_DIR = "/Users/nipsvanmctitsky/phonegod"
CACHE_DIR = f"{BASE_DIR}/static/cached_responses"
LOG_FILE = f"{BASE_DIR}/app_debug.log"
MAX_CACHE_SIZE = 100  # Limit to 100 items

# Ensure directories exist
os.makedirs(CACHE_DIR, exist_ok=True)

# Global state
cache_lock = Lock()
chatgpt_cache = {}

# Create a logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# File handler to write logs to a file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

# Console handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def debug_log(message, structured_data=None):
    """
    Logs messages and optionally structures data like JSON.
    Args:
        message (str): The primary log message.
        structured_data (dict): Additional structured data to log as JSON.
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if structured_data:
        # Format structured data for logging
        formatted_data = json.dumps(structured_data, indent=4)
        log_message = f"{timestamp} DEBUG: {message}\n{formatted_data}"
    else:
        log_message = f"{timestamp} DEBUG: {message}"

    with open(LOG_FILE, "a") as log:
        log.write(log_message + "\n")

    print(log_message)  # Immediate feedback

def set_cache(key, value):
    """
    Sets a value in the cache, respecting the cache size limit.
    """
    with cache_lock:
        if len(chatgpt_cache) >= MAX_CACHE_SIZE:
            # Remove the oldest item (FIFO eviction)
            chatgpt_cache.pop(next(iter(chatgpt_cache)))
        chatgpt_cache[key] = value
