import datetime
import json
import os
import subprocess
import sys

CONFIG_FILE_NAME = "config.json"
CONFIG_SUITE_NAME = "suite_name"
CONFIG_SERIAL_NUMBER = "serial_number"
SERIAL_NUMBER_TEXT = "Please enter the serial number:"
CONFIG_PART_NUMBER = "part_number"
PART_NUMBER_TEXT = "Please enter the part number:"
CONFIG_STAFF_NAME = "staff_name"
STAFF_NAME_TEXT = "Please enter the staff member name:"
CONFIG_REPEAT_TESTS = "repeat_tests"
REPEAT_TESTS_TEXT = "How many times would you like the tests to be repeated?"

NO_DEFAULT_TEXT = "There is no default"


class TestManager:

    def __init__(self):
        self.robot_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(os.path.curdir)))
        self.base_directory = os.path.dirname(self.robot_directory)
        self.config_file_name = os.path.join(self.base_directory,
                                             CONFIG_FILE_NAME)

    def setup_and_run_tests(self):
        """Entry point to the ace-test-framework"""

        TestManager.install_dependencies()
        self.get_configuration()
        self.run_suites()
        return 0

    @staticmethod
    def install_dependencies():
        """Installs and upgrades dependencies needed for robot framework"""

        # check python version and verify we are using Python 3
        if sys.version[0] < '3':
            print("ERROR: python version 3 required. You are using version "
                  "{}".format(sys.version))
            print("You must install python 3 from https://www.python.org")
            print("Make sure to check the 'pip' package manager option when")
            print("installing python")
            return
        try:
            import pip
        except ModuleNotFoundError:
            print("The python 'pip' package manager is required.")
            print("Go to https://www.python.org and download Python 3")
            print("When re-installing, select 'modify' and make sure")
            print("to check the 'pip' option")
            return

        # upgrade pip
        print("Upgrading/installing any required dependencies...")
        subprocess.run(["python", "-m", "pip", "install", "-q",
                        "--upgrade", "pip", "--no-warn-script-location"],
                       shell=True, check=True)
        print("Python 3 is installed and up to date")

        # upgrade/install dependencies such as robot framework
        subprocess.run(["python", "-m", "pip", "install", "-q", "--user",
                        "--upgrade", "-r",
                        os.path.join(os.path.curdir, "requirements.txt"),
                        "--no-warn-script-location"],
                       shell=True, check=True)
        print("Robot framework is installed and up to date")

    def get_configuration(self):
        """Retrieves configuration values from previous run if there are any
           and allows the user to either use the previous configuration values
           or set new ones"""
        try:
            if os.stat(self.config_file_name).st_size == 0:
                self.config = {}
            else:
                config_file = open(self.config_file_name, 'r')
                try:
                    self.config = json.load(config_file)
                except json.decoder.JSONDecodeError:
                    print("ERROR: existing config file is not valid.")
                    print("       Ignoring defaults")
                    self.config = {}
                config_file.close()
        except FileNotFoundError:
            # there is no existing config file
            self.config = {}

        print("\n\nPlease enter the configuration values below.")
        print("Press enter without entering any text to use the default value")
        print("for that configuration value.\n")

        self.get_suite_name()
        self.get_config_value_str(CONFIG_SERIAL_NUMBER, SERIAL_NUMBER_TEXT)
        self.get_config_value_str(CONFIG_PART_NUMBER, PART_NUMBER_TEXT)
        self.get_config_value_str(CONFIG_STAFF_NAME, STAFF_NAME_TEXT)
        self.get_config_value_positive_int(CONFIG_REPEAT_TESTS,
                                           REPEAT_TESTS_TEXT)

        config_file = open(self.config_file_name, 'w')
        config_file.write(json.dumps(self.config))
        config_file.close()

    @staticmethod
    def print_default_invalid_message(config_key):
        print("Default {} value in {} is not valid".format(
            config_key, CONFIG_FILE_NAME))
        print("Ignoring default value")

    def get_suite_name(self):
        print("Please enter the suite name.")
        print("Options:")
        available_suites = sorted(os.listdir(
            os.path.join(self.robot_directory, "suites")))
        default_suite_name_is_valid = False
        if CONFIG_SUITE_NAME in self.config.keys():
            default_suite_name = self.config[CONFIG_SUITE_NAME].lower()
        else:
            default_suite_name = ""
        for index in range(len(available_suites)):
            suite = available_suites[index].lower()
            print("{}: {}".format(index + 1, suite))
            # check that the previous default is still available to run
            if default_suite_name == suite:
                default_suite_name_is_valid = True

        if default_suite_name and not default_suite_name_is_valid:
            TestManager.print_default_invalid_message(CONFIG_SUITE_NAME)
        elif not default_suite_name_is_valid:
            print(NO_DEFAULT_TEXT)
        else:
            print("Default: {}".format(default_suite_name))
        while True:
            user_suite_name = input().strip().lower()
            if not user_suite_name:
                # use default
                if not default_suite_name_is_valid:
                    print(NO_DEFAULT_TEXT)
                else:
                    # config already has default value, just return
                    return
            elif user_suite_name in available_suites:
                self.config[CONFIG_SUITE_NAME] = user_suite_name
                return
            else:
                try:
                    suite_number = int(user_suite_name) - 1
                    if 0 <= suite_number < len(available_suites):
                        self.config[CONFIG_SUITE_NAME] = available_suites[
                                                                suite_number]
                        return
                except ValueError:
                    # the string is not a number, allow user to re-enter value
                    pass
                print("That is not a valid suite name or number")

            print("Please enter the suite number or the full suite name")

    def get_config_value_str(self, config_key, display_text):
        # default exists in the config file and the value is not empty
        default_exists = (config_key in self.config.keys()) and (
            self.config[config_key])
        while True:
            print(display_text)
            if default_exists:
                print("Default: {}".format(self.config[config_key]))
            else:
                print(NO_DEFAULT_TEXT)
            user_input = input().strip()
            if not user_input:
                if default_exists:
                    # config already has default value, just return
                    return
                else:
                    print(NO_DEFAULT_TEXT)
            else:
                self.config[config_key] = user_input
                return

    def get_config_value_positive_int(self, config_key, display_text):
        default_exists = config_key in self.config.keys()
        default_valid = default_exists
        if default_exists:
            try:
                default_value = int(self.config[config_key])
                if 0 >= default_value:
                    default_valid = False
            except ValueError:
                default_valid = False
            if not default_valid:
                TestManager.print_default_invalid_message(config_key)
        while True:
            print(display_text)
            if default_valid:
                print("Default: {}".format(self.config[config_key]))
            else:
                print(NO_DEFAULT_TEXT)
            user_input = input().strip()
            if not user_input:
                if default_valid:
                    # config already has default value, just return
                    return
                else:
                    print(NO_DEFAULT_TEXT)
            else:
                try:
                    value = int(user_input)
                    if 0 < value:
                        self.config[config_key] = value
                        return
                except ValueError:
                    # user did not enter an integer
                    pass
                print("That is not a positive number")

    def run_suites(self):
        suite_directory = os.path.join(self.robot_directory, "suites",
                                       self.config[CONFIG_SUITE_NAME])
        main_test_output_directory = os.path.join(
            self.base_directory, "out", self.config[CONFIG_SUITE_NAME])
        print("Starting tests now")
        for _ in range(self.config[CONFIG_REPEAT_TESTS]):
            current_time = datetime.datetime.utcnow().isoformat("T")
            current_time = current_time.replace(":", "-").replace(".", "-")
            output_directory = os.path.join(main_test_output_directory,
                                            current_time)
            subprocess.run(["python", "-m", "robot", "--outputdir",
                            output_directory, suite_directory],
                           shell=True, check=False)
            config_file_output_name = os.path.join(output_directory,
                                                   CONFIG_FILE_NAME)
            config_file = open(config_file_output_name, 'w')
            config_file.write(json.dumps(self.config))
            config_file.close()
            print("\n\nTests complete! The results are stored in {}\n".format(
                    output_directory))
        input("Press enter to close.")


if __name__ == "__main__":
    test_manager = TestManager()
    test_manager.setup_and_run_tests()
