def pytest_configure(config):
    plugin = config.pluginmanager.getplugin('mypy')
    # plugin.mypy_argv.append('--check-untyped-defs')
    plugin.mypy_argv.append('--exclude')
    plugin.mypy_argv.append('test_*.py')
    plugin.mypy_argv.append('--exclude')
    plugin.mypy_argv.append('conftest.py')
