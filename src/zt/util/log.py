import logging


log_format = '%(name)-18s: %(levelname)-8s: %(message)s'


def setup_logging(loglevel=logging.INFO):
    logger = logging.getLogger()
    if not logger.handlers:
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console)
    logger.setLevel(loglevel)
