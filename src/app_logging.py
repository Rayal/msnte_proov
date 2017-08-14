import logging
from os import mkdir


# Creates a log message formatter
def get_formatter():
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    return formatter


# Creates a log message handler
def get_handler(filename):
    try:
        handler = logging.FileHandler(filename)
    except FileNotFoundError:
        path = filename.split('/')
        path = "/".join((path[:-1]))
        mkdir(path)
        handler = logging.FileHandler(filename)
    formatter = get_formatter()
    handler.setFormatter(formatter)
    return handler


# Configures the given logger with a handler and formatter
def config_logger(logger, filename):
    handler = get_handler(filename)
    logger.addHandler(handler)
    return logger
