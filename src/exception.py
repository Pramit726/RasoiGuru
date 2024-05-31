import sys
from src.logger import logging

# Function to format error message with details
def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # Call the constructor of the base class (Exception)
        super().__init__(error_message)
        # Store the error message and details
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        # Return the error message when the exception is converted to a string
        return self.error_message



        