from src.logger import logging
from src.exception import CustomException
import sys
import time
from pathlib import Path

# Function to extract the final answer from the result
def extract_answer(result):
    try:
        result = str(result['output'])
        start_marker = "Final Answer:"
        start_index = result.find(start_marker)
        print(start_index)
        if start_index != -1:
            result = result[start_index + len(start_marker):].strip()
        else:
            result = ""

        logging.info("Successfully extracted final answer")
        return result

    except Exception as e:
        logging.error("Error in extracting final answer")
        raise CustomException(e, sys)

# Function to check if vectors exist in the index
def vector_exist(index_name, pc):
    try:
        index = pc.Index(index_name)
        # Wait a moment for connection
        time.sleep(1)
        if index.describe_index_stats()['total_vector_count'] == 0:
            logging.info("Vectors do not exist")
            return False
        else:
            logging.info("Vector already exists")
            return True

    except Exception as e:
        logging.info("Error checking vector existence")
        raise CustomException(e, sys)

# Function to get paths of PDF files
def get_paths():
    # Get the current working directory
    current_path = Path(__file__)

    # Get the parent directory of the current working directory
    parent_path = current_path.parent.parent

    # Construct the path to the 'data' directory located in the parent directory
    data_path = parent_path / 'data'

    pdf_files = []
    try:
        for file in data_path.iterdir():
            if file.is_file() and file.name.endswith('.pdf'):
                pdf_files.append(file)

        logging.info("Got the PDF file paths")

        return pdf_files

    except Exception as e:
        logging.info("Error occurred while getting the PDF file paths")
        raise CustomException(e, sys)
    

    


