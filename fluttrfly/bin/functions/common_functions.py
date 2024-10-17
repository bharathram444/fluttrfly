# common_functions.py
import socket
import time

import yaml

# Imports
from ..commands.global_variables import (
    console,
    error_style,
    success_style,
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


# loading animation
def with_loading(task, duration=1, status="Creating"):
    with console.status(f"[{success_style}]{status}..."):
        try:
            time.sleep(duration)
            task()
        except (FileNotFoundError, IsADirectoryError) as e:
            console.print(f"[{error_style}]📛 Error: {e} 😟")
            console.print(
                f"[{error_style}]📛 The configuration file is missing or the specified path is a directory. 😟"
            )
            console.print(
                f"[{error_style}]📛 Use 'fluttrfly env --force' to create the environment. 😟"
            )
            return None
        except Exception as e:
            console.print(f"[{error_style}]📛 An error occurred: {e}")


# CRUD of yaml


def read_yaml(file_path):
    """Reads a YAML file and returns the data."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def write_yaml(file_path, data):
    """Writes the updated data to the YAML file."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)
