import functools
import json
import os


CONFIG_FILE_NAME = "config.json"
CONFIG_SUITE_NAME = "suite_name"
CONFIG_SERIAL_NUMBER = "serial_number"
SERIAL_NUMBER_TEXT = "Please enter the serial number:"
CONFIG_PART_NUMBER = "part_number"
PART_NUMBER_TEXT = "Please enter the part number:"
CONFIG_WORK_ORDER_OR_JOB_NUMBER = "work_order_or_job_number"
WORK_ORDER_JOB_NUMBER_TEXT = "Please enter the work order number or job number:"
CONFIG_STAFF_NAME = "staff_name"
STAFF_NAME_TEXT = "Please enter the staff member name:"
CONFIG_REPEAT_TESTS = "repeat_tests"
REPEAT_TESTS_TEXT = "How many times would you like the tests to be repeated?"

NO_DEFAULT_TEXT = "There is no default"


class ConfigManager:

    def __init__(self, robot_directory, config_file_abspath):
        self.__robot_directory = robot_directory
        self.__robot_directory = robot_directory
        self.__config_file_abspath = config_file_abspath
        self.__config = {}

    def input_configuration(self):
        """Retrieves configuration values from previous run if there are any
           and allows the user to either use the previous configuration values
           or set new ones"""
        self.get_default_config()

        print("\n\nPlease enter the configuration values below.")
        print("Press enter without entering any text to use the default value")
        print("for that configuration value.\n")

        self.input_suite_name()
        self.input_config_value_str(CONFIG_SERIAL_NUMBER, SERIAL_NUMBER_TEXT)
        self.input_config_value_str(CONFIG_PART_NUMBER, PART_NUMBER_TEXT)
        self.input_config_value_str(CONFIG_WORK_ORDER_OR_JOB_NUMBER,
                                    WORK_ORDER_JOB_NUMBER_TEXT)
        self.input_config_value_str(CONFIG_STAFF_NAME, STAFF_NAME_TEXT)
        self.input_config_value_positive_int(CONFIG_REPEAT_TESTS,
                                             REPEAT_TESTS_TEXT)

        config_file = open(self.__config_file_abspath, 'w')
        config_file.write(json.dumps(self.__config))
        config_file.close()

    def get_default_config(self):
        """Retrieves the existing configuration values, if they exist."""
        try:
            if os.stat(self.__config_file_abspath).st_size == 0:
                self.__config = {}
            else:
                config_file = open(self.__config_file_abspath, 'r')
                try:
                    self.__config = json.load(config_file)
                except json.decoder.JSONDecodeError:
                    print("ERROR: existing config file is not valid.")
                    print("       Ignoring defaults")
                    self.__config = {}
                config_file.close()
        except FileNotFoundError:
            # there is no existing config file
            self.__config = {}

    @staticmethod
    def print_default_invalid_message(config_key):
        print("Default {} value in {} is not valid".format(
            config_key, CONFIG_FILE_NAME))
        print("Ignoring default value")

    def input_config_value(self, config_key, display_text, validator):
        """Get the config value for the given config_key"""
        default_valid = False
        if config_key in self.__config.keys():
            try:
                self.__config[config_key] = validator(self.__config[config_key])
                default_valid = True
            except AssertionError:
                ConfigManager.print_default_invalid_message(config_key)
        while True:
            print(display_text)
            if default_valid:
                print("Default: {}".format(self.__config[config_key]))
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
                    value = validator(user_input)
                    self.__config[config_key] = value
                    return
                except AssertionError as e:
                    # invalid valid, print error message and ask for correct
                    # input
                    print(str(e))

    @staticmethod
    def validate_suite_name(valid_suites, suite_name_str):
        lower_suite_name = suite_name_str.lower()
        if lower_suite_name in valid_suites:
            return lower_suite_name

        try:
            suite_num = int(suite_name_str)
            if 0 < suite_num <= len(valid_suites):
                return valid_suites[suite_num - 1]
        except ValueError:
            # not a valid number
            pass

        raise AssertionError("That is not a valid suite name or number")

    def input_suite_name(self):
        suite_directory = os.path.join(self.__robot_directory, "suites")
        suite_folders = sorted(os.listdir(suite_directory))
        available_suites = list(map(lambda suite_name: suite_name.lower(),
                                suite_folders))
        display_text = "Please enter the suite name.\nOptions:"
        for index in range(len(available_suites)):
            suite = available_suites[index].lower()
            display_text += "\n{}: {}".format(index + 1, suite)
            # check that the previous default is still available to run

        suite_validator = functools.partial(ConfigManager.validate_suite_name,
                                            available_suites)
        self.input_config_value(CONFIG_SUITE_NAME, display_text,
                                suite_validator)

    @staticmethod
    def validate_str(input_str):
        """Input: a str"""
        if not input_str:
            raise AssertionError("Input value is empty")
        # other than empty str, all str are valid, simply return them
        return input_str

    def input_config_value_str(self, config_key, display_text):
        self.input_config_value(config_key, display_text, self.validate_str)

    @staticmethod
    def validate_positive_int(input_str):
        """
        Validates that an input str is a positive integer.

        If the input is a positive integer, returns the integer.
        Other the input is not a positive integers, returns False
        """
        try:
            value = int(input_str)
            if 0 < value:
                return value
        except ValueError:
            # user did not enter an integer
            pass
        raise AssertionError("That is not a positive number")

    def input_config_value_positive_int(self, config_key, display_text):
        self.input_config_value(config_key, display_text,
                                ConfigManager.validate_positive_int)

    def get(self, config_key, default=None):
        if config_key in self.__config:
            return self.__config[config_key]
        else:
            return default

    def save_config(self, config_file_output_path):
        config_file = open(config_file_output_path, 'w')
        config_file.write(json.dumps(self.__config))
        config_file.close()
