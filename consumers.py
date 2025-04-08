import logging

from rich import print

import logs

@logs.alogged
async def consume(queue):
    logger = logging.getLogger(__name__)
    send = logs.logged(print)
    logger.info(f" * Consumer started: {queue}")
    while True:
        found = await queue.get()
        logger.debug(f" * Consumer activated: {found}")
        logger.debug(f"            ...queue is: {queue}")
        send(f"[produce]: {found}")
        queue.task_done()
    logger.info(f" * Consumer finished: {queue}")
