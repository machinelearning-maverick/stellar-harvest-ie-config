import functools
import logging

def log_io(level=logging.DEBUG):
    """
    Decorator to log function entry with args/kwargs and exit with return value.
    """
    def decorator(fn):
        logger = logging.getLogger(fn.__module__)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            logger.log(level, f"Entering {fn.__name__} args={args} kwargs={kwargs}")
            result = fn(*args, **kwargs)
            logger.log(level, f"Exiting  {fn.__name__} returned={result!r}")
            return result
        return wrapper
    return decorator
