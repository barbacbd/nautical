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
    fmt = "[🌊 %(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: blue + fmt + reset,
        logging.INFO: green + fmt + reset,
        logging.WARNING: yellow + fmt + reset,
        logging.ERROR: red + fmt + reset,
        logging.CRITICAL: purple + fmt + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name='nautical', verbosity=logging.DEBUG):
    '''Wrap the logging.getLogger functionality to apply nautical 
    based logging information.

    :param name: Name of the logger
    :param verbosity: Level of verbosity for the logger
    :return: logging.log formatted with the NauticalLogFormatter
    '''
    log = logging.getLogger(name)
    log.setLevel(verbosity)

    if not log.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(NauticalLogFormatter())
        log.addHandler(handler)

    return log
