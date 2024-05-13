import logging
from logging.config import dictConfig
from tsviewer.configuration import Configuration
from pathlib import Path

__all__ = ['logger']

configuration = Configuration.get_instance()
log_path = Path(configuration.log_path)

append_to_console = False
if log_path.exists() and not log_path.parent.is_dir() and configuration.log_path != str():
    try:
        log_path.mkdir()
    except (OSError, Exception):
        print('Could not create log directory, falling bag to console appender only')
        append_to_console = True
else:
    append_to_console = True


# level_string = 'DEBUG' if configuration.debug else 'ERROR'
level_string = 'DEBUG'  # for now
# TODO: Revise this: We use dictConfig for setting up logging because flask recommends this way of doing it
# TODO: We may use a yaml file instead of this dict, but we have to use variables within it somehow
logging_config = {'version': 1,
                  'formatters':
                      {'simple': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}},
                  'handlers': {
                      'console': {'class': 'logging.StreamHandler', 'level': level_string, 'formatter': 'simple',
                                  'stream': 'ext://sys.stdout'},
                      'file': {'class': 'logging.FileHandler', 'level': level_string, 'formatter': 'simple',
                               'filename': configuration.log_path}},
                  'loggers': {'console': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
                              'file': {'level': 'DEBUG', 'handlers': ['file'], 'propagate': False}},
                  'root': {'level': 'DEBUG', 'handlers': ['console', 'file']}}
dictConfig(logging_config)

logger = logging.getLogger('flask_tsviewer.app')
