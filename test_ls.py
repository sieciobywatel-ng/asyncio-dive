import os
import shutil

import pytest

from main import ls

tbd = pytest.mark.xfail(reason="To Be Done...")


def test_ls_works_on_file(tree):
    path = 'README.md'
    results = list(ls(path))
    assert results
    assert len(results) == 1
    first, *_ = results
    assert str(first) == str(path)


def test_ls_works_on_a_directory(tree):
    listing = ls(tree)
    entries = list(listing)
    assert any(os.path.basename(p) == 'bar' for p in entries)


def test_ls_is_able_to_traverse(tree):
    expected = {
        'foo',
        'bar', # x2
        'egg',
        'spam'
    }
    results = ls(tree)
    listed = [os.path.basename(p) for p in results]
    for name in expected:
        assert name in listed


@pytest.fixture()
def tree(tmp_path):
    # /
    #     tree/
    #     ├── bar
    #     ├── egg
    #     └── foo
    #         └── bar
    #             └── spam

    root = tmp_path / 'tree'
    foo = root / 'foo'
    bar = root / 'bar'
    foobar = foo / 'bar'

    spam = foobar / 'spam'
    egg = root / 'egg'

    directories =[root, foo, foobar]
    files = [spam, egg, bar]

    for d in directories:
        d.mkdir(parents=True, exist_ok=True)

    for f in files:
        f.touch(exist_ok=True)

    os.system(f'tree {tmp_path}')
    for f in [*directories, *files]:
        assert f.exists()

    yield root
    # cleanup
    shutil.rmtree(root)
