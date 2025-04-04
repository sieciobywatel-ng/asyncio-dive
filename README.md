TODO:

- [&sdot;] write simple async application traversing directory tree
    - [✓] first, start with sync version
        - [&checkmark;] works on file
        - [✓]] works on directory
        - [✓]] can go inside sub directories
    - [⋅] tests it works, create a test suite
    - [ ] change execution to async
- [ ] add pre-commit, linting, blacking #nice-to-have
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

