import logging
import sys

from tsviewer.configuration import Configuration
from pathlib import Path

configuration = Configuration.get_instance()
log_path = Path(configuration.log_path)

append_to_console = False
if log_path.exists() and not log_path.parent.is_dir() and configuration.log_path != str():
    try:
        log_path.mkdir()

    except (OSError, Exception):
        print('Could not create log directory, falling bag to console appender')
        append_to_console = True
else:
    append_to_console = True

logger = None


def get_logger(name: str, to_file: str = 'log/tsviewer.log') -> logging.Logger:
    global logger
    if logger is None:
        logger = logging.getLogger(name)
    else:
        return logger

    level = logging.DEBUG if configuration.debug else logging.WARNING
    print(f'Logfile can be created: {log_path.is_dir()}')
    if not append_to_console:
        logging.basicConfig(filename=to_file, encoding='utf-8', level=level)
    else:
        logging.basicConfig(stream=sys.stderr, encoding='utf-8', level=level)
    return logger
