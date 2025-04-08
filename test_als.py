import os
import shutil

import pytest

from main import ls as als  # just for a moment...

# tbd = pytest.mark.xfail(reason="To Be Done...")


class TestASynchronousFileLister:

    def test_works_on_a_file(self, tree):
        path = 'README.md'
        results = list(als(path))
        assert results
        assert len(results) == 1
        first, *_ = results
        assert str(first) == str(path)

    def test_works_on_a_directory(self, tree):
        listing = als(tree)
        entries = list(listing)
        assert any(os.path.basename(p) == 'bar' for p in entries)

    def test_is_able_to_traverse(self, tree):
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
