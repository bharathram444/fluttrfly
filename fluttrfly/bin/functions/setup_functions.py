# setup_functions.py
import json
import os
import plistlib
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from ..commands.global_variables import (
    config_path,
    console,
    fluttrfly_version,
    info_style,
)
from ..functions.common_functions import error_x, read_yaml, success_x, warning_x, write_yaml
from ..functions.json_functions import read_config


def _env_pubspec(state_management):
    setup_path = _get_setup_path(state_management)
    pubspec_env_path = setup_path / "pubspec.yaml"
    # Load the pubspec.yaml file
    with open(pubspec_env_path, 'r') as file:
        pubspec = yaml.safe_load(file)
        return pubspec


def _get_setup_path(state_management):
    """Retrieve the setup path from the configuration file based on the state management type."""
    # Read the configuration data
    config_data = read_config(config_path)

    # Determine the key based on the state management type
    key = "riverpod_setup" if state_management == "riverpod" else "bloc_setup"

    # Initialize setup_path to an empty Path
    setup_path = Path("")

    # Check if config_data exists and get the setup path
    if config_data:
        setup_path = Path(config_data.get(key, ""))

    return setup_path


def _select_platforms():
    """Allow the user to select platforms via a checkbox-like interface."""
    platforms = ["android", "ios", "linux", "macos", "web", "windows"]
    selected_platforms = []
    console.print(f"[{info_style}]ℹ️ Select platforms for your project:")
    for i, platform in enumerate(platforms, 1):
        user_input = input(f"{i}. {platform}? (y/n): ")
        if user_input.lower() == "y":
            selected_platforms.append(platform)
    if not selected_platforms:
        warning_x(message="No platforms selected. Defaulting to 'android,ios'.")
        return "android,ios"
    return ",".join(selected_platforms)


def create_app():
    """Create a new Flutter app with user-defined organization name, app name, and platforms."""
    # Step 1: Collect user inputs for organization, app name, and platforms
    org_name = input("Enter the organization name (e.g., com.example): ").strip()
    app_name = input("Enter the app name: ").strip()
    # Validate input
    if not org_name or not app_name:
        error_x(message="Organization name and app name cannot be empty!")
        sys.exit(1)
    platforms = _select_platforms()
    # Step 2: Run 'flutter create' command with user inputs
    flutter_create_cmd = f"flutter create --org {org_name} --platforms {platforms} {app_name}"
    try:
        subprocess.run(flutter_create_cmd, shell=True, check=True)
        success_x(message="Flutter project created successfully!")
        # Step 3: Change directory to the newly created app
        os.chdir(app_name)
        return os.getcwd(), org_name, app_name, platforms
    except subprocess.CalledProcessError:
        error_x(message="Failed to create Flutter project.")
        sys.exit(1)
        return None


def add_folders(state_management, app_path):
    """Add assets,lib,packages folders in user app."""
    # Step 4: Add assets,lib,packages,test in user app
    setup_path = _get_setup_path(state_management)
    app_path_x = Path(app_path)
    assets_path = setup_path / "assets"
    lib_path = setup_path / "lib"
    packages_path = setup_path / "packages"
    test_path = setup_path / "test"
    shutil.copytree(assets_path, app_path_x / "assets", dirs_exist_ok=True)
    shutil.copytree(lib_path, app_path_x / "lib", dirs_exist_ok=True)
    shutil.copytree(packages_path, app_path_x / "packages", dirs_exist_ok=True)
    shutil.copytree(test_path, app_path_x / "test", dirs_exist_ok=True)
    success_x(message="assets, lib, packages, test added successfully!")


