"""
A series of functions that manages communication between the Beagle Bone Black (BBB) and
allows the users to control inputs and outputs on the BBB
"""

import BBB_IO_CONSTANTS
import json


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
      "data": "i2c_data_here"
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


def connect_to_bbb():
    # TODO: Implement this function
    pass


def disconnect_from_bbb():
    # TODO: Implement this function
    pass


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

        :param i2c_spec_number: the order in which I2C signals should be sent
            to the circuit under test, with the lowest i2c_spec_number first
            (each i2c_spec_number must be unique for a given test)
        :param data: The data to be sent via I2C
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
    # TODO: send json_to_send to BBSM
    # TODO: received returned JSON from BBSM
    # TODO: parse json into a dictionary

    # return sample data for now
    return {
      BBB_IO_CONSTANTS.INPUTS: {
        list(io_to_send[BBB_IO_CONSTANTS.INPUTS].keys())[0]: list(io_to_send[
            BBB_IO_CONSTANTS.OUTPUTS].values())[0][BBB_IO_CONSTANTS.VALUE]
      }
    }


def get_bbb_input_value(bbb_return_data, pin_name):
    return bbb_return_data[BBB_IO_CONSTANTS.INPUTS][pin_name]
