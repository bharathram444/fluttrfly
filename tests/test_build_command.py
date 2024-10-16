import pytest
from pathlib import Path
from fluttrfly.bin.commands.build_command import BuildCommand

# Mocking functions and global variables used in the BuildCommand class
from fluttrfly.bin.commands.global_variables import (
    console,
    error_style,
    warning_style,
    libString,
)


@pytest.fixture
def mock_load(mocker):
    # Mock the load function to return a valid configuration
    return mocker.patch(
        'fluttrfly.bin.functions.json_functions.load',
        return_value=('repo_url', True, 'repo_dir', 'env_version', 'messages'),
    )


@pytest.fixture
def mock_env_check(mocker):
    return mocker.patch('fluttrfly.bin.functions.env_functions.env_check_up')


@pytest.fixture
def mock_with_loading(mocker):
    return mocker.patch('fluttrfly.bin.functions.common_functions.with_loading')


@pytest.fixture
def build_command():
    return BuildCommand()


# def test_build_no_tags(build_command, mocker):
#     # Mock sys.exit to prevent the test from exiting
#     mocker.patch('sys.exit')

#     # Mock the show_build_command_lines function
#     mock_show_build = mocker.patch(
#         'fluttrfly.bin.functions.build_functions.show_build_command_lines'
#     )

#     # Call the method
#     build_command.build_no_tags()

#     # Assert that show_build_command_lines was called and sys.exit was called
#     mock_show_build.assert_called_once()
#     mocker.patch('sys.exit')  # Use mocker to avoid actual exit


def test_build_module_tag_invalid_dir(build_command, mocker):
    mocker.patch('sys.exit')

    # Mock Path.cwd() to simulate that we're not in the 'lib' directory
    mocker.patch('pathlib.Path.cwd', return_value=Path("/wrong/directory"))

    # Mock the console output
    mock_console = mocker.patch.object(console, 'print')

    build_command.build_module_tag(module="my_module")

    # Ensure the correct warning is printed and no further action is taken
    mock_console.assert_called_with(
        f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory."
    )


# def test_build_module_tag_valid_module(build_command, mocker, mock_with_loading):
#     # Mock Path.cwd() to simulate we're in the 'lib' directory
#     mocker.patch('pathlib.Path.cwd', return_value=Path(f"/some/path{libString}"))

#     # Call the method with a valid module name
#     build_command.build_module_tag(module="my_module")

#     # Ensure with_loading was called
#     mock_with_loading.assert_called_once()



def test_build_module_tag_invalid_module(build_command, mocker):
    # Mock Path.cwd() to simulate we're in the 'lib' directory
    mocker.patch('pathlib.Path.cwd', return_value=Path(f"/some/path{libString}"))

    # Mock the console output
    mock_console = mocker.patch.object(console, 'print')

    # Call the method with an invalid module (numeric)
    build_command.build_module_tag(module="123")

    # Ensure the correct error message is printed
    mock_console.assert_called_with(
        f"[{error_style}]📛 ModuleName argument must be a non-numeric string."
    )

# def test_build_assets_tag_valid(build_command, mocker, mock_with_loading):
#     # Mock Path.cwd() to simulate the current directory
#     mocker.patch('pathlib.Path.cwd', return_value=Path("/some/valid/directory"))
    
#     # Mock (Path.cwd() / 'assets').exists() to return False
#     mocker.patch('pathlib.Path.exists', side_effect=lambda: False)

#     # Call the method
#     build_command.build_assets_tag()

#     # Ensure with_loading was called
#     mock_with_loading.assert_called_once_with(mock.ANY)



def test_build_assets_tag_already_exists(build_command, mocker):
    # Mock Path.cwd() to simulate we're outside the 'lib' directory
    mocker.patch('pathlib.Path.cwd', return_value=Path("/some/valid/directory"))

    # Mock (Path.cwd() / 'assets').exists() to return True (assets directory exists)
    mocker.patch('pathlib.Path.exists', return_value=True)

    # Mock the console output
    mock_console = mocker.patch.object(console, 'print')

    build_command.build_assets_tag()

    # Ensure the correct warning is printed
    mock_console.assert_called_with(
        f"[{warning_style}]🚨 Assets structure already exists. No changes made."
    )


# def test_build_core_tag_valid(build_command, mocker):
#     # Mock Path.cwd() to simulate we're in the 'lib' directory
#     mocker.patch('pathlib.Path.cwd', return_value=Path(f"/some/path{libString}"))

#     # Mock (Path.cwd() / 'core').exists() to return False
#     mock_core_structure = mocker.patch('fluttrfly.bin.functions.build_functions.to_create_core_structure')
#     mocker.patch('pathlib.Path.exists', side_effect=lambda: False)

#     # Call the method
#     build_command.build_core_tag()

#     # Ensure the core structure is created
#     mock_core_structure.assert_called_once()



def test_build_core_tag_already_exists(build_command, mocker):
    # Mock (Path.cwd() / 'core').exists() to return True (core directory exists)
    mocker.patch('pathlib.Path.exists', return_value=True)

    # Mock the console output
    mock_console = mocker.patch.object(console, 'print')

    build_command.build_core_tag()

    # Ensure the correct warning is printed
    mock_console.assert_called_with(
        f"[{warning_style}]🚨 Core structure already exists. No changes made."
    )
