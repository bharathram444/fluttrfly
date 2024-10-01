# command_manager.py
import sys

from ..commands.setup_command import SetupCommand

from ..commands.build_command import BuildCommand
from ..commands.env_command import EnvCommand


class CommandsManager:
    def __init__(self):
        pass

    def handle_env(self, version, reset, update, force):
        """Handle the environment setup and management based on command-line flags."""
        envCommand = EnvCommand()
        if version:
            envCommand.env_version_tag()
        if reset:
            envCommand.env_reset_tag()
        if update:
            envCommand.env_update_tag()
        if force:
            envCommand.env_force_tag()
        if len(sys.argv) == 2:
            envCommand.env_no_tags()

    def handle_build(self, module, assets, core):
        """Handle the building of project structures like modules, assets, and core."""
        buildCommand = BuildCommand()
        if module:
            buildCommand.build_module_tag(module)
        if assets:
            buildCommand.build_assets_tag()
        if core:
            buildCommand.build_core_tag()
        if len(sys.argv) == 2:
            buildCommand.build_no_tags()

    def handle_setup(self, riverpod, bloc):
        """Handle the setup of Flutter projects using either Riverpod or Bloc."""

        setupCommand = SetupCommand()
        if riverpod and bloc:
            setupCommand.usedBoth()
        if riverpod:
            setupCommand.setup_riverpod()
        if bloc:
            setupCommand.setup_bloc()