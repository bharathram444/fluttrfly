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
    config_path = "test_config.json"
    config_data = {"key": "value"}
    return config_path, config_data


def test_write_config(config_path_data):
    write_config(config_path_data[0], config_path_data[1])

    with open(config_path_data[0], "r") as f:
        assert json.load(f) == config_path_data[1]

    Path.unlink(Path(config_path_data[0]))


def test_read_config(config_path_data):
    with open(config_path_data[0], "w") as f:
        json.dump(config_path_data[1], f)

    assert read_config(config_path_data[0]) == config_path_data[1]

    Path.unlink(Path(config_path_data[0]))


def test_write_specific_field(config_path_data):
    with open(config_path_data[0], "w") as f:
        json.dump(config_path_data[1], f)

    write_specific_field(config_path_data[0], "key", "new_value")

    with open(config_path_data[0], "r") as f:
        assert json.load(f) == {"key": "new_value"}

    Path.unlink(Path(config_path_data[0]))


def test_load(config_path_data):
    config_data = {
        "repo_url": "https://github.com/repo",
        "environment_setup_done": True,
        "repo_dir": "",
        "env_version": "",
        "messages": "",
    }

    with open(config_path_data[0], "w") as f:
        json.dump(config_data, f)

    assert load(config_path_data[0]) == (
        "https://github.com/repo",
        True,
        "",
        "",
        "",
    )

    Path.unlink(Path(config_path_data[0]))


def test_check_path_exists():
    path = "check_test"
    Path.mkdir(Path(path), parents=True, exist_ok=True)

    assert check_path_exists(path, False, False) is True

    Path.rmdir(Path(path))
