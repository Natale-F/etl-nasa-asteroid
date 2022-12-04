import logging


def init_logger(log_level: str = 'INFO'):
    """Returns a logger with wanted log level & basic configuration."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s - %(message)s"
    logging.basicConfig(format=log_format)
    log = logging.getLogger()
    log.setLevel(log_level)
    return log
