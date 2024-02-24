import argparse
import sys
from pathlib import Path

# Import functions and global variables
from ..functions.build_functions import (
    show_build_command_lines,
    to_create_assets_structure,
    to_create_core_structure,
    to_create_module_structure,
    with_loading,
)
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
from ..variables.global_variables import (
    config_path,
    console,
    error_style,
    fluttrfly_version,
    warning_style,
)


def main():
    ## Updates Note @

    #    print("we have to access in fluttrfly")
    #    print("test note.... We have to create one updates.txt to give updates like new fluttrfly version released")
    #    print("we should not access in fluttrfly")
    #    print("and. We have to create one fluttrfly_developers_to_users.txt to give instructions about fluttrfly env and fluttrfly .")

    ## Argparse Initialization @
    # Main parser
    epilog = """
    Say goodbye to repetitive setup tasks and focus on your coding magic!
    """
    parser = argparse.ArgumentParser(
        description="CLI to streamline the development process for Flutter projects.",
        epilog=epilog,
    )

    # Sub parser
    subparser = parser.add_subparsers(dest="command")

    ## All command lines used in CLI @

    ## Sub parser build @@

    env_parser = subparser.add_parser(
        "env",
        help="To create fluttrfly environment.",
        description="How to use ? Ans : fluttrfly env --update",
    )

    ## Sub parser build @@

    build_parser = subparser.add_parser(
        "build",
        help="Build various project structures like modules, assets, and core.",
        description="How to use ? Ans : fluttrfly build --core",
    )

    ## Sub parser add @@

    # add command line is used to build particular widgets
    # ex : button call as --add button , dropdown call as --add dropdown , many more (or) ect...

    ## Independent Command Line to know Version @

    # version Flag Arguments
    parser.add_argument(
        "-v",
        "--version",
        help="Print the version information.",
        action="version",
        version="%(prog)s " + fluttrfly_version,
    )

    ## Command Lines of env @

    # env version Flag Arguments
    env_version_for_flag = load(config_path=config_path)[3]
    env_parser.add_argument(
        "-v",
        "--version",
        help="to print version",
        action="version",
        version="%(prog)s " + env_version_for_flag,
    )
    # update Flag Arguments
    env_parser.add_argument(
        "-u", "--update", help="to update env", action="store_true", default=False
    )

    # reset Flag Arguments
    env_parser.add_argument(
        "-r",
        "--reset",
        help="to equalize env's version and fluttrfly's version",
        action="store_true",
        default=False,
    )

    # force Flag Arguments
    env_parser.add_argument(
        "-f", "--force", help="to create env forcibly", action="store_true", default=False
    )

    ## Command Lines of build @

    # modules Positional Arguments
    build_parser.add_argument(
        "-m",
        "--module",
        help="to build structured module",
        metavar="Module",
        dest="module",
        type=str,
    )

    # assets Flag Arguments
    build_parser.add_argument(
        "-a", "--assets", help="to build structured assets", action="store_true", default=False
    )

    # core Flag Arguments
    build_parser.add_argument(
        "-c", "--core", help="to build core", action="store_true", default=False
    )

    ## Command Lines of add @

    # here we have to add arguments of ' add '

    ## Parse the arguments @
    args = parser.parse_args()

    ## Use the arguments in your code @

    ## code of argument 'fluttrfly' @

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    ## code of argument 'fluttrfly env' @

    if args.command == "env":

        if len(sys.argv) == 2:
            repo_url, environment_setup_done, repo_dir, env_version, messages = load(
                config_path=config_path
            )

            if environment_setup_done:
                env_check_up(repo_dir=repo_dir, env_version=env_version, silence=False)
                check_for_updates(repo_dir=repo_dir, branch=env_version)
                sys.exit(0)
            if not environment_setup_done:
                main_repo_dir = environment_setup(repo_url=repo_url)
                check_out = check_out_branch(repo_dir=main_repo_dir, branch_name=env_version)
                add_paths_process_msg_display(
                    main_repo_dir=main_repo_dir,
                    check_out=check_out,
                    env_version=env_version,
                    repo_url=repo_url,
                )
                sys.exit(0)
        repo_url, environment_setup_done, repo_dir, env_version, messages = load(
            config_path=config_path
        )
        if args.reset:
            path_exists = check_path_exists(path=repo_dir, silence=False, force_off=False)
            if path_exists:
                check_out_branch(repo_dir=repo_dir, branch_name=fluttrfly_version)

        if args.update:
            check = check_path_exists(path=repo_dir, silence=False, force_off=False)
            if check:
                update_and_pull_changes(repo_dir=repo_dir, branch=env_version)
                fluttrfly_version_updates(messages=messages)
        if args.force:
            path_exists = check_path_exists(path=repo_dir, silence=False, force_off=True)
            if not path_exists:
                choice_home = input(
                    "Do you want to set up existing fluttrfly env folder or directory path? (Y/n): "
                )
                if choice_home.lower() == 'y':
                    present_repo_dir = set_env_path()
                    if present_repo_dir is None:
                        console.print(
                            f"[{error_style}]📛 Use 'fluttrfly env --force' to create the environment. 😟",
                            style=error_style,
                        )
                        sys.exit(1)
                    check_out = check_out_branch(
                        repo_dir=present_repo_dir, branch_name=env_version
                    )
                    add_paths_process_msg_display(
                        main_repo_dir=present_repo_dir,
                        check_out=check_out,
                        env_version=env_version,
                        repo_url=repo_url,
                    )
                elif choice_home.lower() == 'n':
                    choice_location = input("Do you want to recreate fluttrfly env ? (Y/n): ")
                    if choice_location.lower() == 'y':
                        if environment_setup_done:
                            write_specific_field(
                                config_path=config_path,
                                field_name="environment_setup_done",
                                field_value=False,
                            )
                            main_repo_dir = environment_setup(repo_url=repo_url)
                            check_out = check_out_branch(
                                repo_dir=main_repo_dir, branch_name=env_version
                            )
                            add_paths_process_msg_display(
                                main_repo_dir=main_repo_dir,
                                check_out=check_out,
                                env_version=env_version,
                                repo_url=repo_url,
                            )
                    elif choice_location.lower() == 'n':
                        console.print(
                            f"[{warning_style}]🚨 Exiting. Please choose a option. ✨",
                            style=warning_style,
                        )
                    else:
                        console.print(
                            f"[{error_style}]📛 Invalid choice. Exiting. 😟", style=error_style
                        )
                else:
                    console.print(
                        f"[{error_style}]📛 Invalid choice. Exiting. 😟", style=error_style
                    )

    ## code of argument 'fluttrfly build' @

    if args.command == "build":
        repo_url, environment_setup_done, repo_dir, env_version, messages = load(
            config_path=config_path
        )
        # Check if the environment is set up
        if not environment_setup_done:
            console.print(
                f"[{error_style}]📛 Environment not set up. Run 'fluttrfly env' first. 😟",
                style=error_style,
            )
            sys.exit(1)

        env_check_up(repo_dir=repo_dir, env_version=env_version, silence=True)

        if args.module:
            if not args.module.isdigit():
                if "/lib" in Path.cwd().as_posix():
                    with_loading(lambda: to_create_module_structure(args.module))
                else:
                    console.print(
                        f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory.[{warning_style}]",
                        style=warning_style,
                    )
            else:
                console.print(
                    f"[{error_style}]📛 ModuleName argument must be a non-numeric string.[{error_style}]",
                    style=error_style,
                )
                if "/lib" not in Path.cwd().as_posix():
                    console.print(
                        f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory.[{warning_style}]",
                        style=warning_style,
                    )

        if args.assets:
            if "/lib" in Path.cwd().as_posix():
                console.print(
                    f"[{warning_style}]🚨 Incorrect directory: Please run this command outside the 'lib' directory.[{warning_style}]",
                    style=warning_style,
                )
            else:
                with_loading(lambda: to_create_assets_structure())

        if args.core:
            if "/lib" in Path.cwd().as_posix():
                with_loading(lambda: to_create_core_structure())
            else:
                console.print(
                    f"[{warning_style}]🚨 Incorrect directory: Please run this command from the 'lib' directory.[{warning_style}]",
                    style=warning_style,
                )

        if len(sys.argv) == 2:
            show_build_command_lines()
            sys.exit(0)

    ## code of argument 'fluttrfly add' @

    # Here, We have to write code of sub_parser 'add_parser'
