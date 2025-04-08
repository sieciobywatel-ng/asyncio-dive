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

    @tbd
    async def test_works_on_a_directory(self, tree, capsys):
        listing = als(tree)
        entries = list(listing)
        assert any(os.path.basename(p) == 'bar' for p in entries)

    @tbd
    async def test_is_able_to_traverse(self, tree, capsys):
        expected = {
            'foo',
            'bar', # x2
            'egg',
            'spam'
        }
        results = als(tree)
        listed = [os.path.basename(p) for p in results]
        for name in expected:
            assert name in listed