def update_pubspec_yaml(file_path, state_management):
    """Update pubspec.yaml by adding specific keys and values."""
    # Step 5: Update pubspec.yaml.
    # 0. Read the existing YAML data
    data = read_yaml(file_path)
    # Path of the env pubspec.yaml file
    pubspec = _env_pubspec(state_management)
    # Read and assets section
    assets = pubspec.get('flutter', {}).get('assets', [])
    # 1. Add 'fluttrfly' under the root
    data['dependencies']['fluttrfly'] = {'path': 'packages/fluttrfly'}

    # 2. Add 'assets' under 'flutter'
    if 'flutter' not in data:
        data['flutter'] = {}
    data['flutter']['assets'] = assets

    # 3. Add 'flutter_launcher_icons' under the root
    data['flutter_launcher_icons'] = {
        'android': 'ic_launcher',
        'image_path': 'assets/logo/logo.png',
        'ios': False,
        'min_sdk_android': 21,
        'macos': {'generate': True, 'image_path': 'assets/logo/logo.png'},
    }

    # Write the updated YAML data back to the pubspec.yaml
    write_yaml(file_path, data)
    success_x(message="pubspec.yaml has been updated successfully!")


def update_local_keys(local_keys_path, org_name, app_name):
    """Update local_keys.dart by adding specific keys and values."""
    # Step 6: Update local_keys.dart.
    # 0. Created Path and check exists
    local_keys_path_x = Path(local_keys_path)
    if not local_keys_path_x.exists():
        warning_x(message="local_keys.dart not found."),
    # 1. Read local keys file
    with (local_keys_path_x).open("r") as template_file:
        component_temp = template_file.read()
    # 2. Modify the content
    component_temp = component_temp.replace(
        "in.easycloud.axiom_services", f"{org_name}.{app_name}"
    )
    # 3. Write to a new file
    with (local_keys_path_x).open("w") as new_file:
        new_file.write(component_temp)
    success_x(message="local_keys.dart has been updated successfully!")


def update_android_manifest(manifest_path):
    """Adds location permissions to the AndroidManifest.xml file."""

    # Step 1: Parse the AndroidManifest.xml file
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    # Step 2: Register the 'android' namespace
    ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')

    # Step 3: Create <uses-permission> elements for location permissions
    fine_location_permission = ET.Element("uses-permission")
    fine_location_permission.set(
        "{http://schemas.android.com/apk/res/android}name",
        "android.permission.ACCESS_FINE_LOCATION",
    )

    coarse_location_permission = ET.Element("uses-permission")
    coarse_location_permission.set(
        "{http://schemas.android.com/apk/res/android}name",
        "android.permission.ACCESS_COARSE_LOCATION",
    )

    # Step 4: Insert the permissions below the <manifest> tag
    root.insert(1, fine_location_permission)  # Insert fine location permission
    root.insert(2, coarse_location_permission)  # Insert coarse location permission

    # Step 5: Write the updated file back to AndroidManifest.xml
    tree.write(manifest_path, encoding="utf-8", xml_declaration=True)

    success_x(message="AndroidManifest.xml updated successfully!")


def update_info_plist(plist_path):
    """Add location usage descriptions to iOS Info.plist."""

    # Step 1: Read the existing Info.plist file
    with open(plist_path, 'rb') as plist_file:
        plist_data = plistlib.load(plist_file)

    # Step 2: Add location permission keys to the dict
    plist_data['NSLocationWhenInUseUsageDescription'] = (
        "This app needs access to location when open."
    )
    plist_data['NSLocationAlwaysUsageDescription'] = (
        "This app needs access to location when in the background."
    )

    # Step 3: Write the updated plist back to the file
    with open(plist_path, 'wb') as plist_file:
        plistlib.dump(plist_data, plist_file)

    success_x(message="Info.plist updated successfully!")


