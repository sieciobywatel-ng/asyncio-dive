import os
import shutil

import pytest

def pytest_configure(config):
    plugin = config.pluginmanager.getplugin('mypy')
    # plugin.mypy_argv.append('--check-untyped-defs')
    plugin.mypy_argv.append('--exclude')
    plugin.mypy_argv.append('test_*.py')
    plugin.mypy_argv.append('--exclude')
    plugin.mypy_argv.append('conftest.py')



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
