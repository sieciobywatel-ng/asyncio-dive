import os

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
