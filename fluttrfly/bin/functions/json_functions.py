import json
import sys
from pathlib import Path

# Imports
from ..commands.global_variables import (
    config_path,
    console,
    fluttrfly_version,
)
from ..functions.common_functions import error_x, info_x, success_x, warning_x


def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, IsADirectoryError) as e:
            error_x(message=f"Error: {e}")
            error_x(
                message="The configuration file is missing or the specified path is a directory."
            )
            error_x(message="Use 'fluttrfly env --force' to create the environment.")
            return None
        except Exception as e:
            error_x(message=f"Error: {e}")
            return None

    return wrapper


@handle_exception
def write_config(config_path, data):
    with open(config_path, "w") as config_file:
        json.dump(data, config_file, indent=4)


@handle_exception
def read_config(config_path):
    with open(config_path, "r") as config_file:
        return json.load(config_file)


@handle_exception
def write_specific_field(config_path, field_name, field_value):
    config_data = read_config(config_path)
    config_data[field_name] = field_value
    write_config(config_path, config_data)


@handle_exception
def load(config_path):
    config_data = read_config(config_path=config_path)
    if config_data:
        return (
            config_data.get("repo_url", "https://github.com/bharathram444/fluttrflyEnv.git"),
            config_data.get("environment_setup_done", False),
            config_data.get("repo_dir", ""),
            config_data.get("env_version", "2.0.0"),
            config_data.get("messages", ""),
        )
    return "https://github.com/bharathram444/fluttrflyEnv.git", False, "", "", ""


@handle_exception
def all_paths_get(config_path):
    path_data = read_config(config_path=config_path)
    if path_data:
        return (
            path_data.get("repo_dir", ""),
            path_data.get("env", ""),
            path_data.get("assets", ""),
            path_data.get("bloc_setup", ""),
            path_data.get("riverpod_setup", ""),
            path_data.get("fonts", ""),
            path_data.get("templates", ""),
            path_data.get("messages", ""),
        )
    return "", "", "", "", "", "", "", ""


def check_path_exists(path: str, silence, force_off):
    try:
        if path == "":
            error_x(message="Environment not set up. Run 'fluttrfly env' first.")
            return None
        if Path(path).exists():
            if not silence:
                success_x(message=f"Path '{path}' exists.")
            return True
        else:
            error_x(message=f"Path '{path}' does not exist.")
            if not force_off:
                error_x(message="You have to set up env again using 'fluttrfly env --force'")
            return False
    except Exception as e:
        print(f"Error checking path: {e}")
        return False


@handle_exception
def check_paths_in_config(config_path):
    repo_dir, env, assets, bloc_setup, riverpod_setup, fonts, templates, messages = all_paths_get(
        config_path
    )

    paths_to_check = [
        repo_dir,
        env,
        assets,
        bloc_setup,
        riverpod_setup,
        fonts,
        templates,
        messages,
    ]

    for path in paths_to_check:
        result = check_path_exists(path, silence=False, force_off=False)
        if result is None or not result:
            return False
    return True


