# setup_command.py
import sys
from ..commands.global_variables import (
    console,
    error_style,
    fluttrfly_version,
    info_style,
    success_style,
    warning_style,
)
from ..functions.setup_functions import setup_riverpod_structure, setup_bloc_structure


class SetupCommand:
    def __init__(self):
        pass

    def usedBoth(self):
        """Provide instructions to use one from both Riverpod and Bloc."""
        console.print(
            f"[{warning_style}]🚨 Both --riverpod and --bloc flags were provided. Please use only one. ✨",
            style=warning_style,
        )
        sys.exit(1)

    def setup_riverpod(self):
        """Set up the Flutter project using Riverpod."""
        setup_riverpod_structure()

    def setup_bloc(self):
        """Set up the Flutter project using Bloc."""
        setup_bloc_structure()
