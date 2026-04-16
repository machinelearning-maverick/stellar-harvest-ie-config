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
        },
        "root": {
            "level": "WARNING",  # third-party libs (pydantic, aiokafka, etc.) — warnings only
            "handlers": ["console"],
        },
        "loggers": {
            "stellar_harvest_ie_config": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,   # prevent duplicate output to root's console handler
            },
            "stellar_harvest_ie_models": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_stream": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_store": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_producers": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_consumers": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_ui": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_deployment": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_ml_stellar": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "stellar_harvest_ie_tests": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    })