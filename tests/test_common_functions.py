from unittest.mock import MagicMock, mock_open, patch

import yaml

# Import the common functions
from fluttrfly.bin.functions.common_functions import (
    is_internet_available,
    read_yaml,
    with_loading,
    write_yaml,
)


# Test for is_internet_available
def test_is_internet_available_success():
    with patch('socket.create_connection') as mock_create_connection:
        mock_create_connection.return_value = True
        assert is_internet_available() is True
        mock_create_connection.assert_called_once_with(('8.8.8.8', 53), timeout=5)


# Test for with_loading
def test_with_loading_success():
    mock_task = MagicMock()
    with patch('time.sleep', return_value=None), patch(
        'fluttrfly.bin.commands.global_variables.console.status'
    ) as mock_status:
        with_loading(mock_task, duration=1, status="Creating")
        mock_status.assert_called_once()


def test_with_loading_file_not_found():
    mock_task = MagicMock(side_effect=FileNotFoundError("File not found"))
    with patch('time.sleep', return_value=None), patch(
        'fluttrfly.bin.commands.global_variables.console.print'
    ) as mock_console_print:
        with_loading(mock_task, duration=1, status="Creating")
        mock_console_print.assert_any_call("[bold red]📛 Error: File not found 😟")
        mock_console_print.assert_any_call(
            "[bold red]📛 The configuration file is missing or the specified path is a directory. 😟"
        )


def test_with_loading_general_exception():
    mock_task = MagicMock(side_effect=Exception("General error"))
    with patch('time.sleep', return_value=None), patch(
        'fluttrfly.bin.commands.global_variables.console.print'
    ) as mock_console_print:
        with_loading(mock_task, duration=1, status="Creating")
        mock_console_print.assert_called_with("[bold red]📛 An error occurred: General error")


# Test for read_yaml
def test_read_yaml():
    mock_data = {'key': 'value'}
    with patch('builtins.open', mock_open(read_data=yaml.dump(mock_data))):
        result = read_yaml('dummy_path.yaml')
        assert result == mock_data


# Test for write_yaml
def test_write_yaml():
    mock_data = {'key': 'value'}
    with patch('builtins.open', mock_open()) as mock_file:
        with patch('yaml.dump') as mock_yaml_dump:
            write_yaml('dummy_path.yaml', mock_data)
            mock_file.assert_called_once_with('dummy_path.yaml', 'w')
            mock_yaml_dump.assert_called_once_with(
                mock_data, mock_file(), default_flow_style=False, sort_keys=False
            )
