## 📝 Change Log

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [Unreleased]

#### Added

- New feature or command (e.g., `fluttrfly add`) for adding widgets and utilities to the core.
### Version 2.0.4 (2024-11-20)

#### Added
- Bug Fix in `create_fluttrflyrc` function:
  - Here we hard coded this state_management like "r" now we changed this calling or  passing state_management field form `_setup_project` function.

### Version 2.0.3 (2024-10-21)

#### Added
- Bug Fix in `state_management_manager` function:
  - Here we get path of user project path to read `.fluttrflyrc` but previous logic were not capable to read the file that's way, we changed logic.
- Bug Fix in `common_functions.py` function:
  - Here we added styles fun's to reduce code and easy to use style at console for error, success, warning, info.

### Version 2.0.2 (2024-10-19)

#### Added
- Bug Fix in `check_path_exists` function:
  - Here we read empty json field "repo_dir": "" then we returned None to avoid bug in `fluttrfly env --force` by saying use `fluttrfly env`.
- Bug Fix in `paths_check_up` function:
  - Here we checked wrong hardcoded paths at line 244, 249. We fixed it.

### Version 2.0.1 (2024-10-18)

#### Added
- Enhanced `update_pubspec_yaml` function:
  - Reads the `assets` section from `env_pubspec.yaml` and updates the user flutter app's `pubspec.yaml` accordingly.


### Version 2.0.0 (2024-10-18)

#### Added
- **`fluttrfly setup` command:**
  - Introduced to streamline project setup based on state management.
  - Supports options to choose between `bloc` and `riverpod` for state management during the project creation process:
    - `fluttrfly setup -r` or `--riverpod` for setting up a Flutter project with Riverpod.
    - `fluttrfly setup -b` or `--bloc` for setting up a Flutter project with Bloc.
  - Automates the project structure and boilerplate required for the chosen state management solution.

### Version 1.0.0 (2024-02-24)

#### Added

- **Initial Release:**
  - FluttrFly CLI is officially launched, providing a streamlined Flutter development workflow.
  - Introduces essential commands for project setup, including:
    - `fluttrfly build`: Generates various project structures.
    - `fluttrfly env`: Manages the FluttrFly development environment.

