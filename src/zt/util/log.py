import logging

def setup_logging():
    logger = logging.getLogger()
    if not logger.handlers:
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter('%(name)-18s: %(levelname)-8s: %(message)s'))
        logger.addHandler(console)
    logger.setLevel(logging.INFO)
