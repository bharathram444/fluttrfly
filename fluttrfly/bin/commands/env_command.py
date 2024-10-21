import sys

import click

from ..commands.global_variables import (
    config_path,
)
from ..functions.common_functions import error_x, warning_x
from ..functions.env_functions import (
    check_for_updates,
    check_out_branch,
    env_check_up,
    environment_setup,
    fluttrfly_version_updates,
    update_and_pull_changes,
)
from ..functions.json_functions import (
    add_paths_process_msg_display,
    check_path_exists,
    load,
    set_env_path,
    write_specific_field,
)


class EnvCommand:
    def __init__(self):
        # Load initial configuration values
        (
            self.repo_url,
            self.environment_setup_done,
            self.repo_dir,
            self.env_version,
            self.messages,
        ) = load(config_path=config_path)

    def env_no_tags(self):
        if self.environment_setup_done:
            env_check_up(repo_dir=self.repo_dir, env_version=self.env_version, silence=False)
            check_for_updates(repo_dir=self.repo_dir, branch=self.env_version)
            sys.exit(0)
        else:
            main_repo_dir = environment_setup(repo_url=self.repo_url)
            check_out = check_out_branch(repo_dir=main_repo_dir, branch_name=self.env_version)
            add_paths_process_msg_display(
                main_repo_dir=main_repo_dir,
                check_out=check_out,
                env_version=self.env_version,
                repo_url=self.repo_url,
            )
            sys.exit(0)

    def env_version_tag(self):
        env_version_for_flag = load(config_path=config_path)[3]
        click.echo(f'FluttrFly env version: {env_version_for_flag}')
        sys.exit(0)

    def env_reset_tag(self):
        path_exists = check_path_exists(path=self.repo_dir, silence=False, force_off=False)
        if path_exists:
            check_out = check_out_branch(repo_dir=self.repo_dir, branch_name=self.env_version)
            if check_out is False:
                error_x(message="You have to set up env again using 'fluttrfly env --force'")
                sys.exit(1)

    def env_update_tag(self):
        check = check_path_exists(path=self.repo_dir, silence=False, force_off=False)
        if check:
            update_and_pull_changes(repo_dir=self.repo_dir, branch=self.env_version)
            fluttrfly_version_updates(messages=self.messages)

    def env_force_tag(self):
        """Force the setup of the environment, asking for user confirmation if necessary."""
        path_exists = check_path_exists(path=self.repo_dir, silence=False, force_off=True)
        if path_exists is None:
            sys.exit(0)
        if not path_exists:
            choice_home = input(
                "Do you want to set up existing fluttrfly env folder or directory path? (Y/n): "
            )
            if choice_home.lower() == 'y':
                present_repo_dir = set_env_path()
                if present_repo_dir is None:
                    error_x(message="Use 'fluttrfly env --force' to create the environment.")
                    exit(1)
                check_out = check_out_branch(
                    repo_dir=present_repo_dir, branch_name=self.env_version
                )
                add_paths_process_msg_display(
                    main_repo_dir=present_repo_dir,
                    check_out=check_out,
                    env_version=self.env_version,
                    repo_url=self.repo_url,
                )
            elif choice_home.lower() == 'n':
                self.prompt_for_recreation()
            else:
                error_x(message="Invalid choice. Exiting.")

    def prompt_for_recreation(self):
        """Prompt the user to recreate the fluttrfly environment if it already exists."""
        choice_location = input("Do you want to recreate fluttrfly env? (Y/n): ")
        if choice_location.lower() == 'y':
            # Update configuration to indicate the environment setup is not complete
            write_specific_field(
                config_path=config_path,
                field_name="environment_setup_done",
                field_value=False,
            )
            main_repo_dir = environment_setup(repo_url=self.repo_url)
            check_out = check_out_branch(repo_dir=main_repo_dir, branch_name=self.env_version)
            add_paths_process_msg_display(
                main_repo_dir=main_repo_dir,
                check_out=check_out,
                env_version=self.env_version,
                repo_url=self.repo_url,
            )
        elif choice_location.lower() == 'n':
            warning_x("Exiting. Please choose an option.")
        else:
            error_x(message="Invalid choice. Exiting.")
