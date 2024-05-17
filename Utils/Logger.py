import logging
import os
from datetime import datetime


def setup_logger():
    logger_file = f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
    if not os.path.exists('logs'):
        os.mkdir('logs')
    if os.path.exists(logger_file):
        os.remove(logger_file)
    print("Setting up logger...")
    logging.basicConfig(
        filename = logger_file,
        level = logging.DEBUG,
        format = '%(levelname)s %(asctime)s %(message)s',
        datefmt = '%d/%m/%Y %I:%M:%S %p'
    )
    print("Logger setup completed. Logs will not be logged to file")
