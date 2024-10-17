from unittest.mock import patch

import pytest

from fluttrfly.bin.commands.env_command import EnvCommand

# Assuming the path to the functions and classes is 'fluttrfly.bin' (change accordingly)


@pytest.fixture
def mock_env_command():
    """Fixture to create a mock of EnvCommand class"""
    with patch(
        'fluttrfly.bin.commands.env_command.load',
        return_value=("repo_url", True, "repo_dir", "env_version", "messages"),
    ):
        return EnvCommand()


# Test the `env_no_tags` method when `environment_setup_done` is True
def test_env_no_tags_with_setup_done(mock_env_command):
    with patch('fluttrfly.bin.commands.env_command.env_check_up') as mock_env_check_up, patch(
        'fluttrfly.bin.commands.env_command.check_for_updates'
    ) as mock_check_for_updates, patch('sys.exit') as mock_sys_exit:

        mock_env_command.env_no_tags()

        mock_env_check_up.assert_called_once_with(
            repo_dir="repo_dir", env_version="env_version", silence=False
        )
        mock_check_for_updates.assert_called_once_with(repo_dir="repo_dir", branch="env_version")
        mock_sys_exit.assert_called_once_with(0)


# Test the `env_no_tags` method when `environment_setup_done` is False
def test_env_no_tags_without_setup_done(mock_env_command):
    mock_env_command.environment_setup_done = False
    with patch(
        'fluttrfly.bin.commands.env_command.environment_setup', return_value="main_repo_dir"
    ) as mock_env_setup, patch(
        'fluttrfly.bin.commands.env_command.check_out_branch', return_value="check_out"
    ) as mock_check_out_branch, patch(
        'fluttrfly.bin.commands.env_command.add_paths_process_msg_display'
    ) as mock_add_paths, patch(
        'sys.exit'
    ) as mock_sys_exit:

        mock_env_command.env_no_tags()

        mock_env_setup.assert_called_once_with(repo_url="repo_url")
        mock_check_out_branch.assert_called_once_with(
            repo_dir="main_repo_dir", branch_name="env_version"
        )
        mock_add_paths.assert_called_once_with(
            main_repo_dir="main_repo_dir",
            check_out="check_out",
            env_version="env_version",
            repo_url="repo_url",
        )
        mock_sys_exit.assert_called_once_with(0)


# Test `env_version_tag`


def test_env_version_tag(mock_env_command):
    # Mock the load function to return a specific env_version
    with patch(
        'fluttrfly.bin.commands.env_command.load',
        return_value=('repo_url', 'environment_setup_done', 'repo_dir', 'env_version', 'messages'),
    ), patch('click.echo') as mock_echo, patch('sys.exit') as mock_sys_exit:
        # Call the method
        mock_env_command.env_version_tag()

        # Assert the echo was called with the correct version
        mock_echo.assert_called_once_with('FluttrFly env version: env_version')
        # Ensure sys.exit was called
        mock_sys_exit.assert_called_once_with(0)


# Test `env_reset_tag` when path exists
def test_env_reset_tag(mock_env_command):
    with patch(
        'fluttrfly.bin.commands.env_command.check_path_exists', return_value=True
    ) as mock_check_path, patch(
        'fluttrfly.bin.commands.env_command.check_out_branch'
    ) as mock_check_out_branch:

        mock_env_command.env_reset_tag()

        mock_check_path.assert_called_once_with(path="repo_dir", silence=False, force_off=False)
        mock_check_out_branch.assert_called_once_with(
            repo_dir="repo_dir", branch_name="env_version"
        )


# Test `env_update_tag` when path exists
def test_env_update_tag(mock_env_command):
    with patch(
        'fluttrfly.bin.commands.env_command.check_path_exists', return_value=True
    ) as mock_check_path, patch(
        'fluttrfly.bin.commands.env_command.update_and_pull_changes'
    ) as mock_update_and_pull, patch(
        'fluttrfly.bin.commands.env_command.fluttrfly_version_updates'
    ) as mock_version_updates:

        mock_env_command.env_update_tag()

        mock_check_path.assert_called_once_with(path="repo_dir", silence=False, force_off=False)
        mock_update_and_pull.assert_called_once_with(repo_dir="repo_dir", branch="env_version")
        mock_version_updates.assert_called_once_with(messages="messages")


# Test `env_force_tag` when path doesn't exist
def test_env_force_tag_path_does_not_exist(mock_env_command):
    with patch(
        'fluttrfly.bin.commands.env_command.check_path_exists', return_value=False
    ) as mock_check_path, patch('builtins.input', return_value='y') as mock_input, patch(
        'fluttrfly.bin.commands.env_command.set_env_path', return_value="present_repo_dir"
    ) as mock_set_env_path, patch(
        'fluttrfly.bin.commands.env_command.check_out_branch', return_value="check_out"
    ) as mock_check_out_branch, patch(
        'fluttrfly.bin.commands.env_command.add_paths_process_msg_display'
    ) as mock_add_paths:

        mock_env_command.env_force_tag()

        mock_check_path.assert_called_once_with(path="repo_dir", silence=False, force_off=True)
        mock_input.assert_called_once_with(
            "Do you want to set up existing fluttrfly env folder or directory path? (Y/n): "
        )
        mock_set_env_path.assert_called_once()
        mock_check_out_branch.assert_called_once_with(
            repo_dir="present_repo_dir", branch_name="env_version"
        )
        mock_add_paths.assert_called_once_with(
            main_repo_dir="present_repo_dir",
            check_out="check_out",
            env_version="env_version",
            repo_url="repo_url",
        )
