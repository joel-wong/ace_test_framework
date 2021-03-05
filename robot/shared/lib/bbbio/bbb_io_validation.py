import BBB_IO_CONSTANTS
import BBB_IO_VALIDATION_CONSTANTS


def validate_pin_type(pin_number, pin_type, is_output):
    """
    Validates that the given 'pin_number' can be configured with the
    given 'pin_type' on the BBB

    :param pin_number: str: The pin number in the form Px_y
    :param pin_type: str: The pin type (e.g. digital_3v3)
    :param is_output: bool: True if the pin is configured as an output
    :return: None, if the pin type is valid. Otherwise raises an
        AssertionError
    """
    if pin_type == BBB_IO_CONSTANTS.DIGITAL_3V3:
        if pin_number not in BBB_IO_VALIDATION_CONSTANTS.DIGITAL_PINS:
            raise AssertionError(
                "Cannot specify pin '{}' as a digital pin".format(pin_number))
    elif pin_type == BBB_IO_CONSTANTS.ANALOG_1V8:
        if pin_number not in BBB_IO_VALIDATION_CONSTANTS.ANALOG_PINS:
            raise AssertionError(
                "Cannot specify pin '{}' as an analog pin".format(pin_number))
        elif is_output:
            raise AssertionError("Analog pins cannot be outputs")
    else:
        raise AssertionError("Pin type '{}' is not supported".format(pin_type))
    return True


def validate_bbb_output_value(output_type, value):
    """
    Validates that for the given 'output_type', the 'value' is valid on
    the BBB

    :param output_type: str: The output type (e.g. digital_3v3)
    :param value: str: The output value (e.g. "1")
    :return: None, if the value is valid for the output type. Otherwise
        raises an AssertionError
    """
    if output_type == BBB_IO_CONSTANTS.DIGITAL_3V3:
        if value not in [BBB_IO_CONSTANTS.DIGITAL_LOW,
                         BBB_IO_CONSTANTS.DIGITAL_HIGH]:
            raise ValueError("'{}' is not a valid digital output value".format(
                value))
    else:
        raise ValueError("Output type '{}' is not supported".format(output_type))
    return True


def validate_bbb_output(pin_number, output_type, value):
    """
    Validates that the given 'pin_number' can output 'output_type'
    with the given 'value' on the BBB

    :param pin_number: str: The pin number (e.g. P9_16)
    :param output_type: str: The output type (e.g. digital_3v3)
    :param value: str: The output value (e.g. "1")
    :return: None, if the value is valid for the output type on the given
        pin. Otherwise raises an AssertionError
    """
    validate_pin_type(pin_number, output_type, is_output=True)
    validate_bbb_output_value(output_type, value)


def validate_i2c(i2cbus, chip_address, data_address, data):
    """
    Validates that given I2C parameters are valid for the BBB

    :param i2cbus: str: The I2C bus (e.g. "2")
    :param chip_address: str: the chip address (e.g. 0x27)
    :param data_address: str: the data address (e.g. 0x01)
    :param data: str: the data to be sent (e.g. 0x02)
    :return: None, if the I2C parameters are valid for the BBB. Otherwise
        raises an AssertionError
    """
    if i2cbus not in BBB_IO_VALIDATION_CONSTANTS.I2C_BUSES:
        raise ValueError("i2cbus '{}' does not exist".format(
            i2cbus
        ))
    chip_address_int = int(chip_address, 16)
    if not (3 <= chip_address_int <= 119):
        raise ValueError(
            "I2C chip_address must be between 0x03 and 0x77 (inclusive)")
    data_address_int = int(data_address, 16)
    if not (0 <= data_address_int <= 255):
        raise ValueError(
            "I2C data_address must be between 0x00 and 0xFF (inclusive)")
    if data != "":
        # data can be empty in i2cset, if not validate that it is a
        # non-negative hex value
        data_int = int(data, 16)
        if not (0 <= data_int):
            raise ValueError("I2C data must be non-negative")


def validate_bbb_input(pin_number, input_type):
    """
    Validates that the given 'pin_number' can input 'input_type' on the BBB

    :param pin_number: str: The pin number (e.g. P9_16)
    :param input_type: str: The input type (e.g. digital_3v3)
    :return: None, if the input type is valid for the given
        pin. Otherwise raises an AssertionError
    """
    validate_pin_type(pin_number, input_type, is_output=False)
