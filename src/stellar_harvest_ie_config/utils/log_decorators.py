import functools
import logging
import inspect

from typing import Callable, Dict, Type


def _truncate(value, max_items: int) -> str:
    if isinstance(value, (list, tuple, set)):
        items = list(value)
        if len(items) > max_items:
            return f"{items[:max_items]}... (+{len(items) - max_items} more)"
        return str(items)
    return repr(value)


def _format_value(value, max_items: int, skip_types: Dict[Type, Callable]) -> str:
    for typ, formatter in skip_types.items():
        if isinstance(value, typ):
            return formatter(value)
    return _truncate(value, max_items)


def _truncate_args(args, kwargs, max_items, skip_types):
    t_args = [_format_value(a, max_items, skip_types) for a in args]
    t_kwargs = {k: _format_value(v, max_items, skip_types) for k, v in kwargs.items()}
    return t_args, t_kwargs


def log_io(level=logging.DEBUG, max_items=10, skip_types: Dict[Type, Callable] = None):
    """
    Decorator to log function entry with args/kwargs and exit with return value.
    For both sync and async functions.
    Truncates collections longer than max_items to keep logs readable.

    skip_types: dict mapping type -> formatter callable, e.g.
        {pd.DataFrame: lambda v: f"<DataFrame shape={v.shape}>"}
    """

    _skip = skip_types or {}

    def decorator(fn):
        logger = logging.getLogger(fn.__module__)

        if inspect.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def wrapper(*args, **kwargs):
                t_args, t_kwargs = _truncate_args(args, kwargs, max_items, _skip)
                logger.log(
                    level, f"Entering {fn.__name__} args={t_args} kwargs={t_kwargs}"
                )
                result = await fn(*args, **kwargs)
                logger.log(
                    level,
                    f"Exiting  {fn.__name__} returned={_format_value(result, max_items, _skip)}",
                )
                return result

        else:

            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                t_args, t_kwargs = _truncate_args(args, kwargs, max_items, _skip)
                logger.log(
                    level, f"Entering {fn.__name__} args={t_args} kwargs={t_kwargs}"
                )
                result = fn(*args, **kwargs)
                logger.log(
                    level,
                    f"Exiting  {fn.__name__} returned={_format_value(result, max_items, _skip)}",
                )
                return result

        return wrapper

    return decorator
