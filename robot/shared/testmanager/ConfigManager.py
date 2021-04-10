import functools
import json
import os
import re

# ---- REGEX PATTERNS ----
WORK_ORDER_RE_PATTERN = r'^\d{10}$'
PART_NUMBER_RE_PATTERN = r'^\d{3}-\d{4}-\d{3}$'
BATCH_MO_NUMBER_RE_PATTERN = r'^\d{8}$'
SERIAL_NUMBER_RE_PATTERN = r'^\d{3}$'

# ---- REGEX MESSAGES ----
WORK_ORDER_RE_MESSAGE = "10 digits"
PART_NUMBER_RE_MESSAGE = "xxx-xxxx-xxx where 'x' is a digit"
BATCH_MO_NUMBER_RE_MESSAGE = "8 digits"
SERIAL_NUMBER_RE_MESSAGE = "3 digits"

# ---- CONSTANT TEXT PATTERNS ----
CONFIG_FILE_NAME = "config.json"
CONFIG_SUITE_NAME = "suite_name"
CONFIG_DIR_PATH = "dir_path"
DIR_PATH_TEXT = "Please enter directory path to save test result files in:"
CONFIG_SERIAL_NUMBER = "serial_number"
SERIAL_NUMBER_TEXT = "Please enter the serial number:"
CONFIG_BATCH_MO_NUMBER = "batch_mo_number"
BATCH_MO_NUMBER_TEXT = "Please enter the batch number / MO number:"
CONFIG_PART_NUMBER = "part_number"
PART_NUMBER_TEXT = "Please enter the part number:"
CONFIG_WORK_ORDER_JOB_NUMBER = "work_order_job_number"
# note that work order number is synonymous with job number
WORK_ORDER_JOB_NUMBER_TEXT = "Please enter the work order number / job number:"
CONFIG_STAFF_NAME = "staff_name"
STAFF_NAME_TEXT = "Please enter the staff member name:"
CONFIG_INCLUDE_MANUAL_TESTS = "include_manual_tests"
INCLUDE_MANUAL_TESTS_TEXT = "Include manual tests? [Yes/True or No/False]"
CONFIG_REPEAT_TESTS = "repeat_tests"
REPEAT_TESTS_TEXT = "Run tests continuously until stopped " \
                    "via Ctrl + C? [Yes/True or No/False]"

NO_DEFAULT_TEXT = "There is no default"


class ConfigType:
    def __init__(self, config_key, validator, display_default_config_value, cli_text, gui_text, gui_error_message):
        self.config_key = config_key
        self.validator = validator
        self.display_default_config_value = display_default_config_value
        self.cli_text = cli_text
        self.gui_text = gui_text
        self.gui_error_message = gui_error_message


