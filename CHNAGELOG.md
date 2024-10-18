## 📝 Change Log

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [Unreleased]

#### Added

- New feature or command (e.g., `fluttrfly add`) for adding widgets and utilities to the core.

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

