import sys
from pathlib import Path

from ..commands.global_variables import (
    config_path,
    console,
    error_style,
    libString,
    warning_style,
)
from ..functions.build_functions import (
    show_build_command_lines,
    to_create_assets_structure,
    to_create_core_structure,
    to_create_module_structure,
)
from ..functions.common_functions import with_loading
from ..functions.env_functions import env_check_up
from ..functions.json_functions import load


class BuildCommand:
    def __init__(self):
        # Load initial configuration values
        (
            self.repo_url,
            self.environment_setup_done,
            self.repo_dir,
            self.env_version,
            self.messages,
        ) = load(config_path=config_path)
        # Check if the environment is set up
        if not self.environment_setup_done:
            console.print(
                f"[{error_style}]📛 Environment not set up. Run 'fluttrfly env' first. 😟",
            )
            sys.exit(1)
        env_check_up(repo_dir=self.repo_dir, env_version=self.env_version, silence=True)

    def build_no_tags(self):
        show_build_command_lines()
        sys.exit(0)

    def build_module_tag(self, module):
        if not module.isdigit():
            if libString in Path.cwd().as_posix():
                with_loading(task=lambda: to_create_module_structure(module))
            else:
                console.print(
                    f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory.",
                )
        else:
            console.print(
                f"[{error_style}]📛 ModuleName argument must be a non-numeric string.",
            )
            if libString not in Path.cwd().as_posix():
                console.print(
                    f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory.",
                )

    def build_assets_tag(self):
        if libString in Path.cwd().as_posix():
            console.print(
                f"[{warning_style}]🚨 Incorrect directory: Please run this command outside the 'lib' directory.",
            )
            sys.exit(1)
        elif (Path.cwd() / 'assets').exists():
            console.print(
                f"[{warning_style}]🚨 Assets structure already exists. No changes made.",
            )

        else:
            with_loading(lambda: to_create_assets_structure())

    def build_core_tag(self):
        if (Path.cwd() / 'core').exists():
            console.print(
                f"[{warning_style}]🚨 Core structure already exists. No changes made.",
            )
        elif "/lib" in Path.cwd().as_posix():
            to_create_core_structure()
        else:
            console.print(
                f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory.",
            )
            sys.exit(1)
