import os

from typing import Generator
from typing import Callable
from pathlib import Path
from functools import partial

import asyncio
import random
import logging

logging.basicConfig(
    level=getattr(
        logging,
        os.environ.get("LOG_LEVEL", '').upper(),
        logging.ERROR,
    ),
)

logger = logging.getLogger(__file__)

# to randomize execution time:
nap = partial(asyncio.sleep, random.uniform(0, 0.1))


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


def consume(task):
    path = task.result()
    print(f"als: {path}")


async def als(path: Path):
    spawned = set()  # we need non-weak ref to tasks
    asyncio.current_task().add_done_callback(consume)  # TODO: inject consumer
    if path.is_dir():
        loop = asyncio.get_running_loop()
        logger.debug(f" * listing directory: {path}")
        for child in path.iterdir():
            task = loop.create_task(als(child))
            spawned.add(task)
        await nap()
    await asyncio.gather(*spawned)
    return path


path = Path('/dev/cpu')
# path = '.venv/bin'

def main():
    # procs should exist on every POSIX system and not be too long
    cpu = list(ls(path))
    for found in cpu:
        print(f" ls: {found}")
    asyncio.run(als(path))

if __name__ == "__main__":
    main()
