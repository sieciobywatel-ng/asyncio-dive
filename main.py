from typing import Iterable

# import asyncio
from pathlib import Path


def ls(path: Path) -> Iterable[Path]:
    """
    Traverse a given path, yielding paths of files and directories
    """
    # nice-to-have: change to match
    path = Path(path)
    yield path
    if path.is_dir():
        for child in path.iterdir():
            yield from ls(child)

def main():
    # procs should exist on every POSIX system and not be too long
    processors = ls('/dev/cpu')
    for cpu in processors:
        print(cpu)
    print("Hello from asyncio-dive!")


if __name__ == "__main__":
    main()


