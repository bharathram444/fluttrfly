from unittest.mock import patch

import pytest

from fluttrfly.bin.commands.global_variables import warning_style
from fluttrfly.bin.commands.setup_command import SetupCommand


@pytest.fixture
def setup_command():
    """Fixture to create an instance of SetupCommand."""
    return SetupCommand()


@patch('sys.exit')
@patch('fluttrfly.bin.commands.global_variables.console.print')
def test_used_both(mock_print, mock_exit, setup_command):
    """Test the usedBoth method of SetupCommand."""
    setup_command.usedBoth()

    mock_print.assert_called_once_with(
        f"[{warning_style}]🚨 Both --riverpod[-r] and --bloc[-b] flags were provided. Please use only one. ✨"
    )
    mock_exit.assert_called_once_with(1)


@patch('sys.exit')
def test_setup_no_tags(mock_exit, setup_command):
    """Test the setup_no_tags method of SetupCommand."""
    setup_command.setup_no_tags()
    mock_exit.assert_called_once_with(0)
