import unittest
from unittest.mock import patch

# Assuming CommandsManager is located in commands_manager.py
from fluttrfly.bin.manager.commands_manager import CommandsManager


class TestCommandsManager(unittest.TestCase):
    @patch('fluttrfly.bin.manager.commands_manager.EnvCommand')
    def test_handle_env_version(self, MockEnvCommand):
        """Test handle_env when version flag is passed."""
        manager = CommandsManager()
        mock_env_command = MockEnvCommand.return_value

        # Simulate version flag
        manager.handle_env(version=True, reset=False, update=False, force=False)

        mock_env_command.env_version_tag.assert_called_once()
        mock_env_command.env_reset_tag.assert_not_called()
        mock_env_command.env_update_tag.assert_not_called()
        mock_env_command.env_force_tag.assert_not_called()

    @patch('fluttrfly.bin.manager.commands_manager.EnvCommand')
    def test_handle_env_reset(self, MockEnvCommand):
        """Test handle_env when reset flag is passed."""
        manager = CommandsManager()
        mock_env_command = MockEnvCommand.return_value

        # Simulate reset flag
        manager.handle_env(version=False, reset=True, update=False, force=False)

        mock_env_command.env_reset_tag.assert_called_once()
        mock_env_command.env_version_tag.assert_not_called()
        mock_env_command.env_update_tag.assert_not_called()
        mock_env_command.env_force_tag.assert_not_called()

    @patch('fluttrfly.bin.manager.commands_manager.EnvCommand')
    def test_handle_env_multiple_flags(self, MockEnvCommand):
        """Test handle_env when multiple flags (version and reset) are passed."""
        manager = CommandsManager()
        mock_env_command = MockEnvCommand.return_value

        # Simulate multiple flags
        manager.handle_env(version=True, reset=True, update=False, force=False)

        mock_env_command.env_version_tag.assert_called_once()
        mock_env_command.env_reset_tag.assert_called_once()

    @patch('fluttrfly.bin.manager.commands_manager.EnvCommand')
    def test_handle_env_no_flags(self, MockEnvCommand):
        """Test handle_env with no flags."""
        manager = CommandsManager()
        mock_env_command = MockEnvCommand.return_value

        # Simulate no flags
        manager.handle_env(version=False, reset=False, update=False, force=False)

        # Assert that env_no_tags was called when no flags were passed
        mock_env_command.env_no_tags.assert_called_once()

    @patch('fluttrfly.bin.manager.commands_manager.BuildCommand')
    def test_handle_build_module(self, MockBuildCommand):
        """Test handle_build when module flag is passed."""
        manager = CommandsManager()
        mock_build_command = MockBuildCommand.return_value

        # Simulate module flag
        manager.handle_build(module="auth", assets=False, core=False)

        mock_build_command.build_module_tag.assert_called_once_with("auth")
        mock_build_command.build_assets_tag.assert_not_called()
        mock_build_command.build_core_tag.assert_not_called()

    @patch('fluttrfly.bin.manager.commands_manager.BuildCommand')
    def test_handle_build_assets(self, MockBuildCommand):
        """Test handle_build when assets flag is passed."""
        manager = CommandsManager()
        mock_build_command = MockBuildCommand.return_value

        # Simulate assets flag
        manager.handle_build(module=False, assets=True, core=False)

        mock_build_command.build_assets_tag.assert_called_once()
        mock_build_command.build_module_tag.assert_not_called()
        mock_build_command.build_core_tag.assert_not_called()

    @patch('fluttrfly.bin.manager.commands_manager.BuildCommand')
    def test_handle_build_core(self, MockBuildCommand):
        """Test handle_build when core flag is passed."""
        manager = CommandsManager()
        mock_build_command = MockBuildCommand.return_value

        # Simulate core flag
        manager.handle_build(module=False, assets=False, core=True)

        mock_build_command.build_core_tag.assert_called_once()

    @patch('fluttrfly.bin.manager.commands_manager.BuildCommand')
    def test_handle_build_no_flags(self, MockBuildCommand):
        """Test handle_build with no flags."""
        manager = CommandsManager()
        mock_build_command = MockBuildCommand.return_value

        # Simulate no flags
        manager.handle_build(module=False, assets=False, core=False)

        # Assert that build_no_tags was called when no flags were passed
        mock_build_command.build_no_tags.assert_called_once()

    @patch('fluttrfly.bin.manager.commands_manager.SetupCommand')
    def test_handle_setup_riverpod(self, MockSetupCommand):
        """Test handle_setup when riverpod flag is passed."""
        manager = CommandsManager()
        mock_setup_command = MockSetupCommand.return_value

        # Simulate riverpod flag
        manager.handle_setup(riverpod=True, bloc=False)

        mock_setup_command.setup_riverpod.assert_called_once()
        mock_setup_command.setup_bloc.assert_not_called()

    @patch('fluttrfly.bin.manager.commands_manager.SetupCommand')
    def test_handle_setup_bloc(self, MockSetupCommand):
        """Test handle_setup when bloc flag is passed."""
        manager = CommandsManager()
        mock_setup_command = MockSetupCommand.return_value

        # Simulate bloc flag
        manager.handle_setup(riverpod=False, bloc=True)

        mock_setup_command.setup_bloc.assert_called_once()
        mock_setup_command.setup_riverpod.assert_not_called()

    @patch('fluttrfly.bin.manager.commands_manager.SetupCommand')
    def test_handle_setup_no_flags(self, MockSetupCommand):
        """Test handle_setup with no flags."""
        manager = CommandsManager()
        mock_setup_command = MockSetupCommand.return_value

        # Simulate no flags
        manager.handle_setup(riverpod=False, bloc=False)
        # Assert that setup_no_tags was called when no flags were passed
        mock_setup_command.setup_no_tags.assert_called_once()
