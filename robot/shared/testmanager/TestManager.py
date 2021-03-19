import datetime
import os
import subprocess
import sys
import copy

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
        suite_name = self.config_manager.get(ConfigManager.CONFIG_SUITE_NAME)
        suite_directory = os.path.join(self.robot_directory, "suites",
                                       suite_name)
        main_test_output_directory = os.path.join(self.base_directory, "out",
                                                  suite_name)
        print("Starting tests now")
        run_continuously = self.config_manager.get_bool(
            ConfigManager.CONFIG_REPEAT_TESTS)

        output_directory = os.path.join(main_test_output_directory,
                                        TestManager.generate_datetime_str())
        try:
            os.makedirs(output_directory, mode=0o660)
        except FileExistsError:
            print("Error: Output directory name already exists. Exiting...")
            sys.exit(1)
        individual_output_directory = os.path.join(output_directory,
                                                   "INDIVIDUAL TESTS")

        config_file_output_name = os.path.join(output_directory,
                                               ConfigManager.CONFIG_FILE_NAME)
        self.config_manager.save_config(config_file_output_name)

        if run_continuously:
            test_output_directory = individual_output_directory
        else:
            test_output_directory = output_directory

        subprocess_args = ["python", "-m", "robot", "--outputdir",
                           test_output_directory]

        include_manual_tests = self.config_manager.get_bool(
            ConfigManager.CONFIG_INCLUDE_MANUAL_TESTS)
        if not include_manual_tests:
            subprocess_args.extend(
                TestManager.generate_exclude_tags_subprocess_args(
                    [MANUAL_TEST_CONSTANTS.MANUAL_TEST_TAG]))

        if not run_continuously:
            subprocess_args.append("{}/*.robot".format(suite_directory))
            subprocess.run(subprocess_args, shell=True, check=False)
            TestManager.print_tests_complete_message(output_directory)
            return

        try:
            while True:
                current_run_args = copy.deepcopy(subprocess_args)
                run_datetime = TestManager.generate_datetime_str()
                current_run_args.extend(
                    ["--output", "output-{}.xml".format(run_datetime),
                     "--report", "report-{}.html".format(run_datetime),
                     "--log", "log-{}.html".format(run_datetime)])
                current_run_args.append("{}/*.robot".format(suite_directory))
                subprocess.run(current_run_args, shell=True, check=False)
        except KeyboardInterrupt:
            print("Consolidating all test reports...")
            merge_reports_subprocess_args = [
                "python", "-m", "robot.rebot", "--outputdir", output_directory,
                "--name", "bnc_card",
                "{}/*.xml".format(individual_output_directory)]
            subprocess.run(merge_reports_subprocess_args, shell=True,
                           check=False)
            TestManager.print_tests_complete_message(output_directory)

    @staticmethod
    def generate_datetime_str():
        current_time = datetime.datetime.utcnow().isoformat("T")
        current_time = current_time.replace(":", "-").replace(".", "-")
        return current_time

    @staticmethod
    def print_tests_complete_message(output_directory):
        print("\n\nTests complete! \n")
        print("The results are stored in {}\n".format(output_directory))
        input("Press enter to close.")

    @staticmethod
    def generate_exclude_tags_subprocess_args(tags_to_exclude):
        """
        Generates the arguments to be added to the subprocess args in order to
        exclude the specified 'tags_to_exclude' from running

        :param tags_to_exclude: The list of tags associated with tests that
            will not be run
        :return: The additional arguments to be passed to 'python -m robot'
            upon startup to exclude the 'tags_to_exclude'
        """
        # A current issue in robot framework is that tags are incorrectly
        # parsed when they are variables.
        # This is one of several issues documented in
        # https://github.com/robotframework/robotframework/issues/3238
        #
        # In order to handle the issue, we exclude both the literal str
        # ${TAG_NAME} as well as the TAG_NAME itself.
        # Currently, ${TAG_NAME} is the resolved tag name, but if the above
        # issue is fixed, TAG_NAME will be the resolved tag name
        formatted_tags = list(
            map(lambda tag: "OR".join(["${{{}}}".format(tag), tag]),
                tags_to_exclude))
        return ["--exclude", "OR".join(formatted_tags)]


if __name__ == "__main__":
    test_manager = TestManager()
    test_manager.setup_and_run_tests()
