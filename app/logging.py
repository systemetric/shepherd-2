"""Configure the logging of shepherd so it is readable and pretty"""
import logging
import click
from copy import copy
import http

logger = logging.getLogger("app")


class CustomFormatter(logging.Formatter):
    """A base formatter class containing the colours"""

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    bold_red = "\x1b[31;20m"
    pale_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    message_format = "%(message)s"

    coloured_levels = {
        logging.DEBUG: grey + "DEBUG" + reset + ":    ",
        logging.INFO: green + "INFO" + reset + ":     ",
        logging.WARNING: yellow + "WARNING" + reset + ":  ",
        logging.ERROR: pale_red + "ERROR" + reset + ":    ",
        logging.CRITICAL: bold_red + "CRITICAL" + reset + ": ",
    }


class ShepherdFormatter(CustomFormatter):
    """A formatter which prints the file and line number"""

    def format(self, record):
        location = f"{record.filename}:{record.lineno}"
        message = record.msg % record.args  # Old style python formatting
        return f"{self.coloured_levels[record.levelno]}{location:<21}| {message}"


class UvicornFormatter(CustomFormatter):
    """The same as the ShepherdFormatter but prints uvicorn instead of path"""

    def format(self, record):
        location = "Uvicorn"
        message = record.msg % record.args  # Old style python formatting
        return f"{self.coloured_levels[record.levelno]}{location:<21}| {message}"


class UvicornAccessFormatter(CustomFormatter):
    """All API calls are logged using this formatter
    Based on the uvicorn.logging
    """
    status_code_colours = {
        1: lambda code: click.style(str(code), fg="bright_white"),
        2: lambda code: click.style(str(code), fg="green"),
        3: lambda code: click.style(str(code), fg="yellow"),
        4: lambda code: click.style(str(code), fg="red"),
        5: lambda code: click.style(str(code), fg="bright_red"),
    }

    def get_status_code(self, status_code: int) -> str:
        """Format the status code using"""
        try:
            status_phrase = http.HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = ""
        status_and_phrase = "%s %s" % (status_code, status_phrase)

        def default(code: int) -> str:
            return status_and_phrase

        func = self.status_code_colours.get(status_code // 100, default)
        return func(status_and_phrase)

    def format(self, record):
        """Assemble a complete message with a coloured http code"""
        recordcopy = copy(record)
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = recordcopy.args
        status_code = self.get_status_code(int(status_code))
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        request_line = click.style(request_line, bold=True)
        location = "Uvicorn.access"
        return (f"{self.coloured_levels[record.levelno]}{location:<20} | "
                f"{client_addr:<16} {status_code:<24} {request_line} ")


def configure_logger(name: str, new_fomater, level):
    logger = logging.getLogger(name)
    logger.propagate = False
    if len(logger.handlers) > 0:
        logger.handlers[0].setFormatter(new_fomater())
    logger.setLevel(level)


def configure_logging(level=logging.DEBUG, third_party_level=logging.INFO):
    """Apply the logging formatters to the logging handlers
    Prevents uvicorn's handlers from double logging
    Sets logging level to `level`
    `uvicorn_level` allows the shepherd logs to come through by raising the uvicorn level
    """
    configure_logger("uvicorn", UvicornFormatter, third_party_level)
    configure_logger("uvicorn.access", UvicornAccessFormatter, third_party_level)
    configure_logger("multipart", logging.Formatter, third_party_level)

    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(ShepherdFormatter())
    logger.addHandler(ch)
    logger.info("Logging configured")
