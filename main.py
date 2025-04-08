import os

from typing import Generator
from typing import Callable
from pathlib import Path
from functools import partial
import random
import logging
import asyncio

from rich import print
from rich.console import Console

import logs
from consumers import consume
# to randomize execution time:
nap = partial(asyncio.sleep, random.uniform(0, 0.1))
console = Console()


@logs.logged
def ls(path: Path) -> Generator[Path, None, None]:
    """
    Traverse a given path, yielding paths of files and directories
    """
    # nice-to-have: change to match
    # TODO: should we worry about looped symlinks?
    #    for production, we should, in this context, let's ignore
    path: Path = Path(path) # type: ignore[no-redef]
    yield path
    if path.is_dir():
        for child in path.iterdir(): # child: Path
            yield from ls(child)


@logs.logged
def render(task):
    path = task.result()
    print(r"[yellow]\[ async ]:[/yellow]", f"{path}")


async def als(path: Path):
    logger = logging.getLogger(__name__)
    spawned = set()  # we need non-weak ref to tasks
    asyncio.current_task().add_done_callback(render)  # TODO: inject consumer
    if path.is_dir():
        loop = asyncio.get_running_loop()
        console.log(f" * listing directory: {path}")
        for child in path.iterdir():
            task = loop.create_task(als(child))
            spawned.add(task)
        await nap()
    await asyncio.gather(*spawned)
    return path


async def produce(path: Path, target: asyncio.Queue):
    logger = logging.getLogger(__name__)
    await target.put(path)
    spawned = set()  # we need non-weak ref to tasks
    if path.is_dir():
        loop = asyncio.get_running_loop()
        logger.debug(f" * Producer: listing directory: {path}")
        for child in path.iterdir():
            task = loop.create_task(produce(child, target))
            logger.debug(f" * Producer: child found: {child}")
            spawned.add(task)
            # await asyncio.sleep(0)
            await nap()
    await asyncio.gather(*spawned)


path = Path('/dev/cpu')


async def run(path=Path(path)):
    logger = logging.getLogger(__name__)
    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()
    consumer = loop.create_task(consume(queue))
    producer = loop.create_task(produce(path, queue))
    await asyncio.gather(producer)

    logger.info(f"* Stopping consumer... {consumer}")
    consumer.cancel()
    assert queue.empty(), queue
    logger.info(f"* Canceled. Queue: {queue}")


def main():
    # procs should exist on every POSIX system and not be too long
    console.rule("Running: ls()")
    cpu = list(ls(path))
    for found in cpu:
        print(r" [cyan]\[ sync  ]:[/cyan]", f"{found}")
    console.rule("Running: als()")
    asyncio.run(als(path))
    console.rule("Running: producer()")
    asyncio.run(run(path))
    console.rule("Done.")


if __name__ == "__main__":
    logs.configure()
    main()
