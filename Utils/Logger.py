import logging
from datetime import datetime
from pathlib import Path


def setup_logger():
    logs_folder = Path('logs')
    logger_file = Path(f'{logs_folder}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

    if not logs_folder.exists():
        logs_folder.mkdir()

    if logger_file.exists():
        logger_file.unlink()

    for file in sorted(logs_folder.iterdir())[:-4]:
        file.unlink()

    print("Setting up logger...")
    logging.basicConfig(
        filename = logger_file,
        level = logging.DEBUG,
        format = '%(levelname)s %(asctime)s %(message)s',
        datefmt = '%d/%m/%Y %I:%M:%S %p'
    )
    print("Logger setup completed. Logs will now be logged to file")
