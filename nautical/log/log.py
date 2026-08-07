import logging
import os
import sys


class NauticalLogFormatter(logging.Formatter):
    """Colored log formatter with per-level ANSI styling when outputting to a TTY."""

    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    purple = "\x1b[35;20m"
    reset = "\x1b[0m"
    fmt = "[🌊 %(levelname)s %(asctime)s %(name)s]: %(message)s"

    def __init__(self, use_color: bool = True) -> None:
        super().__init__()
        if use_color:
            self._formatters = {
                logging.DEBUG: logging.Formatter(self.blue + self.fmt + self.reset),
                logging.INFO: logging.Formatter(self.green + self.fmt + self.reset),
                logging.WARNING: logging.Formatter(self.yellow + self.fmt + self.reset),
                logging.ERROR: logging.Formatter(self.red + self.fmt + self.reset),
                logging.CRITICAL: logging.Formatter(self.purple + self.fmt + self.reset),
            }
        else:
            plain = logging.Formatter(self.fmt)
            self._formatters = {
                level: plain
                for level in (
                    logging.DEBUG,
                    logging.INFO,
                    logging.WARNING,
                    logging.ERROR,
                    logging.CRITICAL,
                )
            }

    def format(self, record: logging.LogRecord) -> str:
        formatter = self._formatters.get(record.levelno, self._formatters[logging.DEBUG])
        return formatter.format(record)


def _get_default_level() -> int:
    env_level = os.environ.get("NAUTICAL_LOG_LEVEL", "").upper()
    return getattr(logging, env_level, logging.WARNING)


def get_logger(name: str = "nautical") -> logging.Logger:
    """Get a logger with nautical formatting.

    :param name: Logger name (use __name__ for per-module loggers)
    :return: Configured logger instance
    """
    log = logging.getLogger(name)
    log.setLevel(_get_default_level())

    if not log.handlers:
        handler = logging.StreamHandler()
        use_color = hasattr(sys.stderr, "isatty") and sys.stderr.isatty()
        handler.setFormatter(NauticalLogFormatter(use_color=use_color))
        log.addHandler(handler)

    return log
