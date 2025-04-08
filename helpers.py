from functools import partial
import asyncio

# to randomize execution time
nap = partial(asyncio.sleep, random.uniform(0, 0.1))

from logs import logger


def format(*args, **kwargs):
    kw = [f"{k}={v}" for k, v in kwargs.items()]
    parts = [*map(str, args), *kw]
    return ', '.join(parts)



def alogged(fn, level=logging.PEDANTIC):
    @wraps(fn)
    async def inner(*args, **kwargs):
        logger.log(level, f"   called: {fn.__name__}(...)")
        logger.log(level, f"   |--> {format(*args, **kwargs)}")
        result = await fn(*args, **kwargs)
        result and logger.log(level, f"   returns: {fn.__name__}(...)")
        result and logger.log(level, f"   <--| {result}")
        return result
    return inner


def logged(fn, level=logging.PEDANTIC):
    @wraps(fn)
    def inner(*args, **kwargs):
        logger.log(level, f"   called: {fn.__name__}(...)")
        logger.log(level, f"   |--> {format(*args, **kwargs)}")
        result = fn(*args, **kwargs)
        result and logger.log(level, f"   returns: {fn.__name__}(...)")
        result and logger.log(level, f"   <--| {result}")
        return result
    return inner
