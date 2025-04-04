import os
import main

def test_main_py_can_be_run_from_os():
    error = os.system('python main.py')
    assert not error


def test_main_works():
    main.main()
    assert True
