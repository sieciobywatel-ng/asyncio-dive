import os

from typing import Generator
from pathlib import Path

# import asyncio
import logging

logging.basicConfig(
    level=getattr(
        logging,
        os.environ.get("LOG_LEVEL", '').upper(),
        logging.ERROR,
    ),
)

logger = logging.getLogger(__file__)

path = Path('/dev/cpu')
# path = '.venv/bin'


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
        logger.debug(" * Traversing: %s", path)
        for child in path.iterdir(): # child: Path
            yield from ls(child)


def main():
    # procs should exist on every POSIX system and not be too long
    cpu = list(ls(path))
    for found in cpu:
        print(f" ls: {found}")

if __name__ == "__main__":
    main()
