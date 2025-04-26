import logging
import sys
from logging.config import dictConfig

def setup_logging():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            },
            # You can add RotatingFileHandler, SysLogHandler, etc.
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "loggers": {
            # Package-specific overrides:
            "stellar_harvest_ie_producers": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False
            },
        }
    })
