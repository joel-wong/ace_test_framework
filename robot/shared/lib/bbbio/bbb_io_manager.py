"""
A series of functions that manages communication between the Beagle Bone Black (BBB) and
allows the users to control inputs and outputs on the BBB
"""

import json

from ace_bbsm import BBB_IO_CONSTANTS, Client

import bbb_io_validation
from robot.api import logger

# Sample JSON that will be sent to the BBB when send_io_specifications_to_bbb()
# is called:
"""
[
  {
    "spec_type": "output",
    "output_type": "i2c",
    "i2cbus": "2",
    "chip_address": "0x27",
    "data_address": 0x03,
    "data": 0xF7
  },
  {
    "spec_type": "output",
    "output_type": "digital_3v3"
    "pin_number": "P9_25",
    "output_value": "1"
  },
  {
    "spec_type": "input"
    "input_type": "digital_3v3"
    "pin_number": "P9_25",
  }
]
"""

# Sample data received from the BBB when send_io_specifications_to_bbb() is
# called:
"""
[
  {
    "input_type": "digital_3v3"
    "pin_number": "P9_25",
    "input_value": "1"
  }
]
"""


class BBBServerError(Exception):
    def __init__(self, server_message):
        super().__init__(server_message)


io_to_send = []
bbb_return_data = []
client = Client()


def connect_to_bbb():
    """
    Connects to the BBB using the IP address and port number defined
    in the ace_bbsm module.

    The BBB must not already be connected when function is called.
    """
    client.connect_to_bbb()
    reset_bbb_io_specifications()


def disconnect_from_bbb():
    """
    Disconnects from the BBB. The BBB must be connected when this function
    is called.
    """
    client.disconnect_from_bbb()


def reset_bbb_io_specifications():
    """
    Resets the data/steps sent to and/or returned from the BBB
    """
    io_to_send.clear()
    reset_bbb_return_data()


def reset_bbb_return_data():
    """
    Resets the data returned from the BBB
    """
    bbb_return_data.clear()


def specify_bbb_digital_output(pin_number, value):
    """
    Updates the 'io_to_send' so that when
    'send_io_specifications_to_BBB' is called, the given digital 'value'
    is output on the given pin_number

    :param pin_number: The pin number on which the BBB will have a digital
        output
    :param value: The value for the signal that should be output on the BBB
    """
    bbb_io_validation.validate_bbb_output(
        pin_number, BBB_IO_CONSTANTS.DIGITAL_3V3, value)
    io_to_send.append({
        BBB_IO_CONSTANTS.SPEC_TYPE: BBB_IO_CONSTANTS.SPEC_TYPE_OUTPUT,
        BBB_IO_CONSTANTS.OUTPUT_TYPE: BBB_IO_CONSTANTS.DIGITAL_3V3,
        BBB_IO_CONSTANTS.PIN_NUMBER: pin_number,
        BBB_IO_CONSTANTS.OUTPUT_VALUE: value
    })


I2C_KEYS = {BBB_IO_CONSTANTS.I2CBUS, BBB_IO_CONSTANTS.I2C_CHIP_ADDRESS,
            BBB_IO_CONSTANTS.I2C_DATA_ADDRESS, BBB_IO_CONSTANTS.I2C_DATA}


def specify_bbb_i2c_output(i2cbus, chip_address, data_address, data):
    """
    Updates the 'io_to_send' so that when
    'send_io_specifications_to_BBB' is called, the given
    'i2c_specification_number' and 'data' is output

    There can be zero or more pieces of I2C data provided in each test.
    Most tests will not require any I2C data to be sent to the device under
    test. If I2C data is provided to the circuit under test, it must have a
    i2c_spec_number. This specifies the order in which the I2C data is sent
    to the circuit under test. For example, if there are two pieces of I2C
    data to be sent to the BBB, then there should be two calls to this
    function:
    specify_bbb_i2c_output(1, i2cbus, chip_address, data_address, data)
    specify_bbb_i2c_output(2, i2cbus, chip_address, data_address, data)

    If there is only one piece of I2C data is required, then only one call
    to this function is required:
    specify_bbb_i2c_output(1, i2cbus, chip_address, data_address, data)

    Note that only the order of the i2c_spec_numbers is important (when
    there are multiple sets of I2C data), not the actual numbers

    On the Beaglebone, the following command will occur once
    send_io_specifications_to_bbb() is called:
        i2cset -y -r i2cbus chip_address data_address data

    :param i2cbus: str: the identifier for the i2cbus on the BeagleBone that
        will output the data
    :param chip_address: str: A str representing a hex value between 0x03 and
        0x77 for the corresponding chip address
    :param data_address: str: A str representing a hex value between 0x00 and
        0xFF for the corresponding data address
    :param data: str: The data to be sent via I2C, representing a hex value.
        Can also be an empty str
    """
    bbb_io_validation.validate_i2c(i2cbus, chip_address, data_address, data)
    io_to_send.append({
        BBB_IO_CONSTANTS.SPEC_TYPE: BBB_IO_CONSTANTS.SPEC_TYPE_OUTPUT,
        BBB_IO_CONSTANTS.OUTPUT_TYPE: BBB_IO_CONSTANTS.I2C,
        BBB_IO_CONSTANTS.I2CBUS: i2cbus,
        BBB_IO_CONSTANTS.I2C_CHIP_ADDRESS: chip_address,
        BBB_IO_CONSTANTS.I2C_DATA_ADDRESS: data_address,
        BBB_IO_CONSTANTS.I2C_DATA: data
    })


