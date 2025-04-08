import os
import shutil
import asyncio
import pathlib

import pytest

from main import als as als  # just for a moment...

tbd = pytest.mark.xfail(reason="To Be Done...")


@pytest.mark.asyncio
class TestASynchronousFileLister:

    async def test_works_on_a_file(self, tree, capsys):
        path = pathlib.Path('README.md')
        await asyncio.gather(als(path))
        stdout, stderr = capsys.readouterr()
        assert str(path) in stdout

    async def test_works_on_a_directory(self, tree, capsys):
        await asyncio.gather(als(tree))
        stdout, stderr = capsys.readouterr()
        assert 'tree/' in stdout

    async def test_is_able_to_traverse(self, tree, capsys):
        expected = {
            'tree/bar',
            'tree/egg',
            'tree/foo/',
            'tree/foo/bar/',
            'tree/foo/bar/spam',
        }
        await asyncio.gather(als(tree))
        stdout, stderr = capsys.readouterr()
        for path in expected:
            assert path in stdout
