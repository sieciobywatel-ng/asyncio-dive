from typing import Generator
from typing import Union

# import asyncio
from pathlib import Path


def ls(path: Path) -> Generator[Path, None, None]:
    """
    Traverse a given path, yielding paths of files and directories
    """
    # nice-to-have: change to match
    path: Path = Path(path) # type: ignore[no-redef]
    yield path
    if path.is_dir():
        for child in path.iterdir(): # child: Path
            yield from ls(child)

def main() -> None:
    # procs should exist on every POSIX system and not be too long
    path = Path('/dev/cpu')
    processors: Generator[Path] = ls(path)
    for cpu in processors:
        print(cpu)
    print("Hello from asyncio-dive!")


if __name__ == "__main__":
    main()
