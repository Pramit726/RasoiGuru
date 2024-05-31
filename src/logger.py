import logging
import os
from datetime import datetime

# Define the log file name with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the path to the logs directory and create it if it doesn't exist
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

# Define the full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure basic logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Set the log file path
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Set the log message format
    level=logging.INFO,  # Set the logging level to INFO
)