def update_dependencies(state_management):
    """
    Updates Flutter dependencies in the pubspec.yaml file and installs them using flutter pub add.
    """
    # Path of the env pubspec.yaml file
    pubspec = _env_pubspec(state_management)
    # Extract dependencies and dev_dependencies
    dependencies = pubspec.get('dependencies', {})
    dev_dependencies = pubspec.get('dev_dependencies', {})
    # Filter out flutter and fluttrfly from dependencies
    runtime_deps = [
        k for k in dependencies if k not in ['flutter', 'fluttrfly', 'cupertino_icons']
    ]
    # Filter out flutter_test from dev_dependencies
    dev_deps = [k for k in dev_dependencies if k not in ['flutter_test', 'flutter_lints']]
    # Add runtime dependencies using 'flutter pub add'
    if runtime_deps:
        runtime_cmd = ['flutter', 'pub', 'add'] + runtime_deps
        subprocess.run(runtime_cmd, check=True)

    # Add dev dependencies using 'flutter pub add -d'
    if dev_deps:
        dev_cmd = ['flutter', 'pub', 'add', '-d'] + dev_deps
        subprocess.run(dev_cmd, check=True)
    success_x(message="Dependencies updated successfully!")


def run_flutter_commands(app_path):
    """
    Run Flutter commands in the user app and in the packages/fluttrfly package.
    """
    # Define the commands to run
    commands = [
        "flutter clean",
        "flutter pub get",
        "flutter pub run build_runner build --delete-conflicting-outputs",
    ]
    app_path_x = Path(app_path)
    # Run commands in the user app directory
    success_x(message="Running Flutter commands in the user app...")
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True, cwd=app_path_x)
            success_x(message=f"Executed: {command}")
        except subprocess.CalledProcessError as e:
            error_x(message=f"Error while executing command '{command}': {e}")

    # Run commands in the packages/fluttrfly directory
    success_x(message="Running Flutter commands in the packages/fluttrfly...")
    fluttrfly_path = app_path_x / "packages/fluttrfly"
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True, cwd=fluttrfly_path)
            success_x(message=f"Executed: {command}")
        except subprocess.CalledProcessError as e:
            error_x(message=f"Error while executing command '{command}': {e}")
    success_x(message="Flutter commands executed successfully!")


def create_fluttrflyrc(app_path, state_management):
    """
    Create a .fluttrflyrc file in the user app directory with specified data.
    """
    # Define the data to be stored in the .fluttrflyrc file
    key = "r" if state_management == "riverpod" else "b"
    fluttrfly_data = {"state_management": key, "fluttrfly_version": fluttrfly_version}
    app_path_x = Path(app_path)

    # Define the path to the .fluttrflyrc file
    fluttrflyrc_path = app_path_x / ".fluttrflyrc"

    # Write the data to the .fluttrflyrc file
    try:
        with open(fluttrflyrc_path, 'w') as fluttrflyrc_file:
            json.dump(fluttrfly_data, fluttrflyrc_file, indent=4)
        success_x(message=f"Created .fluttrflyrc file at: {fluttrflyrc_path}")
    except Exception as e:
        error_x(message=f"📛Error while creating .fluttrflyrc file: {e}")


def show_setup_command_lines():
    # Main title with bold green foreground and yellow background
    title = "[bold green] 👨‍💻 Welcome to the Flutter command line tool (fluttrfly[FLY]) 🙂 ![/bold green]"
    console.print(title)
    # Command prompt with bold foreground and italic yellow underline
    command_prompt = "[bold]Choose a command to help you with your flutter project :[/bold]"
    console.print(command_prompt)
    # Commands with bold styles and different colors
    commands = [
        "[bold magenta]fluttrfly setup --riverpod[/bold magenta]  - Set up a riverpod project",
        "[bold cyan]fluttrfly setup --bloc[/bold cyan]  - Set up a bloc project",
        "[bold dodger_blue2]fluttrfly setup --help[/bold dodger_blue2]  - For more info",
    ]
    for command in commands:
        console.print(command)
    # Future features with bold and italic styles
    future_features = "[bold yellow]More features coming soon![/bold yellow] [italic]([italic red]ETA: 2 seconds[/italic red])[italic]"
    console.print(future_features)
