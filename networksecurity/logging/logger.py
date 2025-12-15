import logging
import os
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"


logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOGS_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOGS_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)


def log_separator(secion_name=""):
    separator_line = "-" * 90
    logging.info(f"\n\n{separator_line}")
    if secion_name:
        logging.info(f"START OF: {secion_name.upper()}")
        logging.info(f"{separator_line}\n")


if __name__ == "__main__":
    log_separator(secion_name="logging test")