from pathlib import Path
from unittest.mock import patch

import pytest

from fluttrfly.bin.commands.global_variables import warning_style
from fluttrfly.bin.commands.setup_command import SetupCommand


@pytest.fixture
def setup_command(tmpdir):
    """Fixture to create an instance of SetupCommand."""
    repo_dir = tmpdir.mkdir("repo_dir")  # Create a temp directory
    with patch(
        'fluttrfly.bin.commands.setup_command.load',
        return_value=("repo_url", True, str(repo_dir), "env_version", "messages"),
    ), patch('fluttrfly.bin.commands.setup_command.env_check_up') as mock_env_check:
        mock_env_check.return_value = None  # Mocking the return value
        yield SetupCommand()


@patch('sys.exit')
@patch('fluttrfly.bin.commands.global_variables.console.print')
def test_used_both(mock_print, mock_exit, setup_command, mocker):
    """Test the usedBoth method of SetupCommand."""
    mocker.patch('pathlib.Path.cwd', return_value=Path("/some/valid/directory"))
    mocker.patch('pathlib.Path.exists', return_value=True)

    setup_command.used_both()

    mock_print.assert_called_once_with(
        f"[{warning_style}]🚨 Both --riverpod[-r] and --bloc[-b] flags were provided. Please use only one. 😕"
    )
    mock_exit.assert_called_once_with(1)


@patch('sys.exit')
def test_setup_no_tags(mock_exit, setup_command, mocker):
    """Test the setup_no_tags method of SetupCommand."""
    mocker.patch('pathlib.Path.cwd', return_value=Path("/some/valid/directory"))
    mocker.patch('pathlib.Path.exists', return_value=True)

    setup_command.setup_no_tags()
    mock_exit.assert_called_once_with(0)
