import logging


class NauticalLogFormatter(logging.Formatter):
    '''Formatter class that will be used for formatting nautical
    information. The formatter will add color as well as an image
    '''
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    purple = "\x1b[35;20m"
    reset = "\x1b[0m"
    format = "[🌊 %(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: purple + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def getLogger(name='nautical', verbosity=logging.CRITICAL):
    '''Wrap the logging.getLogger functionality to apply nautical 
    based logging information.

    :param name: Name of the logger
    :param verbosity: Level of verbosity for the logger
    :return: logging.log formatted with the NauticalLogFormatter
    '''
    log = logging.getLogger()
    log.setLevel(verbosity)

    handler = logging.StreamHandler()
    handler.setFormatter(NauticalLogFormatter())
    log.addHandler(handler)

    return log
