# logging_utils.py
import os
import time
import json
import logging
from config.config import LOG_FILE  # Import LOG_FILE from config

############################### Debug Logging ###############################

DEBUG = True
LOG_FILE = "/Users/nipsvanmctitsky/phonegod/local_debug.log"

# Ensure the log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

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
    log_file = "/Users/nipsvanmctitsky/phonegod/local_debug.log"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if structured_data:
        # Format structured data for logging
        formatted_data = json.dumps(structured_data, indent=4)
        log_message = f"{timestamp} DEBUG: {message}\n{formatted_data}"
    else:
        log_message = f"{timestamp} DEBUG: {message}"

    with open(log_file, "a") as log:
        log.write(log_message + "\n")

    print(log_message)  # Immediate feedback