import BBB_IO_CONSTANTS
import BBB_IO_VALIDATION_CONSTANTS


def validate_pin_type(pin_name, pin_type, is_output):
    if pin_type == BBB_IO_CONSTANTS.DIGITAL:
        if pin_name not in BBB_IO_VALIDATION_CONSTANTS.DIGITAL_PINS:
            raise AssertionError(
                "Cannot specify pin '{}' as a digital pin".format(pin_name))
    elif pin_type == BBB_IO_CONSTANTS.ANALOG:
        if pin_name not in BBB_IO_VALIDATION_CONSTANTS.ANALOG_PINS:
            raise AssertionError(
                "Cannot specify pin '{}' as an analog pin".format(pin_name))
        elif is_output:
            raise AssertionError("Analog pins cannot be outputs")
    else:
        raise AssertionError("Pin type '{}' is not supported".format(pin_type))
    return True


def validate_pin_not_specified(current_io_to_send, pin_name):
    if pin_name in current_io_to_send[BBB_IO_CONSTANTS.OUTPUTS]:
        raise AssertionError(
            "Output specification for pin '{}' already defined".format(pin_name))
    if pin_name in current_io_to_send[BBB_IO_CONSTANTS.INPUTS]:
        raise AssertionError(
            "Input specification for pin '{}' already defined".format(pin_name))
    return True


def validate_bbb_output_value(output_type, value):
    if output_type == BBB_IO_CONSTANTS.DIGITAL:
        if value not in [BBB_IO_CONSTANTS.DIGITAL_LOW,
                         BBB_IO_CONSTANTS.DIGITAL_HIGH]:
            raise ValueError("'{}' is not a valid digital output value".format(
                value))
    else:
        raise ValueError("Output type '{}' is not supported".format(output_type))
    return True


def validate_bbb_output(current_io_to_send, pin_name, output_type, value):
    validate_pin_not_specified(current_io_to_send, pin_name)
    validate_pin_type(pin_name, output_type, is_output=True)
    validate_bbb_output_value(output_type, value)


def validate_i2c(current_io_to_send, int_i2c_spec_number, i2cbus, chip_address,
                 data_address, data):
    if int_i2c_spec_number in current_io_to_send[BBB_IO_CONSTANTS.I2C]:
        raise AssertionError("I2C specification '{}' is already defined".format(
            int_i2c_spec_number
        ))
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


def validate_bbb_input(current_io_to_send, pin_name, input_type):
    validate_pin_not_specified(current_io_to_send, pin_name)
    validate_pin_type(pin_name, input_type, is_output=False)