class ConfigManager:
    def __init__(self, robot_directory, config_file_abspath):
        self.__robot_directory = robot_directory
        self.__robot_directory = robot_directory
        self.__config_file_abspath = config_file_abspath
        self.__config = {}
        self.suite_name_config = ConfigType(
            config_key=CONFIG_SUITE_NAME,
            validator=ConfigManager.validate_suite_name,
            display_default_config_value=True,
            cli_text="",
            gui_text="Please Select Test Suite:",
            gui_error_message=""
        )
        self.dir_path_config = ConfigType(
            config_key=CONFIG_DIR_PATH,
            validator=ConfigManager.validate_dir_path,
            display_default_config_value=True,
            cli_text=DIR_PATH_TEXT,
            gui_text="Please select folder to save test result files in:",
            gui_error_message="Invalid Folder!"
        )
        self.part_number_config = ConfigType(
            config_key=CONFIG_PART_NUMBER,
            validator=ConfigManager.validate_part_number,
            display_default_config_value=True,
            cli_text=PART_NUMBER_TEXT,
            gui_text="Part Number:",
            gui_error_message="Invalid Part Number! Expected input of the form: {}".format(
                PART_NUMBER_RE_MESSAGE)
        )
        self.batch_mo_number_config = ConfigType(
            config_key=CONFIG_BATCH_MO_NUMBER,
            validator=ConfigManager.validate_batch_mo_number,
            display_default_config_value=True,
            cli_text=BATCH_MO_NUMBER_TEXT,
            gui_text="Batch Number/MO Number:",
            gui_error_message="Invalid Batch Number/MO Number! Expected input of the form: {}".format(
                BATCH_MO_NUMBER_RE_MESSAGE)
        )
        self.serial_number_config = ConfigType(
            config_key=CONFIG_SERIAL_NUMBER,
            validator=ConfigManager.validate_serial_number,
            display_default_config_value=False,
            cli_text=SERIAL_NUMBER_TEXT,
            gui_text="Serial Number:",
            gui_error_message="Invalid Serial Number! Expected input of the form: {}".format(
                SERIAL_NUMBER_RE_MESSAGE)
        )
        self.work_order_job_number_config = ConfigType(
            config_key=CONFIG_WORK_ORDER_JOB_NUMBER,
            validator=ConfigManager.validate_work_order,
            display_default_config_value=True,
            cli_text=WORK_ORDER_JOB_NUMBER_TEXT,
            gui_text="Work Order/Job Number:",
            gui_error_message="Invalid Work Order/Job Number! Expected input of the form: {}".format(
                WORK_ORDER_RE_MESSAGE)
        )
        self.staff_name_config = ConfigType(
            config_key=CONFIG_STAFF_NAME,
            validator=ConfigManager.validate_str,
            display_default_config_value=True,
            cli_text=STAFF_NAME_TEXT,
            gui_text="Staff Member Name:",
            gui_error_message="Invalid Staff Name!"
        )
        self.include_manual_tests_config = ConfigType(
            config_key=CONFIG_INCLUDE_MANUAL_TESTS,
            validator=ConfigManager.validate_bool,
            display_default_config_value=True,
            cli_text=INCLUDE_MANUAL_TESTS_TEXT,
            gui_text="",
            gui_error_message=""
        )
        self.repeat_tests_config = ConfigType(
            config_key=CONFIG_REPEAT_TESTS,
            validator=ConfigManager.validate_bool,
            display_default_config_value=True,
            cli_text=REPEAT_TESTS_TEXT,
            gui_text="Run tests continuously?",
            gui_error_message=""
        )

    def input_config_via_command_line(self):
        """Retrieves configuration values from previous run if there are any
           and allows the user to either use the previous configuration values
           or set new ones"""
        self.get_default_config()

        print("\n\nPlease enter the configuration values below.")
        print("Press enter without entering any text to use the default value")
        print("for that configuration value.\n")

        self.input_suite_name()
        self.input_config_value(self.dir_path_config)
        self.input_config_value(self.part_number_config)
        self.input_config_value(self.batch_mo_number_config)
        self.input_config_value(self.serial_number_config)
        self.input_config_value(self.work_order_job_number_config)
        self.input_config_value(self.staff_name_config)
        self.input_config_value(self.include_manual_tests_config)
        self.input_config_value(self.repeat_tests_config)

        self.save_config_as_default()

    def save_config_as_default(self):
        self.save_config(self.__config_file_abspath)

    def save_config(self, config_file_output_path):
        config_file = open(config_file_output_path, 'w')
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

    def input_config_value(self, config_type):
        """Get the config value for the given config_key"""
        default_valid = False
        if config_type.config_key in self.__config.keys() and config_type.display_default_config_value:
            try:
                self.__config[config_type.config_key] = config_type.validator(self.__config[config_type.config_key])
                default_valid = True
            except AssertionError:
                ConfigManager.print_default_invalid_message(config_type.config_key)
        while True:
            print(config_type.cli_text)
            if default_valid:
                print("Default: {}".format(self.__config[config_type.config_key]))
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
                    value = config_type.validator(user_input)
                    self.__config[config_type.config_key] = value
                    return
                except AssertionError as e:
                    # invalid valid, print error message and ask for correct
                    # input
                    print(str(e))

    def get_default_config_value(self, config_type):
        if config_type.config_key in self.__config.keys():
            try:
                value = config_type.validator(self.__config[config_type.config_key])
                return value
            except AssertionError:
                return None
        return None

    def set_config_value(self, config_type, user_input):
        value = config_type.validator(user_input.strip())
        self.__config[config_type.config_key] = value

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

    def get_available_suites_and_set_suite_validator(self):
        suite_directory = os.path.join(self.__robot_directory, "suites")
        suite_folders = sorted(os.listdir(suite_directory))
        available_suites = list(map(lambda suite_name: suite_name.lower(),
                                    suite_folders))
        self.suite_name_config.validator = functools.partial(ConfigManager.validate_suite_name, available_suites)
        return available_suites

    def input_suite_name(self):
        available_suites = self.get_available_suites_and_set_suite_validator()
        display_text = "Please enter the suite name.\nOptions:"
        for index in range(len(available_suites)):
            suite = available_suites[index].lower()
            display_text += "\n{}: {}".format(index + 1, suite)
            # check that the previous default is still available to run
        self.suite_name_config.cli_text = display_text
        self.input_config_value(self.suite_name_config)

    @staticmethod
    def validate_dir_path(input_str):
        if os.path.isdir(input_str):
            return input_str
        else:
            raise AssertionError("input value must be a valid directory")

    @staticmethod
    def validate_str(input_str):
        """Input: a str"""
        if not input_str:
            raise AssertionError("Input value is empty")
        # other than empty str, all str are valid, simply return them
        return input_str

    @staticmethod
    def validate_re_match(pattern, input_str, re_message):
        if ConfigManager.validate_str(input_str) and re.fullmatch(pattern, input_str):
            return input_str
        raise AssertionError("Invalid input. Expected input of the form: {}".format(re_message))

    @staticmethod
    def validate_work_order(input_str):
        return ConfigManager.validate_re_match(WORK_ORDER_RE_PATTERN, input_str, WORK_ORDER_RE_MESSAGE)

    @staticmethod
    def validate_part_number(input_str):
        return ConfigManager.validate_re_match(PART_NUMBER_RE_PATTERN, input_str, PART_NUMBER_RE_MESSAGE)

    @staticmethod
    def validate_batch_mo_number(input_str):
        return ConfigManager.validate_re_match(BATCH_MO_NUMBER_RE_PATTERN, input_str, BATCH_MO_NUMBER_RE_MESSAGE)

    @staticmethod
    def validate_serial_number(input_str):
        return ConfigManager.validate_re_match(SERIAL_NUMBER_RE_PATTERN, input_str, SERIAL_NUMBER_RE_MESSAGE)

    @staticmethod
    def validate_bool(value):
        if type(value) == bool:
            return value
        try:
            input_str_lower = value.lower()
        except AttributeError as e:
            raise AssertionError("Input value must be Yes/True or No/False")
        if input_str_lower in ["y", "yes", "t", "true"]:
            return True
        elif input_str_lower in ["n", "no", "f", "false"]:
            return False
        raise AssertionError("Input value must be Yes/True or No/False")

    def get(self, config_key, default=None):
        if config_key in self.__config:
            return self.__config[config_key]
        else:
            return default

    def get_bool(self, config_key, default=None):
        if config_key in self.__config:
            return self.__config[config_key] is True
        else:
            return default

    def get_log_config_str(self):
        if self.__config == {}:
            self.get_default_config()
        return json.dumps(self.__config)
