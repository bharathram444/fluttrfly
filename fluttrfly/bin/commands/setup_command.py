import sys

from ..commands.global_variables import (
    config_path,
    console,
    error_style,
    info_style,
    success_style,
    warning_style,
)
from ..functions.common_functions import with_loading
from ..functions.env_functions import env_check_up
from ..functions.json_functions import load
from ..functions.setup_functions import (
    add_folders,
    create_app,
    create_fluttrflyrc,
    run_flutter_commands,
    show_setup_command_lines,
    update_android_manifest,
    update_dependencies,
    update_info_plist,
    update_local_keys,
    update_pubspec_yaml,
)


class SetupCommand:
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

    def used_both(self):
        """Provide instructions to use one from both Riverpod and Bloc."""
        console.print(
            f"[{warning_style}]🚨 Both --riverpod[-r] and --bloc[-b] flags were provided. Please use only one. ✨",
        )
        sys.exit(1)

    def _setup_project(self, state_management):
        """Set up the Flutter project based on the state management type."""
        # step 1: create basic flutter app using user inputs
        app_path, org_name, app_name, platforms = create_app()

        # step 2: add assets, lib, packages folders in user app.
        with_loading(
            task=lambda: add_folders(state_management=state_management, app_path=app_path),
            status='Adding',
        )

        # step 3: update pubspec.yaml
        with_loading(
            task=lambda: update_pubspec_yaml(
                file_path=app_path + "/pubspec.yaml", state_management=state_management
            ),
            status='Updating',
        )

        # step 4: update local_keys.dart
        with_loading(
            task=lambda: update_local_keys(
                local_keys_path=app_path + "/lib/core/local_storage/local_keys.dart",
                org_name=org_name,
                app_name=app_name,
            ),
            status='Updating',
        )

        # step 5: update AndroidManifest.xml and Info.plist based on platforms
        if 'android' in platforms:
            with_loading(
                task=lambda: update_android_manifest(
                    manifest_path=app_path + "/android/app/src/main/AndroidManifest.xml"
                ),
                status='Updating',
            )
        if 'ios' in platforms:
            with_loading(
                task=lambda: update_info_plist(plist_path=app_path + "/ios/Runner/Info.plist"),
                status='Updating',
            )

        # step 6: update dependencies based on state management type
        with_loading(
            task=lambda: update_dependencies(state_management=state_management), status='Updating'
        )

        # step 7: run flutter commands to complete the setup
        with_loading(task=lambda: run_flutter_commands(app_path=app_path), status='Running')

        # step 8: create .fluttrflyrc in user app
        with_loading(task=lambda: create_fluttrflyrc(app_path=app_path))

        # step 9: provide navigation info
        console.print(f"[{info_style}]ℹ️  Run: cd {app_name} && code . ✨")
        console.print(
            f"[{success_style}]✅ {state_management.capitalize()} project setup successfully! ✨"
        )

    def setup_riverpod(self):
        """Set up the Flutter project using Riverpod."""
        self._setup_project(state_management="riverpod")

    def setup_bloc(self):
        """Set up the Flutter project using Bloc."""
        self._setup_project(state_management="bloc")

    def setup_no_tags(self):
        show_setup_command_lines()
        sys.exit(0)
