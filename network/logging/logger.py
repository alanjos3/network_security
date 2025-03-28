import logging
import os
import datetime

LOG_FILE = f"{datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log"
log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

os.makedirs(log_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(lineno)d %(levelname)s : %(message)s',
    level=logging.INFO,
)
