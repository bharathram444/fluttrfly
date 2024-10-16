# import os
# import unittest
# from unittest.mock import patch, MagicMock, mock_open, call
# from pathlib import Path
# import subprocess

# # Import the setup_functions module
# from fluttrfly.bin.functions.setup_functions import (
#     _get_setup_path,
#     _select_platforms,
#     create_app,
#     add_folders,
#     update_pubspec_yaml,
#     update_local_keys,
#     update_android_manifest,
#     update_info_plist,
#     update_dependencies,
#     run_flutter_commands,
#     create_fluttrflyrc,
# )


# class TestSetupFunctions(unittest.TestCase):
#     @patch('fluttrfly.bin.functions.json_functions.read_config')
#     def test_get_setup_path(self, mock_read_config):
#         # Mock the config data for both cases (riverpod and bloc)
#         mock_read_config.return_value = {
#             "riverpod_setup": "/path/to/riverpod_setup",
#             "bloc_setup": "/path/to/bloc_setup",
#         }

#         # Test for riverpod
#         result = _get_setup_path("riverpod")
#         self.assertEqual(result, Path("/path/to/riverpod_setup"))

#         # Test for bloc
#         result = _get_setup_path("bloc")
#         self.assertEqual(result, Path("/path/to/bloc_setup"))

#     @patch('builtins.input', side_effect=["y", "n", "y", "n", "n", "n"])
#     @patch('setup_functions.console')
#     def test_select_platforms(self, mock_console, mock_input):
#         result = _select_platforms()
#         self.assertEqual(result, "android,linux")

#     @patch('setup_functions.subprocess.run')
#     @patch('setup_functions.os.chdir')
#     @patch('builtins.input', side_effect=["com.example", "test_app"])
#     @patch('setup_functions._select_platforms', return_value="android,ios")
#     @patch('setup_functions.console')
#     def test_create_app_success(
#         self, mock_console, mock_select_platforms, mock_input, mock_chdir, mock_subprocess_run
#     ):
#         mock_subprocess_run.return_value = MagicMock(returncode=0)
#         app_path, org_name, app_name, platforms = create_app()
#         self.assertEqual(app_path, os.getcwd())
#         self.assertEqual(org_name, "com.example")
#         self.assertEqual(app_name, "test_app")
#         self.assertEqual(platforms, "android,ios")

#     @patch('setup_functions.subprocess.run', side_effect=subprocess.CalledProcessError(1, "cmd"))
#     @patch('setup_functions.console')
#     def test_create_app_failure(self, mock_console, mock_subprocess_run):
#         with self.assertRaises(SystemExit):
#             create_app()

#     @patch('setup_functions._get_setup_path', return_value=Path("/setup_path"))
#     @patch('setup_functions.shutil.copytree')
#     @patch('setup_functions.console')
#     def test_add_folders(self, mock_console, mock_copytree, mock_get_setup_path):
#         add_folders("riverpod", "/app_path")
#         mock_copytree.assert_has_calls(
#             [
#                 call(Path("/setup_path/assets"), Path("/app_path/assets"), dirs_exist_ok=True),
#                 call(Path("/setup_path/lib"), Path("/app_path/lib"), dirs_exist_ok=True),
#                 call(Path("/setup_path/packages"), Path("/app_path/packages"), dirs_exist_ok=True),
#                 call(Path("/setup_path/test"), Path("/app_path/test"), dirs_exist_ok=True),
#             ]
#         )

#     @patch('setup_functions.read_yaml', return_value={'dependencies': {}, 'flutter': {}})
#     @patch('setup_functions.write_yaml')
#     @patch('setup_functions.console')
#     def test_update_pubspec_yaml(self, mock_console, mock_write_yaml, mock_read_yaml):
#         update_pubspec_yaml("/path/to/pubspec.yaml")
#         mock_read_yaml.assert_called_once_with("/path/to/pubspec.yaml")
#         mock_write_yaml.assert_called_once()  # We could also test the exact write content

#     @patch('builtins.open', new_callable=mock_open, read_data="old data")
#     @patch('setup_functions.console')
#     def test_update_local_keys(self, mock_console, mock_open_file):
#         update_local_keys("/path/to/local_keys.dart", "com.example", "test_app")
#         mock_open_file.assert_called_with("/path/to/local_keys.dart", "w")
#         mock_open_file().write.assert_called_once_with(
#             "old data".replace("in.easycloud.axiom_services", "com.example.test_app")
#         )

#     @patch('setup_functions.ET.parse')
#     @patch('setup_functions.console')
#     def test_update_android_manifest(self, mock_console, mock_et_parse):
#         mock_tree = MagicMock()
#         mock_root = MagicMock()
#         mock_et_parse.return_value = mock_tree
#         mock_tree.getroot.return_value = mock_root

#         update_android_manifest("/path/to/AndroidManifest.xml")

#         mock_root.insert.assert_any_call(1, mock_tree.getroot().insert())

#     @patch('builtins.open', new_callable=mock_open, read_data="{}")
#     @patch('setup_functions.plistlib.load', return_value={})
#     @patch('setup_functions.plistlib.dump')
#     @patch('setup_functions.console')
#     def test_update_info_plist(
#         self, mock_console, mock_plistlib_dump, mock_plistlib_load, mock_open_file
#     ):
#         update_info_plist("/path/to/Info.plist")
#         mock_open_file.assert_called_with("/path/to/Info.plist", "wb")
#         mock_plistlib_dump.assert_called_once()

#     @patch('setup_functions.subprocess.run')
#     @patch('setup_functions.console')
#     def test_run_flutter_commands(self, mock_console, mock_subprocess_run):
#         run_flutter_commands("/path/to/app")
#         commands = [
#             "flutter clean",
#             "flutter pub get",
#             "flutter pub run build_runner build --delete-conflicting-outputs",
#         ]
#         mock_subprocess_run.assert_has_calls(
#             [call(cmd, shell=True, check=True, cwd=Path("/path/to/app")) for cmd in commands]
#         )
