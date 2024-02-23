# build_functions.py


import shutil
import time
from pathlib import Path

from rich.tree import Tree

# Imports
from ..variables.global_variables import (
    branch_colors,
    config_path,
    console,
    current_directory,
    error_style,
    success_style,
)
from .json_functions import read_config


# loading animation
def with_loading(task, duration=1):
    with console.status("[bold green]Creating..."):
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
            console.print(f"An error occurred: {e}", style="bold red")


## Tree Functions @
def module_tree(module_name: str):
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
    presentation_node.add("[magenta]cubit[/magenta]")

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

# Module function $


def to_create_module_structure(ModuleName):

    # Local variables
    fm_module_name = ModuleName.lower()
    module_path = current_directory / fm_module_name

    # Creating structure
    module_path.mkdir(parents=True, exist_ok=True)
    folders_and_sub_folders_list_strs = [
        "data/model",
        "data/repository",
        "presentation/cubit",
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
    module_tree(module_name=fm_module_name)


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
    config_data = read_config(config_path)
    if config_data:
        core = Path(config_data.get("core", ""))
    shutil.copytree(core, current_directory / "core", dirs_exist_ok=True)
    console.print("[bold yellow]Use this command to add 📦 dependencies : ", style="bold")
    console.print(
        "[bold cyan]flutter pub add[/bold cyan] cupertino_icons flutter_bloc dartz intl path_provider firebase_crashlytics logger url_launcher freezed_annotation build_runner package_info_plus image_picker day_night_time_picker freezed",
        style="cyan",
    )
    console.print("[bold magenta]✅ Chick 📄 notes present in core folder! [/bold magenta]")
    console.print(
        "[bold green]✅ Core structure created successfully! ✨ 🌟 ✨[/bold green]",
        style=success_style,
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
        "[bold dodger_blue2]fluttrfly build --core[/bold dodger_blue2]   - Create core files and folders",
        "[bold blue]fluttrfly build --help[/bold blue]   - For more info",
    ]
    for command in commands:
        console.print(command)
    # Future features with bold and italic styles
    future_features = "[bold yellow]More features coming soon![/bold yellow] [italic]([italic red]ETA: 2 seconds[/italic red])[italic]"
    console.print(future_features)
