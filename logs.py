import os
from functools import wraps

import logging

from rich.logging import RichHandler


def configure(namespace=__name__):
    default = logging.WARNING
    requested = os.environ.get("LOG_LEVEL", '').upper()
    level = logging.getLevelNamesMapping().get(requested, default)
    logging.basicConfig(level=level, handlers=[RichHandler()])

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured @{level}")
    return logger


def get_logger(namespace=__name__):
    this = logging.getLogger(namespace)
    return this or configure(namespace)

def format(*args, **kwargs):
    kw = [f"{k}={v}" for k, v in kwargs.items()]
    parts = [*map(str, args), *kw]
    return ', '.join(parts)


def alogged(fn):
    namespace = fn.__name__
    logger = logging.getLogger(namespace) or configure().getLogger(namespace)

    @wraps(fn)
    async def inner(*args, **kwargs):
        logger.debug(f"   called: {fn.__name__}(...)")
        logger.debug(f"   |--> {format(*args, **kwargs)}")
        result = await fn(*args, **kwargs)
        result and logger.debug(f"   returns: {fn.__name__}(...)")
        result and logger.debug(f"   <--| {result}")
        return result
    return inner


def logged(fn):
    namespace = fn.__name__
    logger = logging.getLogger(namespace) or configure().getLogger(namespace)

    @wraps(fn)
    def inner(*args, **kwargs):
        logger.debug(f"   called: {fn.__name__}(...)")
        logger.debug(f"   |--> {format(*args, **kwargs)}")
        result = fn(*args, **kwargs)
        result and logger.debug(f"   returns: {fn.__name__}(...)")
        result and logger.debug(f"   <--| {result}")
        return result
    return inner
