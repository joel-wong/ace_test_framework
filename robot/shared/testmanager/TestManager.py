import datetime
import json
import os
import subprocess

from manual import MANUAL_TEST_CONSTANTS

import ConfigManager
from DependencyManager import DependencyManager


class TestManager:

    def __init__(self):
        self.robot_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(os.path.curdir)))
        self.base_directory = os.path.dirname(self.robot_directory)
        self.config_file_abspath = os.path.join(
            self.base_directory, ConfigManager.CONFIG_FILE_NAME)
        self.config_manager = ConfigManager.ConfigManager(
            self.robot_directory, self.config_file_abspath)

    def setup_and_run_tests(self):
        """Entry point to the ace-test-framework"""

        DependencyManager.install_dependencies()
        self.config_manager.input_configuration()
        self.run_suites()
        return 0

    def run_suites(self):
        suite_name = self.config_manager.get(
            ConfigManager.CONFIG_SUITE_NAME)
        suite_directory = os.path.join(self.robot_directory, "suites",
                                       suite_name)
        main_test_output_directory = os.path.join(self.base_directory, "out",
                                                  suite_name)
        print("Starting tests now")
        num_suite_runs = self.config_manager.get(
            ConfigManager.CONFIG_REPEAT_TESTS)
        for _ in range(num_suite_runs):
            current_time = datetime.datetime.utcnow().isoformat("T")
            current_time = current_time.replace(":", "-").replace(".", "-")
            output_directory = os.path.join(main_test_output_directory,
                                            current_time)
            subprocess_args = ["python", "-m", "robot", "--outputdir",
                               output_directory]
            include_manual_tests = self.config_manager.get_bool(
                ConfigManager.CONFIG_INCLUDE_MANUAL_TESTS)
            if not include_manual_tests:
                subprocess_args.extend(
                    TestManager.generate_exclude_tags_args(
                        [MANUAL_TEST_CONSTANTS.MANUAL_TEST_TAG]))
            subprocess_args.append(suite_directory)
            subprocess.run(subprocess_args, shell=True, check=False)
            config_file_output_name = os.path.join(
                output_directory, ConfigManager.CONFIG_FILE_NAME)
            self.config_manager.save_config(config_file_output_name)
            print("\n\nTests complete! The results are stored in {}\n".format(
                    output_directory))
        input("Press enter to close.")

    @staticmethod
    def generate_exclude_tags_args(tags_to_exclude):
        """
        Generates the arguments to be added to the subprocess args in order to
        exclude the specified 'tags_to_exclude' from running

        :param tags_to_exclude: The list of tags associated with tests that
            will not be run
        :return: The additional arguments to be passed to 'python -m robot' upon
            startup to exclude the 'tags_to_exclude'
        """
        formatted_tags = list(
            map(lambda tag: "OR".join(["${{{}}}".format(tag), tag]),
                tags_to_exclude))
        return ["--exclude", "OR".join(formatted_tags)]


if __name__ == "__main__":
    test_manager = TestManager()
    test_manager.setup_and_run_tests()
