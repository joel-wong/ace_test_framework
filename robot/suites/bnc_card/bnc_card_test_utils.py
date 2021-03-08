from ace_bbsm import BBB_IO_CONSTANTS

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
# Specify BBB I2C Output Dict    ${i2c_output_1}
# ${i2c_output_2} =    Get I2C for User IO Output Mode         ${I2C_PINNAME}
# Specify BBB I2C Output Dict    ${i2c_output_2}
#
# Test setup/teardown:
# Reset BBB IO specifications
# ${i2c_output} =    Get I2C to Set All IO Expander IOs as Inputs
# Specify BBB I2C Output Dict     ${i2c_output}
# Execute BNC Card Test via BBB


def get_base_io_expander_i2c():
    """
    Provides a dictionary containing the I2C information common to all
    i2cset commands for the BNC Card

    :return: dict: A dict containing the IO expander i2cbus and chip address
        on the BNC card
    """
    return {
        BBB_IO_CONSTANTS.I2CBUS:
            BNC_CONFIG.I2C_IO_EXPANDER_I2CBUS,
        BBB_IO_CONSTANTS.I2C_CHIP_ADDRESS:
            BNC_CONFIG.I2C_IO_EXPANDER_CHIP_ADDRESS
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
    if not (0 <= pin_number_int <= 255):
        raise ValueError(
            "pin_number {} is not between 0x00 and 0xff".format(pin_number))
    inverted_pin_number = 255 - pin_number_int
    return "{:#04x}".format(inverted_pin_number)


def get_base_io_expander_i2c_to_set_value():
    """
    In addition to using this function to set the output value of an IO
    expander pin, the IO expander must be configured to be an output.
    This can be done with the 'get_i2c_to_configure_io_expander_ios()'
    function.

    :return: dict: A dict containing the IO expander i2cbus and chip address
        on the BNC card as well as the data address of the register that sets
        outputs on the IO expander
    """
    i2c_dict = get_base_io_expander_i2c()
    i2c_dict[
        BBB_IO_CONSTANTS.I2C_DATA_ADDRESS
    ] = BNC_CONFIG.I2C_IO_EXPANDER_OUTPUT_REGISTER
    return i2c_dict


def assert_pin_controls_user_io(i2c_pin):
    """
    Validates that the input 'i2c_pin' controls whether a User IO
    is an input or output on the BNC card

    :param i2c_pin: str: An 8 bit hex number
    :return: bool: True if the 'i2c_pin' controls whether a user IO pin is
        an input or an output. Otherwise throws an AssertionError
    """
    if i2c_pin not in [BNC_CONFIG.I2C_BNC8_USER1_NIN_OUT,
                       BNC_CONFIG.I2C_BNC7_USER2_NIN_OUT]:
        raise AssertionError(
            "{} does not control a user IO pin".format(i2c_pin))
    return True


def get_i2c_for_user_io_input_mode(i2c_pin):
    """
    Returns a dictionary containing the information required by an
    i2cset command to set the user IO controlled by the
    'i2c_pin' on the BNC card to input mode

    :param i2c_pin: str: A user IO pin number
        Note that i2c_pin is not necessary to achieve the purpose
        of this function but we still make it a required argument for
        consistency and clarity
    :return: dict: Parameters to i2cset for setting the appropriate
        User IO to input mode
    """
    assert_pin_controls_user_io(i2c_pin)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = "0x00"
    return i2c_dict


def get_i2c_for_user_io_output_mode(i2c_pin):
    """
    Returns a dictionary containing the information required by an
    i2cset command to set the user IO controlled by the
    'i2c_pin' on the BNC card to output mode

    :param i2c_pin: str: A user IO pin number
    :return: dict: Parameters to i2cset for setting the appropriate
        User IO to output mode
    """
    assert_pin_controls_user_io(i2c_pin)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = i2c_pin
    return i2c_dict


def assert_pin_controls_open_drain_mode(i2c_pin):
    """
    Validates that the input 'i2c_pin' controls whether VETO_OUT
    is in open drain or driven mode

    :param i2c_pin: str: An 8 bit hex number
    :return: bool: True if the 'i2c_pin' on the IO expander controls the open
        drain/driven mode for VETO_OUT. Otherwise throws an AssertionError
    """
    if i2c_pin != BNC_CONFIG.I2C_BNC4_VETO_OUT_OC:
        raise AssertionError(
            "{} does not control a user IO pin".format(i2c_pin))
    return True


def get_i2c_for_driven_mode(i2c_pin):
    """
    Returns a dictionary containing the information required by an
    i2cset command to set the VETO_OUT on the BNC card
    (controlled by the 'i2c_pin') to driven mode

    :param i2c_pin: str: The BNC4_VETO_OUT_OC pin number on the IO expander
    :return: dict: Parameters to i2cset for setting VETO_OUT to driven
        mode
    """
    assert_pin_controls_open_drain_mode(i2c_pin)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = i2c_pin
    return i2c_dict


def get_i2c_for_open_drain_mode(i2c_pin):
    """
    Returns a dictionary containing the information required by an
    i2cset command to set the VETO_OUT on the BNC card
    (controlled by the 'i2c_pin') to open drain mode

    :param i2c_pin: str: The BNC4_VETO_OUT_OC pin number on the IO expander
        Note that i2c_pin is not necessary to achieve the purpose
        of this function but we still make it a required argument for
        consistency and clarity
    :return: dict: Parameters to i2cset for setting VETO_OUT to open drain
        mode
    """
    assert_pin_controls_open_drain_mode(i2c_pin)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = "0x00"
    return i2c_dict


def assert_pin_controls_termination_resistance(i2c_pin):
    """
    Validates that the input 'i2c_pin' controls whether a termination
    resistor is enabled or disabled

    :param i2c_pin: str: An 8 bit hex number
    :return: bool: True if the 'i2c_pin' controls the termination resistance
        of a BNC connector. Otherwise throws an AssertionError
    """
    if i2c_pin not in [BNC_CONFIG.I2C_BNC1_500HM_EN,
                       BNC_CONFIG.I2C_BNC6_500HM_EN,
                       BNC_CONFIG.I2C_BNC8_500_HM_EN,
                       BNC_CONFIG.I2C_BNC7_500_HM_EN]:
        raise AssertionError(
            "{} does not control a termination resistor".format(i2c_pin))
    return True


def get_i2c_to_enable_termination_resistor(i2c_pin):
    """
    Returns a dictionary containing the information required by an
    i2cset command to set the BNC connector controlled by the
    given 'i2c_pin' to have a 50 ohm termination resistance

    :param i2c_pin: str: An IO expander pin number that controls the
        termination resistance for a BNC connector
    :return: dict: Parameters to i2cset that enable a termination
        resistor on the BNC card
    """
    assert_pin_controls_termination_resistance(i2c_pin)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = i2c_pin
    return i2c_dict


def get_i2c_to_disable_termination_resistor(i2c_pin):
    """
    Returns a dictionary containing the information required by an
    i2cset command to set the BNC connector controlled by the
    given 'i2c_pin' to have a high input impedance

    :param i2c_pin: str: An IO expander pin number that controls the
        termination resistance for a BNC connector
        Note that i2c_pin is not necessary to achieve the purpose
        of this function but we still make it a required argument for
        consistency and clarity
    :return: dict: Parameters to i2cset that disable a termination
        resistor on the BNC card
    """
    assert_pin_controls_termination_resistance(i2c_pin)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = "0x00"
    return i2c_dict


def assert_pin_controls_led(i2c_pin):
    """
    Validates that the input 'i2c_pin' controls whether an LED on
    the BNC Card

    :param i2c_pin: str: An 8 bit hex number
    :return: bool: True if the 'i2c_pin' controls an LED. Otherwise throws
        an AssertionError
    """
    if i2c_pin != BNC_CONFIG.I2C_RLED:
        raise AssertionError(
            "{} does not control an LED".format(i2c_pin))
    return True


def get_i2c_to_turn_on_led(i2c_pin):
    """
    Returns a dictionary containing the information required by an
    i2cset command to turn on an LED using the given 'i2c_pin'

    :param i2c_pin: str: The IO expander pin number that controls the orange
        LED. Note that to turn on the orange LED, the green LED must already be
        on (which occurs if TDC_LED is set to low)
        Note that i2c_pin is not necessary to achieve the purpose
        of this function but we still make it a required argument for
        consistency and clarity
    :return: dict: Parameters to i2cset that turn on an LED on the BNC card
    """
    assert_pin_controls_led(i2c_pin)
    i2c_dict = get_base_io_expander_i2c_to_set_value()
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = "0x00"
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
    i2c_dict[
        BBB_IO_CONSTANTS.I2C_DATA_ADDRESS
    ] = BNC_CONFIG.I2C_IO_EXPANDER_CONFIG_REGISTER
    inverted_pin_numbers = bitwise_not_8bit_hex(pin_numbers)
    i2c_dict[BBB_IO_CONSTANTS.I2C_DATA] = inverted_pin_numbers
    return i2c_dict


def get_i2c_to_set_all_io_expander_ios_as_inputs():
    """
    Returns a dictionary containing the information required by an
    i2cset command to set all pins on the IO Expander to inputs

    :return: dict: A dictionary containing the required 4 arguments to
        i2cset
    """
    return get_i2c_to_configure_io_expander_ios("0x00")
