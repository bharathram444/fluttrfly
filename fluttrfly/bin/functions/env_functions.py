# env_functions.py

import socket
import subprocess
import sys
from pathlib import Path

# Imports
from ..functions.json_functions import check_path_exists
from ..variables.global_variables import (
    console,
    error_style,
    fluttrfly_version,
    info_style,
    success_style,
    warning_style,
)

## Internet check @


def is_internet_available(host="8.8.8.8", port=53, timeout=5):
    try:
        # Try creating a socket connection to the specified host and port
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        console.print(
            f"[{error_style}]📛 No internet connection. Please check your connection and try again. 😟"
        )
        return False


## fluttrfly version updates @
def fluttrfly_version_updates(messages):
    message_path = Path(messages) / "message.txt"
    try:
        with message_path.open("r") as message_file:
            message = message_file.read().strip()
            if message:
                console.print(f"[{info_style}]ℹ️ {message} ℹ️", style=info_style)
            else:
                print("")
    except FileNotFoundError:
        console.print(f"[{info_style}]📛 Message file not found ℹ️", style=info_style)
    except Exception as e:
        console.print(f"[{info_style}]📛 Error reading message file: {e} ℹ️", style=info_style)


## env functions @


def clone_repo_at_home(repo_url):
    try:
        user_home = Path.home()
        repo_dir = user_home / Path(repo_url.rstrip('.git')).name
        subprocess.run(["git", "clone", repo_url, str(repo_dir)], check=True)
        console.print(f"[{success_style}]✅ Repository cloned successfully to: {repo_dir} ✨")
        return repo_dir
    except subprocess.CalledProcessError as error:
        console.print(f"[{error_style}]📛 Error cloning repository: {error} 😟")
        return None


def clone_repo_at_user_chosen_location(repo_url):
    try:
        console.print(
            "[bold]To set up the environment, let's choose a location for the fluttrflyenv repository.[/bold]"
        )
        console.print("[bold]Please follow these steps:[/bold]")
        console.print(
            "[bold cyan]1.[/bold cyan] [italic]Choose or navigate to a specific folder.[/italic]"
        )
        console.print(
            "[bold cyan]2.[/bold cyan] [italic]Create a new folder and give it a name.[/italic]"
        )
        console.print(
            "[bold cyan]3.[/bold cyan] [italic]Copy the complete path of the newly created folder.[/italic]"
        )
        console.print(
            "[bold cyan]4.[/bold cyan] [italic]Paste the path below when prompted.[/italic]"
        )

        user_chosen_location = input("Enter the path to create the environment:")

        if user_chosen_location:
            user_chosen_location_path = Path(user_chosen_location)
            repo_dir = user_chosen_location_path / Path(repo_url.rstrip('.git')).name
            subprocess.run(["git", "clone", repo_url, str(repo_dir)], check=True)
            return repo_dir
        else:
            console.print(
                "[{warning_style}]🚨 Exiting, the provided path is empty. Please provide a valid path. ✨",
                style=warning_style,
            )
            return None
    except subprocess.CalledProcessError as error:
        console.print(f"[{error_style}]📛 Error cloning repository: {error} 😟")
        console.print("Using a default directory as a fallback.")
        return None


def git_stash(repo_dir):
    try:
        subprocess.run(["git", "stash"], cwd=repo_dir, check=True)
        console.print(f"[{success_style}]✅ Changes stashed successfully. ✨")
        return True
    except subprocess.CalledProcessError as error:
        console.print(f"[{error_style}]📛 Error stashing changes: {error} 😟")
        return False


def reset_and_clean(repo_dir):
    try:
        subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=repo_dir, check=True)
        subprocess.run(["git", "clean", "-fd"], cwd=repo_dir, check=True)
        console.print(f"[{success_style}]✅ Local changes reset and cleaned successfully. ✨")
        return True
    except subprocess.CalledProcessError as error:
        console.print(f"[{error_style}]📛 Error resetting and cleaning: {error} 😟")
        return False


def pull_commits(repo_dir, branch_name):
    try:
        git_stash(repo_dir)
        subprocess.run(["git", "pull", "origin", branch_name], cwd=repo_dir, check=True)
        console.print(f"[{success_style}]✅ Updates pulled successfully. ✨")
        return True
    except subprocess.CalledProcessError as error:
        console.print(f"[{error_style}]📛 Error pulling updates: {error} 😟")
        return False


