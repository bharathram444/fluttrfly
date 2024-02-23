# Assuming the code is part of a package named 'fluttrfly.bin.functions.
from fluttrfly.bin.functions.build_functions import (
    with_loading,
)


def test_with_loading_success():
    def task():
        print("Task executed successfully")

    with_loading(task)


def test_with_loading_file_not_found_error():
    def task():
        raise FileNotFoundError("File not found")

    result = with_loading(task)
    assert result is None


def test_with_loading_is_a_directory_error():
    def task():
        raise IsADirectoryError("Is a directory")

    result = with_loading(task)
    assert result is None
