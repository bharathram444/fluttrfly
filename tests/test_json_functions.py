import json
from pathlib import Path

import pytest

from fluttrfly.bin.functions.json_functions import (
    check_path_exists,
    load,
    read_config,
    write_config,
    write_specific_field,
)


@pytest.fixture
def config_path_data():
    """Fixture to provide config path and data for tests."""
    config_path = "test_config.json"
    config_data = {"key": "value"}
    return config_path, config_data


def write_json_file(file_path, data):
    """Helper function to write JSON data to a file."""
    with open(file_path, "w") as f:
        json.dump(data, f)


def read_json_file(file_path):
    """Helper function to read JSON data from a file."""
    with open(file_path, "r") as f:
        return json.load(f)


def cleanup_file(file_path):
    """Helper function to delete the file after the test."""
    Path(file_path).unlink()


def test_write_config(config_path_data):
    """Test writing a configuration file."""
    config_path, config_data = config_path_data
    write_config(config_path, config_data)
    assert read_json_file(config_path) == config_data
    cleanup_file(config_path)


def test_read_config(config_path_data):
    """Test reading a configuration file."""
    config_path, config_data = config_path_data
    write_json_file(config_path, config_data)
    assert read_config(config_path) == config_data
    cleanup_file(config_path)


def test_write_specific_field(config_path_data):
    """Test writing a specific field in the config file."""
    config_path, config_data = config_path_data
    write_json_file(config_path, config_data)
    write_specific_field(config_path, "key", "new_value")
    assert read_json_file(config_path) == {"key": "new_value"}
    cleanup_file(config_path)


def test_load(config_path_data):
    """Test loading specific fields from a configuration file."""
    config_path = config_path_data[0]
    config_data = {
        "repo_url": "https://github.com/repo",
        "environment_setup_done": True,
        "repo_dir": "",
        "env_version": "",
        "messages": "",
    }
    write_json_file(config_path, config_data)
    assert load(config_path) == (
        "https://github.com/repo",
        True,
        "",
        "",
        "",
    )
    cleanup_file(config_path)


def test_check_path_exists():
    """Test checking if a directory path exists."""
    path = "check_test"
    Path(path).mkdir(parents=True, exist_ok=True)
    assert check_path_exists(path, False, False) is True
    Path(path).rmdir()
