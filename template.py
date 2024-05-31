import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

project_name = "RasoiGuru"

# List of files to be created
list_of_files = [
    "data/",
    "notebooks/experiment.ipynb",
    "src/__init__.py",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/data_ingestion.py",
    f"src/{project_name}/check_index.py",
    f"src/{project_name}/create_tools.py",
    f"src/{project_name}/generation.py",
    f"src/exception.py",
    f"src/logger.py",
    f"src/utils.py",
    ".env",
    ".gitignore",
    "README.md",
    "api.py",
    "requirements.txt",
    "setup.py"
]

# Loop through the list of files
for filepath in list_of_files:
    # Convert the filepath to a Path object
    filepath = Path(filepath)
    # Split the filepath into directory and filename
    filedir, filename = os.path.split(filepath)

    # Create directory if it doesn't exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    # Create empty file if it doesn't exist or if it's empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")