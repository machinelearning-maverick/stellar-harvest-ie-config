import functools
import logging
import inspect


def _truncate(value, max_items: int) -> str:
    if isinstance(value, (list, tuple, set)):
        items = list(value)
        if len(items) > max_items:
            return f"{items[:max_items]}... (+{len(items) - max_items} more)"
        return str(items)
    return repr(value)


def _truncate_args(args, kwargs, max_items):
    truncated_args = [_truncate(a, max_items) for a in args]
    truncated_kwargs = {k: _truncate(v, max_items) for k, v in kwargs.items()}
    return truncated_args, truncated_kwargs


def log_io(level=logging.DEBUG, max_items=10):
    """
    Decorator to log function entry with args/kwargs and exit with return value.
    For both sync and async functions.
    Truncates collections longer than max_items to keep logs readable.
    """

    def decorator(fn):
        logger = logging.getLogger(fn.__module__)

        if inspect.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def wrapper(*args, **kwargs):
                t_args, t_kwargs = _truncate_args(args, kwargs, max_items)
                logger.log(
                    level, f"Entering {fn.__name__} args={t_args} kwargs={t_kwargs}"
                )
                result = await fn(*args, **kwargs)
                logger.log(
                    level,
                    f"Exiting  {fn.__name__} returned={_truncate(result, max_items)}",
                )
                return result

        else:

            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                t_args, t_kwargs = _truncate_args(args, kwargs, max_items)
                logger.log(
                    level, f"Entering {fn.__name__} args={t_args} kwargs={t_kwargs}"
                )
                result = fn(*args, **kwargs)
                logger.log(
                    level,
                    f"Exiting  {fn.__name__} returned={_truncate(result, max_items)}",
                )
                return result

        return wrapper

    return decorator
