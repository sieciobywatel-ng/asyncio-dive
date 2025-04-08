import os
import shutil
import asyncio
import pathlib

import logging

import pytest
import pytest_asyncio

import consumers
from main import produce

tbd = pytest.mark.xfail(reason="To Be Done...")
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def queue():
    this = asyncio.Queue()
    yield this
    await this.join()

@tbd
@pytest_asyncio.fixture
async def consumer(queue):
    loop = asyncio.get_running_loop()
    consumer = loop.create_task(consumers.consume(queue))
    yield consumer
    logger.info(f"* Stopping consumer... {consumer}")
    consumer.cancel()
    assert queue.empty()
    logger.info(f"* Canceled. Queue: {queue}")


@pytest.mark.asyncio
class TestProducers:

    async def test_works_on_a_file(self, tree, capsys, consumer, queue):
        path = pathlib.Path('README.md')
        await asyncio.gather(produce(path, target=queue))
        stdout, stderr = capsys.readouterr()
        assert str(path) in stdout

    async def test_works_on_a_directory(self, tree, capsys, consumer, queue):
        await asyncio.gather(produce(tree, target=queue))
        stdout, stderr = capsys.readouterr()
        assert 'tree/' in stdout

    async def test_is_able_to_traverse(self, tree, capsys, consumer, queue):
        expected = {
            'tree/bar',
            'tree/egg',
            'tree/foo/',
            'tree/foo/bar/',
            'tree/foo/bar/spam',
        }
        await asyncio.gather(produce(tree, target=queue))
        stdout, stderr = capsys.readouterr()
        for path in expected:
            assert path in stdout
