import sys
import os
from networksecurity.logging import logger


print(os.getcwd())


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error Occured in Python Script: [{self.file_name}] on line number: [{self.lineno}] with error message: [{str(self.error_message)}]"




# if __name__ == "__main__":
#     try:
#         logger.logging.info("Entering the TRY Block")
#         a = 1/0
#     except Exception as e:
#         logger.logging.info(NetworkSecurityException(e, sys))
#         raise NetworkSecurityException(e, sys)