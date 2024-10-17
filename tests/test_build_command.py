from pathlib import Path
from unittest.mock import patch

import pytest

from fluttrfly.bin.commands.build_command import BuildCommand

# Mocking functions and global variables used in the BuildCommand class
from fluttrfly.bin.commands.global_variables import (
    console,
    error_style,
    libString,
    warning_style,
)


@pytest.fixture
def mock_build_command(tmpdir):
    """Fixture to create a mock of BuildCommand class."""
    repo_dir = tmpdir.mkdir("repo_dir")  # Create a temp directory
    with patch(
        'fluttrfly.bin.commands.build_command.load',
        return_value=("repo_url", True, str(repo_dir), "env_version", "messages"),
    ), patch('fluttrfly.bin.commands.build_command.env_check_up') as mock_env_check:
        mock_env_check.return_value = None  # Mocking the return value
        yield BuildCommand()  # Yield the instance for use in tests


def check_console_output(mock_console, expected_message):
    """Helper function to check console output"""
    mock_console.assert_called_once_with(expected_message)


def test_build_module_tag_invalid_dir(mock_build_command, mocker):
    mocker.patch('sys.exit')
    mocker.patch('pathlib.Path.cwd', return_value=Path("/wrong/directory"))
    mock_console = mocker.patch.object(console, 'print')

    mock_build_command.build_module_tag(module="my_module")

    check_console_output(
        mock_console,
        f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory.",
    )


def test_build_module_tag_invalid_module(mock_build_command, mocker):
    mocker.patch('pathlib.Path.cwd', return_value=Path(f"/some/path{libString}"))
    mock_console = mocker.patch.object(console, 'print')

    mock_build_command.build_module_tag(module="123")

    check_console_output(
        mock_console, f"[{error_style}]📛 ModuleName argument must be a non-numeric string."
    )


def test_build_assets_tag_already_exists(mock_build_command, mocker):
    mocker.patch('pathlib.Path.cwd', return_value=Path("/some/valid/directory"))
    mocker.patch('pathlib.Path.exists', return_value=True)
    mock_console = mocker.patch.object(console, 'print')

    mock_build_command.build_assets_tag()

    check_console_output(
        mock_console, f"[{warning_style}]🚨 Assets structure already exists. No changes made."
    )


def test_build_core_tag_already_exists(mock_build_command, mocker):
    mocker.patch('pathlib.Path.exists', return_value=True)
    mock_console = mocker.patch.object(console, 'print')

    mock_build_command.build_core_tag()

    check_console_output(
        mock_console, f"[{warning_style}]🚨 Core structure already exists. No changes made."
    )
