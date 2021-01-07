import bbbio.BBB_IO_CONSTANTS as BBB_IO_CONSTANTS
import BNC_CONFIG

# All of the I2C functions below produce a dictionary of i2cset arguments that
# will alter one of the four registers in the PCA9534 IO expander:
# https://www.nxp.com/docs/en/data-sheet/PCA9534.pdf

# All pin_numbers are str in the form 0x[a-fA-F\d]{2} e.g. 0xa2
# in other words, they are 8 bits hex values

# Normal usage in robot:
#
# During test:
# ${i2c_output_1} =    Get I2C to Configure IO Expander IOs    ${I2C_PINNAME}
# Specify BBB I2C Output Dict    1    ${i2c_output_1}
# ${i2c_output_2} =    Get I2C for User IO Output Mode         ${I2C_PINNAME}
# Specify BBB I2C Output Dict    2    ${i2c_output_2}
#
# Test teardown:
# Reset BBB IO specifications
# ${i2c_output} =    Get I2C to Set All IO Expander IOs as Inputs
# Specify BBB I2C Output Dict    1    ${i2c_output}
# Send IO Specifications to BBB


def get_base_io_expander_i2c():
    """
    :return: dict: A dict containing the IO expander i2cbus and chip address
        on the BNC card
    """
    return {
        # i2c bus 2 on BBB is connected to IO expander
        BBB_IO_CONSTANTS.I2CBUS: "2",
        # i2c chip address = 0x27 for BNC card IO expander
        BBB_IO_CONSTANTS.I2C_CHIP_ADDRESS: "0x27"
    }


def bitwise_not_8bit_hex(pin_number):
    """
    Performs a bitwise not on an unsigned 8 bit hex number

    Examples:
    0x02 -> 0xfd
    0xf0 -> 0x0f
    0xa4 -> 0x5b

    :param pin_number: str: A 8 bit hex number
    :return: str: An 8 bit hex number representing the bitwise not of the input
    """
    pin_number_int = int(pin_number, 16)
    if 0 <= pin_number_int <= 255:
        raise ValueError(
            "pin_number {} is not between 0x00 and 0xff".format(pin_number))
    inverted_pin_number = 255 - pin_number_int
    return "{:#04x}".format(inverted_pin_number)


def get_base_io_expander_i2c_to_set_value():
    """
    :return: dict: A dict containing the IO expander i2cbus and chip address
        on the BNC card as well as the data address of the register that sets
        outputs on the IO expander
    """
    i2c_dict = get_base_io_expander_i2c()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA_ADDRESS] = "0x01"
    return i2c_dict


def assert_pin_controls_user_io(pin_number):
    """
    :param pin_number: str: An 8 bit hex number
    :return: bool: True if the 'pin_number' controls whether a user IO pin is
        an input or an output. Otherwise throws an AssertionError
    """
    if pin_number not in [BNC_CONFIG.I2C_BNC8_USER1_NIN_OUT,
                          BNC_CONFIG.I2C_BNC7_USER2_NIN_OUT]:
        raise AssertionError(
            "{} does not control a user IO pin".format(pin_number))
    return True


def get_i2c_for_user_io_input_mode(pin_number):
    """
    :param pin_number: str: A user IO pin number
    :return: A dictionary containing the information required to set a user IO
        to input mode on a BNC card through i2cset
    """
    assert_pin_controls_user_io(pin_number)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = bitwise_not_8bit_hex(pin_number)
    return i2c_dict


def get_i2c_for_user_io_output_mode(pin_number):
    """
    :param pin_number: str: A user IO pin number
    :return: A dictionary containing the information required to set a user IO
        to output mode on a BNC card through i2cset
    """
    assert_pin_controls_user_io(pin_number)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = pin_number
    return i2c_dict


def assert_pin_controls_open_drain_mode(pin_number):
    """
    :param pin_number: str: An 8 bit hex number
    :return: bool: True if the 'pin_number' on the IO expander controls the open
        drain/driven mode for VETO_OUT. Otherwise throws an AssertionError
    """
    if pin_number != BNC_CONFIG.I2C_BNC4_VETO_OUT_OC:
        raise AssertionError(
            "{} does not control a user IO pin".format(pin_number))
    return True


def get_i2c_for_driven_mode(pin_number):
    """
    :param pin_number: str: The BNC4_VETO_OUT_OC pin number on the IO expander
    :return: A dictionary containing the information required to set driven mode
        for VETO_OUT on a BNC card via i2cset
    """
    assert_pin_controls_open_drain_mode(pin_number)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = pin_number
    return i2c_dict


def get_i2c_for_open_drain_mode(pin_number):
    """
    :param pin_number: str: The BNC4_VETO_OUT_OC pin number on the IO expander
    :return: A dictionary containing the information required to set open drain
        mode for VETO_OUT on a BNC card via i2cset
    """
    assert_pin_controls_open_drain_mode(pin_number)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = bitwise_not_8bit_hex(pin_number)
    return i2c_dict


def assert_pin_controls_termination_resistance(pin_number):
    """
    :param pin_number: str: An 8 bit hex number
    :return: bool: True if the 'pin_number' controls the termination resistance
        of a BNC connector. Otherwise throws an AssertionError
    """
    if pin_number not in [BNC_CONFIG.I2C_BNC1_500HM_EN,
                          BNC_CONFIG.I2C_BNC6_500HM_EN,
                          BNC_CONFIG.I2C_BNC8_500_HM_EN,
                          BNC_CONFIG.I2C_BNC7_500_HM_EN]:
        raise AssertionError(
            "{} does not control a termination resistor".format(pin_number))
    return True


def get_i2c_to_enable_termination_resistor(pin_number):
    """
    :param pin_number: str: An IO expander pin number that controls termination
        resistance for a BNC connector
    :return: A dictionary containing the information required to enable the
        termination resistor on a BNC card via i2cset
    """
    assert_pin_controls_termination_resistance(pin_number)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = pin_number
    return i2c_dict


def get_i2c_to_disable_termination_resistor(pin_number):
    """
    :param pin_number: str: An IO expander pin number that controls termination
        resistance for a BNC connector
    :return: A dictionary containing the information required to disable the
        termination resistor on a BNC card via i2cset
    """
    assert_pin_controls_termination_resistance(pin_number)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = bitwise_not_8bit_hex(pin_number)
    return i2c_dict


def get_i2c_to_configure_io_expander_ios(pin_numbers):
    """
    Configures the 8 IO expander pins to be inputs or outputs. An 8 bit hex str
    is input. A 0 bit results in an input on a given pin and a 1 bit results
    in an output on a given pin

    Examples:
    0x00 -> All 8 IOs are inputs
    0x08 -> the 3rd IO (zero indexed) on the IO expander will be an output,
            all other IOs will be inputs
    0xf0 -> the 4th to 8th (inclusive) IOs (zero indexed) on the IO expander
            will be outputs, the 0th to 3rd IOs will be inputs
    0xfF -> All 8 IOs are outputs

    :param pin_numbers: str: A hex number representing the pins that should
        be set to an output. Case-insensitive
    :return: dict: A dictionary containing the 4 arguments to i2cset that will
        will be called on the BBB
    """
    i2c_dict = get_base_io_expander_i2c()
    # changes configuration register
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA_ADDRESS] = "0x03"
    inverted_pin_numbers = bitwise_not_8bit_hex(pin_numbers)
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = inverted_pin_numbers
    return i2c_dict


def get_i2c_to_set_all_io_expander_ios_as_inputs():
    return get_i2c_to_configure_io_expander_ios("0x00")
