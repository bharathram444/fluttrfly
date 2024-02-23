import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

# Assuming the code is part of a package named 'your_package'
from fluttrfly.bin.functions.env_functions import (
    check_for_updates,
    clone_repo_at_home,
    clone_repo_at_user_chosen_location,
    get_current_branch,
    is_internet_available,
)


def test_is_internet_available():
    assert is_internet_available() is True


@pytest.mark.parametrize(
    "host,port,timeout,expected_result",
    [
        ("8.8.8.8", 53, 5, True),
        ("192.168.1.1", 80, 3, False),
    ],
)
def test_is_internet_available_parametrized(host, port, timeout, expected_result):
    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.side_effect = OSError if not expected_result else None
        assert is_internet_available(host, port, timeout) is expected_result


@pytest.fixture
def repo_url():
    return "https://github.com/bharathram444/fclAssets.git"


def test_clone_repo_at_home_success(repo_url):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = None
        result = clone_repo_at_home(repo_url)
        assert result is not None
        mock_run.assert_called_once()


def test_clone_repo_at_home_failure(repo_url):
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            cmd="git clone", returncode=1, output="Error"
        )
        result = clone_repo_at_home(repo_url)
        assert result is None
        mock_run.assert_called_once()


def test_clone_repo_at_user_chosen_location_success(repo_url, mocker):
    mocker.patch("builtins.input", side_effect=["/user/location", "\n"])
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = None
        result = clone_repo_at_user_chosen_location(repo_url)
        assert result is not None
        mock_run.assert_called_once()


def test_clone_repo_at_user_choosed_location_failure():
    # Set up mock input to return an empty string
    with patch('builtins.input', return_value=''):
        # Call the function and assert that it returns None
        result = clone_repo_at_user_chosen_location(
            repo_url="https://github.com/bharathram444/fclAssets.git"
        )
        assert result is None


@pytest.fixture
def repo_dir():
    repo_dir = Path("n/fluttrflyenv/fclAssets")
    return repo_dir


def test_get_current_branch(repo_dir):
    # Create a mock git repository
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = b"main\n"

        # Call the function with a mock repo_dir
        current_branch = get_current_branch(repo_dir, silence=True)

        # Check if the function returns the correct current branch
        assert current_branch == "main"

        # Check if the function calls subprocess.check_output with the correct arguments
        mock_check_output.assert_called_once_with(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_dir
        )


def test_check_for_updates(repo_dir):
    # Create a mock git repository
    with patch("subprocess.check_output") as mock_check_output, patch(
        "subprocess.run"
    ) as mock_run:
        # Mock the output of 'git status -uno' to indicate updates are available
        mock_check_output.return_value = b"Your branch is behind 'origin/main'"

        # Call the function with a mock repo_dir and branch
        branch = "main"
        updates_available = check_for_updates(repo_dir, branch)

        # Check if the function returns True to indicate updates are available
        assert updates_available is True

        # Check if the function calls subprocess.check_output with the correct arguments
        mock_check_output.assert_called_once_with(["git", "status", "-uno"], cwd=repo_dir)

        # Check if the function calls subprocess.run with the correct arguments to fetch updates
        mock_run.assert_called_once_with(["git", "fetch"], cwd=repo_dir, check=True)


def test_check_for_updates_no_updates(repo_dir):
    # Create a mock git repository
    with patch("subprocess.check_output") as mock_check_output, patch(
        "subprocess.run"
    ) as mock_run:
        # Mock the output of 'git status -uno' to indicate no updates are available
        mock_check_output.return_value = b"Your branch is up to date with 'origin/main'"

        # Call the function with a mock repo_dir and branch
        branch = "main"
        updates_available = check_for_updates(repo_dir, branch)

        # Check if the function returns False to indicate no updates are available
        assert updates_available is False

        # Check if the function calls subprocess.check_output with the correct arguments
        mock_check_output.assert_called_once_with(["git", "status", "-uno"], cwd=repo_dir)

        # Check if the function calls subprocess.run with the correct arguments to fetch updates
        mock_run.assert_called_once_with(["git", "fetch"], cwd=repo_dir, check=True)
