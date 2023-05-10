import logging, sys


def get_file_handler(formatter, log_filename):
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    return file_handler


def get_stream_handler(formatter):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(name, formatter, log_filename = "logfile.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler(formatter, log_filename))
    logger.addHandler(get_stream_handler(formatter))
    return logger