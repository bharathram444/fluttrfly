# build_functions.py


import shutil
from pathlib import Path

from rich.tree import Tree

# Imports
from ..commands.global_variables import (
    branch_colors,
    config_path,
    console,
    current_directory,
    success_style,
    warning_style,
)
from ..functions.common_functions import with_loading
from ..functions.setup_functions import update_dependencies
from .json_functions import read_config


## Tree Functions @
def module_tree(module_name: str, cubit_or_provider: str = "cubit"):
    """
    Generates a styled, compressed module tree representation using rich.

    Args:
        module_name (str): The name of the module to show the structure for.
    """

    tree = Tree(f"[bold gold1]{module_name}[/bold gold1]")

    data_node = tree.add("[bold green]data[/bold green]")
    data_node.add("[green]models[/green]")
    data_node.add("[green]repository[/green]")

    presentation_node = tree.add("[bold magenta]presentation[/bold magenta]")
    presentation_node.add(f"[magenta]{cubit_or_provider}[/magenta]")

    screen_node = presentation_node.add("[magenta]screen[/magenta]")
    screen_node.add(f"[blue]{module_name}_page.dart[/blue]")

    presentation_node.add("[magenta]widgets[/magenta]")

    console.print(tree)
    console.print(
        f"[bold green]✅ Module '{module_name}' created successfully! ✨ 🌟 ✨[/bold green]",
        style=success_style,
    )


def assets_tree():
    tree = Tree("[bold gold1]assets[/bold gold1]")
    fonts_node = tree.add("[bold green]fonts[/bold green]")
    fonts_node.add("[blue]Raleway-Regular.ttf[/blue]")
    fonts_node.add("[blue]Roboto-Bold.ttf[/blue]")

    for branch in ["audio", "images", "video", "data", "others"]:
        tree.add(f"[bold {branch_colors[branch]}]" + branch, style=branch_colors[branch])

    console.print(tree)
    console.print(
        "[bold green]✅ Assets structure created successfully! ✨ 🌟 ✨[/bold green]",
        style=success_style,
    )


## Command Lines Build Functions @


def state_management_manager():
    config_data_of_fly = read_config(config_path)
    fluttrflyrc_path = current_directory.parent / ".fluttrflyrc"
    # Check if the config file exists
    if fluttrflyrc_path.exists():
        config_data_of_user_app = read_config(current_directory.parent / ".fluttrflyrc")
        state_management_char = config_data_of_user_app.get(
            "state_management", "b"
        )  # Default to 'b' if not set
        # Map state management character to setup type
        state_management = "riverpod_setup" if state_management_char == "r" else "bloc_setup"
        return state_management, config_data_of_user_app
    else:
        # Prompt user for input if config file does not exist
        state_management = (
            input("Enter your app state management (riverpod/bloc, or 'r'/'b'): ").strip().lower()
        )
        if state_management in ["r", "riverpod"]:
            state_management = "riverpod_setup"
            return state_management, config_data_of_fly
        else:
            console.print(f"[{warning_style}]📛 Invalid input! Defaulting to 'bloc'")
            state_management = "bloc_setup"
            return state_management, config_data_of_fly


# Module function $


def to_create_module_structure(ModuleName):

    # Local variables
    fm_module_name = ModuleName.lower()
    module_path = current_directory / fm_module_name
    state_management, _ = state_management_manager()

    cubit_or_provider = "provider" if state_management == "riverpod_setup" else "cubit"

    # Creating structure
    module_path.mkdir(parents=True, exist_ok=True)
    folders_and_sub_folders_list_strs = [
        "data/model",
        "data/repository",
        f"presentation/{cubit_or_provider}",
        "presentation/screen",
        "presentation/widgets",
    ]
    for folder_and_inner_folders in folders_and_sub_folders_list_strs:
        (module_path / folder_and_inner_folders).mkdir(parents=True, exist_ok=True)

    # Read the template
    config_data = read_config(config_path)
    if config_data:
        templates = Path(config_data.get("templates", ""))
        widget_template_path = templates / "MyWidget.txt"

    with (widget_template_path).open("r") as template_file:
        component_temp = template_file.read()

    # Modify the content
    component_temp = component_temp.replace("MyWidget", fm_module_name.capitalize() + "Screen")

    # Write to a new file
    with (module_path / "presentation/screen" / f"{fm_module_name}_page.dart").open(
        "w"
    ) as new_file:
        new_file.write(component_temp)
    module_tree(module_name=fm_module_name, cubit_or_provider=cubit_or_provider)


# Assets Function $


def to_create_assets_structure():
    # Local variables
    user_assets_path = current_directory / "assets"

    # Creating structure
    user_assets_path.mkdir(exist_ok=True)
    categories = ["fonts", "audio", "images", "video", "data", "others"]
    for folder in categories:
        (user_assets_path / folder).mkdir(exist_ok=True)

    # To copy files into folder
    config_data = read_config(config_path)
    if config_data:
        fonts = Path(config_data.get("fonts", ""))
    shutil.copytree(fonts, user_assets_path / "fonts", dirs_exist_ok=True)
    assets_tree()


# Core Function $


def to_create_core_structure():
    state_management, config_data_of_fly = state_management_manager()
    if config_data_of_fly:
        core = Path(config_data_of_fly.get(f"{state_management}", "")) / "lib/core"
    with_loading(
        task=lambda: shutil.copytree(core, current_directory / "core", dirs_exist_ok=True),
        status='Building',
    )
    with_loading(task=lambda: update_dependencies(state_management), status='Updating')
    console.print(
        f"[{success_style}]✅ Core structure created successfully! ✨ 🌟 ✨",
    )


def show_build_command_lines():
    # Main title with bold green foreground and yellow background
    title = "[bold green] 👨‍💻 Welcome to the Flutter command line tool (fluttrfly[FLY]) 🙂 ![/bold green]"
    console.print(title)
    # Command prompt with bold foreground and italic yellow underline
    command_prompt = "[bold]Choose a command to help you with your flutter project :[/bold]"
    console.print(command_prompt)
    # Commands with bold styles and different colors
    commands = [
        "[bold magenta]fluttrfly build --module module name[/bold magenta]  - Create a module structure",
        "[bold cyan]fluttrfly build --assets[/bold cyan]  - Create an assets structure",
        "[bold dodger_blue2]fluttrfly build --core[/bold dodger_blue2]    - Create core files and folders",
        "[bold blue]fluttrfly build --help[/bold blue]    - For more info",
    ]
    for command in commands:
        console.print(command)
    # Future features with bold and italic styles
    future_features = "[bold yellow]More features coming soon![/bold yellow] [italic]([italic red]ETA: 2 seconds[/italic red])[italic]"
    console.print(future_features)