def check_for_updates(repo_dir, branch):
    try:
        if not is_internet_available():
            return False
        # Fetch updates from the remote repository
        subprocess.run(["git", "fetch"], cwd=repo_dir, check=True)

        # Check if the local branch is behind the remote branch
        output = subprocess.check_output(["git", "status", "-uno"], cwd=repo_dir)

        if f"Your branch is behind 'origin/{branch}'" in output.decode():
            console.print(f"[{warning_style}]🚨 Updates available for env {branch} ✨")
            console.print(
                f"[{info_style}]🛠️  The environment is already set up. You can update it using 'fluttrfly env --update'. 🛠️",
                style=info_style,
            )
            return True
        else:
            console.print(f"[{success_style}]✅ No updates available for env {branch} ✨")
            return False
    except subprocess.CalledProcessError as error:
        # Check if the error message indicates an internet connection issue
        if "Could not resolve host" in str(error):
            console.print(f"[{error_style}]📛 Error checking for updates: {error} 😟")
            console.print(f"[{error_style}]📛 Check your internet connection and try again. 😟")
        else:
            console.print(f"[{error_style}]📛 Error checking for updates: {error} 😟")
        return False


def get_current_branch(repo_dir, silence):
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_dir
        )
        current_branch = output.decode().strip()
        if not silence:
            console.print(f"[{success_style}]✅ Current branch: {current_branch} ✨")
        return current_branch
    except subprocess.CalledProcessError as error:
        console.print(f"[{error_style}]📛 Error getting current branch: {error} 😟")
        return None


def check_out_branch(repo_dir, branch_name):
    try:
        git_stash(repo_dir)
        subprocess.run(["git", "checkout", branch_name], cwd=repo_dir, check=True)
        console.print(f"[{success_style}]✅ Checked out to branch: {branch_name} ✨")
        return True
    except subprocess.CalledProcessError as error:
        console.print(f"[{error_style}]📛 Error checking out branch: {error} 😟")
        return False


def environment_setup(repo_url):
    repo_dir = None  # Initialize repo_dir
    choice_home = input(
        "Do you want to set up fluttrfly env in your home folder or directory? (Y/n): "
    )
    if choice_home.lower() == 'y':
        repo_dir = clone_repo_at_home(repo_url=repo_url)
    elif choice_home.lower() == 'n':
        choice_location = input(
            "Do you have a specific folder or directory in mind to set up fluttrfly env? (Y/n): "
        )
        if choice_location.lower() == 'y':
            repo_dir = clone_repo_at_user_chosen_location(repo_url=repo_url)
        elif choice_location.lower() == 'n':
            console.print(
                "[{warning_style}]🚨 Exiting. Please choose a setup option. ✨",
                style=warning_style,
            )
        else:
            console.print("[{error_style}]📛 Invalid choice. Exiting. 😟", style=error_style)
    else:
        console.print("[{error_style}]📛 Invalid choice. Exiting. 😟", style=error_style)

    return repo_dir


def update_and_pull_changes(repo_dir, branch):
    current_env_branch = get_current_branch(repo_dir=repo_dir, silence=False)
    if current_env_branch != branch:
        check_out_branch(repo_dir=repo_dir, branch_name=branch)
    local_changes_removed = reset_and_clean(repo_dir=repo_dir)
    if local_changes_removed:
        check = check_for_updates(repo_dir=repo_dir, branch=branch)
        if check:
            pull_commits(repo_dir=repo_dir, branch_name=branch)
            console.print(
                f"[{info_style}]✨ You're all set! Happy coding with fluttrfly v{fluttrfly_version} and env v{current_env_branch}! ✨",
                style=info_style,
            )


def env_check_up(repo_dir, env_version, silence):
    path_exists = check_path_exists(path=repo_dir, silence=silence, force_off=False)
    if path_exists:
        current_env_branch = get_current_branch(repo_dir=repo_dir, silence=silence)

        if current_env_branch is None:
            console.print(
                f"[{error_style}]📛 You have to set up env again using 'fluttrfly env --force' 😟"
            )
            sys.exit(1)
        if env_version == current_env_branch:
            if not silence:
                console.print(
                    f"[{info_style}]✨ You're all set! Happy coding with fluttrfly v{fluttrfly_version} and env v{env_version}! ✨",
                    style=info_style,
                )
        if env_version != current_env_branch:
            console.print(
                f"[{info_style}]ℹ️  The env (v{current_env_branch}) != fluttrfly v{fluttrfly_version}. ℹ️",
                style=info_style,
            )
            console.print(
                f"[{error_style}]📛 You have to reset env using 'fluttrfly env --reset' 😟"
            )
            sys.exit(1)
    elif not path_exists:
        sys.exit(1)
