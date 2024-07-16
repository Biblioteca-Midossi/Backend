import logging
from datetime import datetime
# import os
from pathlib import Path


def setup_logger():
    logs_folder = Path('logs')
    logger_file = Path(f'{logs_folder}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

    if not logs_folder.exists():
        logs_folder.mkdir()

    if logger_file.exists():
        logger_file.unlink()

    # total_logs: list[Path] = [file for file in logs_folder.iterdir() if file.suffix == '.log']
    # if len(total_logs) > 2:
    #     less_recent_logs: list[Path] = [logger_file]
    #     for file in total_logs:
    #         if file.stat().st_birthtime < less_recent_logs[0].stat().st_birthtime:
    #             less_recent_log = file
    #     less_recent_log.unlink()

    print("Setting up logger...")
    logging.basicConfig(
        filename = logger_file,
        level = logging.DEBUG,
        format = '%(levelname)s %(asctime)s %(message)s',
        datefmt = '%d/%m/%Y %I:%M:%S %p'
    )
    print("Logger setup completed. Logs will now be logged to file")
