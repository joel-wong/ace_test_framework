"""
A series of functions that manages communication between the Beagle Bone Black (BBB) and
allows the users to control inputs and outputs on the BBB
"""

import BBB_IO_CONSTANTS
import json

import ace_bbsm

# Sample JSON that will be sent to the BBB when send_io_specifications_to_bbb()
# is called:
"""
{
    "outputs":{
    "P8-30": {
        "type": "digital",
        BBB_IO_CONSTANTS.VALUE: "1"
    },
    "P8-40": {
        "type": "analog",
        BBB_IO_CONSTANTS.VALUE: "1.8"
    },
    "P8-50": {
        "type": "pwm",
        BBB_IO_CONSTANTS.VALUE: "60"
    }
  },
  "i2c": {
    1: {
      "data": "base64 encoding of first data"
    },
    2: {
      "data": "base 64 encoding of second data"
    }
  }
  "inputs": {
    "P8-20": {
       "type": "digital",
    }
}
"""

# Sample data received from the BBB when send_io_specifications_to_bbb() is
# called:
"""
{
  "inputs": {
      "P8-20": 0
  }
}
"""


io_to_send = {}
client = ace_bbsm.Client()


def connect_to_bbb():
    client.connect_to_bbb()


def disconnect_from_bbb():
    client.disconnect_from_bbb()


def reset_bbb_io_specifications():
    io_to_send[BBB_IO_CONSTANTS.INPUTS] = {}
    io_to_send[BBB_IO_CONSTANTS.OUTPUTS] = {}
    io_to_send[BBB_IO_CONSTANTS.I2C] = {}


def specify_bbb_output(pin_name, output_type, value):
    """
    Updates the 'io_to_send' so that when
    'send_io_specifications_to_BBB' is called, the given 'output_type'
    and 'value' is output on the given pin_name

    :param pin_name: The pin name on which the BBB will have an output
    :param output_type: the type of signal that should be output on the BBB
    :param value: The value for the signal that should be output on the BBB
    """
    # TODO: validate that the input type is valid
    # TODO: validate that the input value is valid for the input type
    io_to_send[BBB_IO_CONSTANTS.OUTPUTS][pin_name] = {
        BBB_IO_CONSTANTS.TYPE: output_type,
        BBB_IO_CONSTANTS.VALUE: value
    }


def specify_bbb_i2c_output(i2c_spec_number, data):
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
        specify_bbb_i2c_output(1, first_data)
        specify_bbb_i2c_output(2, second_data)

        If there is only one piece of I2C data is required, then only one call
        to this function is required:
        specify_bbb_i2c_output(1, first_data)

        Note that the only the order of the i2c_spec_numbers is important (when
        there are multiple sets of I2C data), not the actual numbers

        :param i2c_spec_number: int: the order in which I2C signals should be sent
            to the circuit under test, with the lowest i2c_spec_number first
            (each i2c_spec_number must be unique for a given test)
        :param data: byte[]: The data to be sent via I2C
    """
    io_to_send[BBB_IO_CONSTANTS.I2C][int(i2c_spec_number)] = {
        BBB_IO_CONSTANTS.I2C_DATA: data
    }


def specify_bbb_input(pin_name, input_type):
    """
    Updates the 'io_to_send' so that when
    'send_io_specifications_to_BBB' is called, the given 'input_type'
    is input on the given pin_name and the value is returned.

    :param pin_name: The pin name on which the BBB will have an input
    :param input_type: the type of signal that should be input on the BBB
    """
    io_to_send[BBB_IO_CONSTANTS.INPUTS][pin_name] = {
        BBB_IO_CONSTANTS.TYPE: input_type
    }


def send_io_specifications_to_bbb():
    """
    Sends the current IO specifications amalgamated from all calls to
    `specify_bbb_output()` and `specify_bbb_input()` since the last call to
    `reset_bbb_io_specifications()` to the BBB

    :return: The outputs on the BBB requested in the specify_bbb_input calls
    """
    json_to_send = json.dumps(io_to_send)
    response = client.json_request_response_bbb(json_to_send)
    return json.loads(response)


def get_bbb_input_value(bbb_return_data, pin_name):
    """
    Retrieves the value on the input 'pin_name' within the given
    'bbb_return_data'

    :param bbb_return_data: The data returned from
    'send_io_specifications_to_bbb()'
    :param pin_name: The pin name on which the BBB has received input
    :return: The value of the specified input to the BBB
    """
    return bbb_return_data[BBB_IO_CONSTANTS.INPUTS][pin_name]
