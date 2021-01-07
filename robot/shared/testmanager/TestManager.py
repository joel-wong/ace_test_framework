import datetime
import json
import os
import subprocess

import ConfigManager
from DependencyManager import DependencyManager


class TestManager:

    def __init__(self):
        self.robot_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(os.path.curdir)))
        self.robot_lib_path = os.path.join(self.robot_directory,
                                           "shared", "lib")
        self.base_directory = os.path.dirname(self.robot_directory)
        self.submodule_path = os.path.join(self.base_directory,
                                           "Submodules")
        self.config_file_abspath = os.path.join(
            self.base_directory, ConfigManager.CONFIG_FILE_NAME)
        self.config_manager = ConfigManager.ConfigManager(
            self.robot_directory, self.config_file_abspath)

    def setup_and_run_tests(self):
        """Entry point to the ace-test-framework"""

        self.setup_pythonpath()
        DependencyManager.install_dependencies()
        self.config_manager.input_configuration()
        self.run_suites()
        return 0

    def setup_pythonpath(self):
        os.environ["PYTHONPATH"] = ";".join(
            [self.robot_lib_path, self.submodule_path,
             os.getenv("PYTHONPATH", default="")])

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
            subprocess.run(["python", "-m", "robot", "--outputdir",
                            output_directory, suite_directory],
                           shell=True, check=False)
            config_file_output_name = os.path.join(
                output_directory, ConfigManager.CONFIG_FILE_NAME)
            self.config_manager.save_config(config_file_output_name)
            print("\n\nTests complete! The results are stored in {}\n".format(
                    output_directory))
        input("Press enter to close.")


if __name__ == "__main__":
    test_manager = TestManager()
    test_manager.setup_and_run_tests()
