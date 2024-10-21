# global_variables.py


import importlib.metadata as metadata
import importlib.resources
from pathlib import Path

from rich.console import Console
from rich.style import Style

# global variables
package_name = "fluttrfly"
fluttrfly_path = importlib.resources.files(package_name)
config_path = fluttrfly_path / "assets/config.json"
current_directory = Path.cwd()
fluttrfly_version = metadata.version("fluttrfly")
console = Console()

# consts
lib_string = "/lib"

# Define styles for messages
error_style = Style(color="red", bold=True)
success_style = Style(color="green", bold=True)
warning_style = Style(color="yellow", bold=True)
info_style = Style(color="cyan", bold=True)

branch_colors = {
    "audio": "yellow",
    "images": "magenta",
    "video": "cyan",
    "data": "orange_red1",
    "others": "red",
}

#  "repo_url": "https://github.com/bharathram444/fclAssets.git"


# flutter_cli/
# ├── fluttrfly/
# │   ├── assets/
# │   │   └── config.json
# │   └── bin/
# │       ├── __pycache__/
# │       ├── commands/
# │       │   ├── __pycache__/
# │       │   ├── __init__.py
# │       │   └── command_lines.py
# │       ├── functions/
# │       │   ├── __pycache__/
# │       │   ├── __init__.py
# │       │   ├── build_functions.py
# │       │   ├── env_functions.py
# │       │   └── json_functions.py
# │       ├── variables/
# │       │   ├── __pycache__/
# │       │   ├── __init__.py
# │       │   └── global_variables.py
# │       ├── __init__.py
# │       └── entry.py
# ├── fluttrfly.egg-info/
# ├── .gitignore
# ├── LICENSE
# ├── README.md
# └── setup.py


# we have to add this below two lines to message.txt when fluttrfly version incremented

# new fluttrfly 1.1.0 version is released.
# use - 'pip install --upgrade fluttrfly' to update.

# If you're making bug fixes, it would be 1.9.1.
# If you're adding new features, it would be 1.10.0.
# If you're making major, breaking changes, it might be 2.0.0.


# {
#     "repo_dir": "/home/bharath/to_test_force/fclenv/fclAssets",
#     "assets": "/home/bharath/to_test_force/fclenv/fclAssets/assets",
#     "core": "/home/bharath/to_test_force/fclenv/fclAssets/assets/flutter_things/lib/core",
#     "fonts": "/home/bharath/to_test_force/fclenv/fclAssets/assets/fonts",
#     "templates": "/home/bharath/to_test_force/fclenv/fclAssets/assets/templates",
#     "messages":"/home/bharath/to_test_force/fclenv/fclAssets/assets/messages",
#     "environment_setup_done": true,
#     "env_version": "1.0.0",
#     "repo_url": "https://github.com/bharathram444/fclAssets.git"
# }


# .
# ├── fluttrfly
# │   ├── assets
# │   │   └── config.json
# │   ├── bin
# │   │   ├── commands
# │   │   │   ├── command_lines.py
# │   │   │   ├── command_manager.py
# │   │   │   └── __init__.py
# │   │   ├── entry.py
# │   │   ├── functions
# │   │   │   ├── build_functions.py
# │   │   │   ├── env_functions.py
# │   │   │   ├── __init__.py
# │   │   │   ├── json_functions.py
# │   │   │   └── __pycache__
# │   │   │       ├── build_functions.cpython-311.pyc
# │   │   │       ├── env_functions.cpython-311.pyc
# │   │   │       ├── __init__.cpython-311.pyc
# │   │   │       └── json_functions.cpython-311.pyc
# │   │   ├── __init__.py
# │   │   ├── __pycache__
# │   │   │   └── __init__.cpython-311.pyc
# │   │   └── variables
# │   │       ├── global_variables.py
# │   │       ├── __init__.py
# │   │       └── __pycache__
# │   │           ├── global_variables.cpython-311.pyc
# │   │           └── __init__.cpython-311.pyc
# │   ├── __init__.py
# │   └── __pycache__
# │       └── __init__.cpython-311.pyc
# ├── LICENSE
# ├── poetry.lock
# ├── pyproject.toml
# ├── README.md
# └── tests
#     ├── __init__.py
#     ├── __pycache__
#     │   ├── __init__.cpython-311.pyc
#     │   ├── test_build_functions.cpython-311-pytest-8.0.1.pyc
#     │   ├── test_env_functions.cpython-311-pytest-8.0.1.pyc
#     │   └── test_json_functions.cpython-311-pytest-8.0.1.pyc
#     ├── test_build_functions.py
#     ├── test_env_functions.py
#     └── test_json_functions.py

# 13 directories, 33 files
