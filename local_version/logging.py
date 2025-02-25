import os
import time
import json
import logging
from .config import DEBUG, LOG_FILE

# Ensure the log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "a").close()

# Create a logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

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

# Prevent duplicate handlers
if not logger.hasHandlers():
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
        try:
            formatted_data = json.dumps(structured_data, indent=4)
            log_message = f"{timestamp} DEBUG: {message}\n{formatted_data}"
        except Exception as e:
            log_message = f"{timestamp} DEBUG: {message} (Structured data logging failed: {e})"
    else:
        log_message = f"{timestamp} DEBUG: {message}"

    with open(LOG_FILE, "a") as log:
        log.write(log_message + "\n")

    print(log_message)  # Immediate feedback