def specify_bbb_i2c_output_dict(i2cset_parameters):
    """
    Convenience method that allows a dictionary to be specified when adding I2C
    specifications
    :param i2cset_parameters: The i2c parameters, as a dictionary. Must contain
        all of the following keys and no additional keys:
        - `BBB_IO_CONSTANTS.I2CBUS`
        - `BBB_IO_CONSTANTS.I2C_CHIP_ADDRESS`
        - `BBB_IO_CONSTANTS.I2C_DATA_ADDRESS`
        - `BBB_IO_CONSTANTS.I2C_DATA`
    :return:
    """
    if I2C_KEYS != set(i2cset_parameters.keys()):
        raise ValueError("I2C data is missing or has extra keys")
    specify_bbb_i2c_output(i2cset_parameters[BBB_IO_CONSTANTS.I2CBUS],
                           i2cset_parameters[BBB_IO_CONSTANTS.I2C_CHIP_ADDRESS],
                           i2cset_parameters[BBB_IO_CONSTANTS.I2C_DATA_ADDRESS],
                           i2cset_parameters[BBB_IO_CONSTANTS.I2C_DATA])


def specify_bbb_digital_input(pin_number):
    """
    Updates the 'io_to_send' so that when
    'send_io_specifications_to_BBB' is called, the digital value of the given
    pin_number is returned.

    :param pin_number: The pin number on which the BBB will have a digital input
    """
    bbb_io_validation.validate_bbb_input(pin_number,
                                         BBB_IO_CONSTANTS.DIGITAL_3V3)
    io_to_send.append({
        BBB_IO_CONSTANTS.SPEC_TYPE: BBB_IO_CONSTANTS.SPEC_TYPE_INPUT,
        BBB_IO_CONSTANTS.INPUT_TYPE: BBB_IO_CONSTANTS.DIGITAL_3V3,
        BBB_IO_CONSTANTS.PIN_NUMBER: pin_number
    })


def specify_bbb_analog_input(pin_number):
    """
    Updates the 'io_to_send' so that when
    'send_io_specifications_to_BBB' is called, the analog value (normalized
    between 0 and 1) of the given pin_number is returned

    :param pin_number: The pin number on which the BBB will have an analog input
    """
    bbb_io_validation.validate_bbb_input(pin_number,
                                         BBB_IO_CONSTANTS.ANALOG_1V8)
    io_to_send.append({
        BBB_IO_CONSTANTS.SPEC_TYPE: BBB_IO_CONSTANTS.SPEC_TYPE_INPUT,
        BBB_IO_CONSTANTS.INPUT_TYPE: BBB_IO_CONSTANTS.ANALOG_1V8,
        BBB_IO_CONSTANTS.PIN_NUMBER: pin_number
    })


def send_io_specifications_to_bbb(suite_validator):
    """
    Sends the current IO specifications amalgamated from all calls to
    `specify_bbb_output()` and `specify_bbb_input()` since the last call to
    `reset_bbb_io_specifications()` to the BBB

    :param suite_validator: A function that takes the IO specification as an
        input and verifies that the entire specification is valid for the given
        suite. For example, it may validate that there are no pins that will
        be in contention for the given IO specification. Having a suite level
        validator is highly recommended, but a None value can be input to skip
        suite level validation
    :return: The outputs on the BBB requested in the specify_bbb_input calls
    """
    if bbb_return_data:
        raise AssertionError("Must call reset_bbb_io_specifications() or "
                             "reset_bbb_return_data() before sending new IO "
                             "specification")
    if suite_validator is not None:
        suite_validator(io_to_send)
    json_to_send = json.dumps(io_to_send)
    response = client.json_request_response_bbb(json_to_send)
    returned_data = json.loads(response)
    if 'Error' in returned_data:
        logger.warn(returned_data['Error'])
        raise BBBServerError(returned_data['Error'])
    else:
        bbb_return_data.extend(returned_data)
        return bbb_return_data


def get_bbb_input_value(pin_number):
    """
    Retrieves the value or values on the input 'pin_number' within the
    'bbb_return_data'

    'send_io_specifications_to_bbb' must be called before calling this function
    or the return data will be empty as the BBB will not have ever received the
    IO specifications

    Return the value or values in a list, even if there is only one value

    :param pin_number: The pin name on which the BBB has received input
    :return: A list of values of the specified input to the BBB
    """
    input_dicts = filter(
        lambda data: data[BBB_IO_CONSTANTS.PIN_NUMBER] == pin_number,
        bbb_return_data)
    input_values = list(map(
        lambda data: data[BBB_IO_CONSTANTS.INPUT_VALUE],
        input_dicts))
    if not input_values:
        raise AssertionError("No values for the given pin_number")
    return input_values
