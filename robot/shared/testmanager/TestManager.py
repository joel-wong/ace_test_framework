import datetime
import os
import subprocess
import sys
import copy
import argparse
import signal

from manual import MANUAL_TEST_CONSTANTS
import Listener
import SelectTests

import ConfigManager
from DependencyManager import DependencyManager

from gui.GUI import GUI
from PyQt5 import QtWidgets


class TestManager:
    def __init__(self, in_gui_mode=True):
        self.robot_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(os.path.curdir)))
        self.base_directory = os.path.dirname(self.robot_directory)
        self.config_file_abspath = os.path.join(
            self.base_directory, ConfigManager.CONFIG_FILE_NAME)
        self.config_manager = ConfigManager.ConfigManager(
            self.robot_directory, self.config_file_abspath)

        self.__in_gui_mode = in_gui_mode
        self.__gui = None
        self.robot_process = None
        self.stop_tests = False
        self.emergency_stop_flag = False
        self.suite_count = 0
        self.test_fail_count = 0
        self.test_pass_count = 0

    def setup_and_run_framework(self):
        """Entry point to the ace-test-framework"""
        DependencyManager.install_dependencies()
        if self.__in_gui_mode:
            self.config_manager.get_default_config()
            app = QtWidgets.QApplication(sys.argv)
            app.setStyle('Fusion')
            self.__gui = GUI(self)
            self.__gui.start_gui()
            sys.exit(app.exec_())
        else:
            self.config_manager.input_config_via_command_line()
            self.run_suites()
        return 0

    def run_suites(self, test_runner_worker=None):
        suite_name = self.config_manager.get(ConfigManager.CONFIG_SUITE_NAME)
        suite_directory = os.path.join(self.robot_directory, "suites",
                                       suite_name)
        main_test_output_directory = self.config_manager.get(
            ConfigManager.CONFIG_DIR_PATH)

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
                           test_output_directory,
                           "--doc", self.config_manager.log_test_data()]

        if not self.__in_gui_mode:
            include_manual_tests = self.config_manager.get_bool(
                ConfigManager.CONFIG_INCLUDE_MANUAL_TESTS)
            if not include_manual_tests:
                subprocess_args.extend(
                    TestManager.generate_exclude_tags_subprocess_args(
                        [MANUAL_TEST_CONSTANTS.MANUAL_TEST_TAG]))

        if self.__in_gui_mode:
            subprocess_args.extend(["--listener", Listener.__file__])
            selected_tests_list = self.__gui.select_tests_window.selected_tests_list
            subprocess_args.extend(["--prerunmodifier", "{}:{}".format(
                SelectTests.__file__, selected_tests_list)])

        if not run_continuously:
            try:
                subprocess_args.append("{}/*.robot".format(suite_directory))
                self.run_process(subprocess_args, test_runner_worker)
            except KeyboardInterrupt:
                self.emergency_stop_flag = True
            self.print_tests_complete_message(output_directory)
            return

        try:
            while self.stop_tests is False:
                current_run_args = copy.deepcopy(subprocess_args)
                run_datetime = TestManager.generate_datetime_str()
                current_run_args.extend(
                    ["--output", "output-{}.xml".format(run_datetime),
                     "--report", "report-{}.html".format(run_datetime),
                     "--log", "log-{}.html".format(run_datetime)])
                current_run_args.append("{}/*.robot".format(suite_directory))
                self.run_process(current_run_args, test_runner_worker)
                if test_runner_worker is not None:
                    test_runner_worker.progress.emit()
        except KeyboardInterrupt:
            self.emergency_stop_flag = True
        self.consolidate_reports(output_directory, individual_output_directory)

    def run_process(self, subprocess_args, test_runner_worker):
        if test_runner_worker is not None:
            self.run_process_with_live_count(subprocess_args, test_runner_worker)
        else:
            self.run_process_without_communication(subprocess_args)
        self.suite_count += 1

    def run_process_with_live_count(self, subprocess_args, test_runner_worker):
        for message in self.run_process_with_communication(subprocess_args):
            split_message = message.split(':')
            if split_message[0].strip() == Listener.LISTENER_MESSAGE:
                if split_message[1].strip() == Listener.FAIL_MESSAGE:
                    self.test_fail_count += 1
                    test_runner_worker.progress.emit()
                elif split_message[1].strip() == Listener.PASS_MESSAGE:
                    self.test_pass_count += 1
                    test_runner_worker.progress.emit()
            else:
                print(message, end="")

    def run_process_with_communication(self, subprocess_args):
        self.robot_process = subprocess.Popen(subprocess_args, shell=True,
                                              stdout=subprocess.PIPE,
                                              universal_newlines=True)
        for stdout_line in iter(self.robot_process.stdout.readline, ""):
            yield stdout_line
        self.robot_process.stdout.close()
        self.robot_process.wait()

    def run_process_without_communication(self, subprocess_args):
        self.robot_process = subprocess.Popen(subprocess_args, shell=True,)
        self.robot_process.wait()

    def get_tests(self):
        suite_name = self.config_manager.get(ConfigManager.CONFIG_SUITE_NAME)
        suite_directory = os.path.join(self.robot_directory, "suites",
                                       suite_name)
        return SelectTests.get_tests(suite_directory)

    @staticmethod
    def generate_datetime_str():
        current_time = datetime.datetime.utcnow().isoformat("T")
        current_time = current_time.replace(":", "-").replace(".", "-")
        return current_time

    def consolidate_reports(self, output_directory, individual_output_directory):
        print("Consolidating all test reports...")
        merge_reports_subprocess_args = [
            "python", "-m", "robot.rebot", "--outputdir", output_directory,
            "--name", "bnc_card",
            "{}/*.xml".format(individual_output_directory)]
        subprocess.run(merge_reports_subprocess_args, shell=True,
                       check=False)
        self.print_tests_complete_message(output_directory)

    def print_tests_complete_message(self, output_directory):
        print("\n\nTests complete! \n")
        if self.emergency_stop_flag:
            print("Note: Remaining tests were automatically failed after emergency stop was activated.\n")
        print("The results are stored in {}\n".format(output_directory))
        if not self.__in_gui_mode:
            input("Press enter to close.")
        else:
            self.__gui.tests_complete_window.set_open_output_buttons(output_directory)

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


def sigint_signal_handler(signal, frame):
    test_manager.stop_tests = True
    test_manager.emergency_stop_flag = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run ACE Test Framework')
    parser.add_argument('--nogui', action="store_true")
    args = parser.parse_args()
    signal.signal(signal.SIGINT, sigint_signal_handler)
    test_manager = TestManager(in_gui_mode=(not args.nogui))
    test_manager.setup_and_run_framework()
