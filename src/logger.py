import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)

def get_logger(_name="ac_radio"):
    # create logger
    logger = logging.getLogger(_name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.debug(logger)
    return logger
