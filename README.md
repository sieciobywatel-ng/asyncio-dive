TODO:

- [&bigdot;] write simple async application traversing directory tree
    - [&bigdot;] first, start with sync version
        - [&checkmark;] works on file
        - [ ] works on directory
        - [ ] can go inside sub directories
    - [&bigdot;] tests it works, create a test suite
    - [ ] change execution to async
- [ ] maybe add tests showing what works and how and what not


# Usage

#### Install dependencies:

```
uv venv
uv sync
```

#### Run pytest


(optionally with mypy and spec renderer)

- `uv run pytest --spec --mypy`

- ...or activate venv and run pytest directly:

```
source .venv/bin/activate
pytest --spec --mypy
```

