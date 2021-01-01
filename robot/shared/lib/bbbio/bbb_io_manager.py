"""
A series of functions that manages communication between the Beagle Bone Black (BBB) and
allows the users to control inputs and outputs on the BBB
"""

import json

import ace_bbsm

# Sample JSON that will be sent to the BBB when send_io_specifications_to_bbb()
# is called:
"""
{
    "outputs":{
    "P8-30": {
        "type": "digital",
        "value": "1"
    },
    "P8-40": {
        "type": "analog",
        "value": "1.8"
    },
    "P8-50": {
        "type": "pwm",
        "value": "60"
    }
  },
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
    io_to_send["inputs"] = {}
    io_to_send["outputs"] = {}


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
    io_to_send["outputs"][pin_name] = {
        "type": output_type,
        "value": value
    }


def specify_bbb_input(pin_name, input_type):
    """
    Updates the 'io_to_send' so that when
    'send_io_specifications_to_BBB' is called, the given 'input_type'
    is input on the given pin_name and the value is returned.

    :param pin_name: The pin name on which the BBB will have an input
    :param input_type: the type of signal that should be input on the BBB
    """
    io_to_send["inputs"][pin_name] = {
        "type": input_type
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
