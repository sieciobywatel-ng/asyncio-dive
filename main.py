from typing import Iterable

# import asyncio
from pathlib import Path


def ls(path: Path) -> Iterable[Path]:
    """
    Traverse a given path, yielding paths of files and directories
    """
    # nice-to-have: change to match
    path = Path(path)
    if path.is_dir():
        yield from map(ls, path.iterdir())
    else:
        yield path


def main():
    print("Hello from asyncio-dive!")


if __name__ == "__main__":
    main()