def add_paths_process_msg_display(main_repo_dir, check_out, env_version, repo_url):
    if main_repo_dir is None:
        if check_out is False:
            # Error setting up the environment
            write_config(
                config_path=config_path,
                data={
                    "repo_dir": "",
                    "environment_setup_done": False,
                    "env_version": "2.0.0",
                    "repo_url": "https://github.com/bharathram444/fluttrflyEnv.git",
                },
            )
            error_x(message="Error setting up the environment. Please try again.")
            sys.exit(1)

    write_config(
        config_path=config_path,
        data={
            "repo_dir": str(main_repo_dir),
            "env": str(main_repo_dir) + "/env",
            "assets": str(main_repo_dir) + "/env/assets",
            "bloc_setup": str(main_repo_dir) + "/env/assets/flutter_assets/bloc_setup",
            "riverpod_setup": str(main_repo_dir) + "/env/assets/flutter_assets/riverpod_setup",
            "fonts": str(main_repo_dir) + "/env/assets/fonts",
            "templates": str(main_repo_dir) + "/env/assets/templates",
            "messages": str(main_repo_dir) + "/env/messages",
            "environment_setup_done": True,
            "env_version": env_version,
            "repo_url": repo_url,
        },
    )

    if main_repo_dir is not None:
        # Additional messages
        success_x(message="Environment set up successfully!")
        info_x(
            message=f"The environment (v{env_version}) has been set up and linked to fluttrfly v{fluttrfly_version}."
        )
        info_x(message="Paths linked to fluttrfly from the environment:")
        console.print(f"   • Repo Directory: {str(main_repo_dir)}")
        console.print(f"   • Environment : {str(main_repo_dir)}/env")
        console.print(f"   • Assets: {str(main_repo_dir)}/env/assets")
        console.print(f"   • Flutter Assets: {str(main_repo_dir)}/env/assets/flutter_assets")
        console.print(f"   • Fonts: {str(main_repo_dir)}/env/assets/fonts")
        console.print(f"   • Templates: {str(main_repo_dir)}/env/assets/templates")
        console.print(f"   • messages: {str(main_repo_dir)}/env/messages")
        warning_x(message="Important: Do not modify the structure of the environment or move it!")
        warning_x(message="Avoid moving or deleting folders within the environment.")
        warning_x(message="Avoid changing branches manually within the environment.")
        warning_x(message="Any unauthorized changes may lead to fluttrfly malfunction.")
        info_x(
            message=f"You're all set! Happy coding with fluttrfly v{fluttrfly_version} and env v{env_version}!"
        )


def set_env_path():
    try:
        console.print("[bold]To set up the existing environment path.[/bold]")
        console.print("[bold]Please follow these steps:[/bold]")
        console.print(
            "[bold cyan]1.[/bold cyan] [italic]Navigate to folder were you moved env.[/italic]"
        )
        console.print(
            "[bold cyan]2.[/bold cyan] [italic]go deeper were 'fluttrflyEnv' folder present.[/italic]"
        )
        console.print(
            "[bold cyan]3.[/bold cyan] [italic]Copy the complete path of the 'fluttrflyEnv' folder.[/italic]"
        )
        console.print(
            "[bold cyan]4.[/bold cyan] [italic]Paste the path below when prompted.[/italic]"
        )
        repo_dir = input("Enter the path to the fluttrfly env folder: ")
        real_repo_dir = check_path_exists(path=repo_dir, silence=False, force_off=True)
        if real_repo_dir:
            result = paths_check_up(repo_dir)
            if result:
                return repo_dir
            else:
                return None
        if real_repo_dir is None or not real_repo_dir:
            raise FileNotFoundError
    except FileNotFoundError:
        error_x(message=f"Path '{repo_dir}' does not exist. Please provide a valid path. 😟")
        return None
    except Exception as e:
        error_x(message=f"An error occurred: {e}")
        return None


def paths_check_up(repo_dir):
    paths = [
        f"{str(repo_dir)}/env",
        f"{str(repo_dir)}/env/assets",
        f"{str(repo_dir)}/env/assets/flutter_assets/bloc_setup",
        f"{str(repo_dir)}/env/assets/flutter_assets/bloc_setup/assets",
        f"{str(repo_dir)}/env/assets/flutter_assets/bloc_setup/lib",
        f"{str(repo_dir)}/env/assets/flutter_assets/bloc_setup/packages",
        f"{str(repo_dir)}/env/assets/flutter_assets/bloc_setup/packages/fluttrfly",
        f"{str(repo_dir)}/env/assets/flutter_assets/riverpod_setup",
        f"{str(repo_dir)}/env/assets/flutter_assets/riverpod_setup/assets",
        f"{str(repo_dir)}/env/assets/flutter_assets/riverpod_setup/lib",
        f"{str(repo_dir)}/env/assets/flutter_assets/riverpod_setup/packages",
        f"{str(repo_dir)}/env/assets/flutter_assets/riverpod_setup/packages/fluttrfly",
        f"{str(repo_dir)}/env/assets/fonts",
        f"{str(repo_dir)}/env/assets/templates",
        f"{str(repo_dir)}/env/messages/",
    ]
    for path in paths:
        result = check_path_exists(path, silence=False, force_off=True)
        if result is None or not result:
            error_x(message="Please provide a valid path of fluttrflyenv. (or)")
            return False
    return True
