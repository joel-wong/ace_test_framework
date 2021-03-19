from ace_bbsm import BBB_IO_CONSTANTS as BIC
import BNC_CAPE_VALIDATION_CONSTANTS as CAPE_CONSTS
import BNC_CONFIG


class BNCValidator:

    @staticmethod
    def validate_suite(io_specifications):
        """
        Validates that the input 'io_specifications' contain a list of
        valid commands, in-order. Specifically checks that:
        - none of the commands will cause contention on the BNC Card
        - when an I2C command is run, its parameters are valid for
              the IO Expander on the BNC Card
        - digital inputs to the BBB are outputs on the BNC card
        - all configured pin numbers correspond to inputs and outputs
              on the custom signal conditioning board
        - other edge cases

        :param io_specifications: the list of input or output
            specifications that will be executed on the BBB.
            Note that an I2C specification is considered an output
            specification for the purpose of this framework
        :return: None, if the suite is valid, otherwise raises an
            AssertionError
        """
        for spec_num in range(len(io_specifications)):
            BNCValidator.validate_spec(spec_num, io_specifications)

    @staticmethod
    def validate_spec(spec_num, io_specifications):
        """
        Validates that the input or output at the index 'spec_num'
        in the io_specifications is valid for the BNC Card test suite.

        :param spec_num: The index of the specification to be validated
        :param io_specifications: the list of input, output, and I2C
            specifications that will be executed on the BBB
        :return: None, if the specification is valid, otherwise raises an
            AssertionError
        """
        spec = io_specifications[spec_num]
        if spec[BIC.SPEC_TYPE] == BIC.SPEC_TYPE_INPUT:
            BNCValidator.validate_spec_input(spec_num, io_specifications)
        elif spec[BIC.SPEC_TYPE] == BIC.SPEC_TYPE_OUTPUT:
            BNCValidator.validate_spec_output(spec_num, io_specifications)
        else:
            raise AssertionError(
                "spec type {} is invalid".format(spec[BIC.SPEC_TYPE]))

    @staticmethod
    def validate_spec_input(spec_num, io_specifications):
        """
        Validates that the input at the index 'spec_num'
        in the io_specifications is valid for the BNC Card test suite.

        :param spec_num: The index of the input specification to
            be validated.
        :param io_specifications: the list of input, output, and I2C
            specifications that will be executed on the BBB
        :return: None, if the specification is valid, otherwise raises an
            AssertionError
        """
        spec = io_specifications[spec_num]
        if spec[BIC.INPUT_TYPE] == BIC.DIGITAL_3V3:
            BNCValidator.validate_spec_input_digital(spec_num,
                                                     io_specifications)
        elif spec[BIC.INPUT_TYPE] == BIC.ANALOG_1V8:
            BNCValidator.validate_spec_input_analog(spec_num,
                                                    io_specifications)
        else:
            raise AssertionError(
                "{}-type input not supported".format(spec[BIC.INPUT_TYPE]))

    @staticmethod
    def validate_spec_input_digital(spec_num, io_specifications):
        """
        Validates that the digital input at the index 'spec_num'
        in the io_specifications is valid for the BNC Card test suite.

        :param spec_num: The index of the digital input specification to
            be validated.
        :param io_specifications: the list of input, output, and I2C
            specifications that will be executed on the BBB
        :return: None, if the specification is valid, otherwise raises an
            AssertionError
        """
        spec = io_specifications[spec_num]
        pin_number = spec[BIC.PIN_NUMBER]
        if pin_number not in CAPE_CONSTS.ALLOWED_DIGITAL_3V3_INPUT_PINS:
            raise AssertionError("{} is not a valid digital input pin for "
                                 "the BNC tests".format(pin_number))

        # Special case: User IO BNC Connectors
        # BNC Connector User IOs must be configured as outputs on the
        # BNC Card to be connected to inputs on the BBB
        if pin_number in [BNC_CONFIG.B_USER1_BI_DIR_L3V3,
                          BNC_CONFIG.B_USER2_BI_DIR_L3V3]:
            if pin_number == BNC_CONFIG.B_USER1_BI_DIR_L3V3:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC8_USER1_NIN_OUT
            else:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC7_USER2_NIN_OUT
            if not BNCValidator.is_user_io_in_output_mode(
                    spec_num, io_specifications, nin_out_bit_location):
                raise AssertionError(
                    "{} is set as input but the corresponding user IO on the "
                    "BNC card has been set to input mode, causing undefined "
                    "behaviour".format(pin_number))

        # Special case: User IO pin header in
        # Pin header User IOs must be configured as inputs on the BNC Card
        # to be connected to an input on the BBB
        if pin_number in [BNC_CONFIG.P_USER1_IN_TO_BBB,
                          BNC_CONFIG.P_USER2_IN_TO_BBB]:
            if pin_number == BNC_CONFIG.P_USER1_IN_TO_BBB:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC8_USER1_NIN_OUT
            else:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC7_USER2_NIN_OUT
            if BNCValidator.is_user_io_in_output_mode(
                    spec_num, io_specifications, nin_out_bit_location):
                raise AssertionError(
                    "{} is set as input but the corresponding user IO on the "
                    "BNC card has been set to output mode, causing undefined "
                    "behaviour".format(pin_number))

    @staticmethod
    def validate_spec_input_analog(spec_num, io_specifications):
        """
        Validates that the analog input at the index 'spec_num'
        in the io_specifications is valid for the BNC Card test suite.

        :param spec_num: The index of the analog input specification to
            be validated.
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :return: None, if the specification is valid, otherwise raises an
            AssertionError
        """
        pin_number = io_specifications[spec_num][BIC.PIN_NUMBER]
        if pin_number not in CAPE_CONSTS.ALLOWED_ANALOG_1V8_PINS:
            raise AssertionError("{} is not a valid analog input pin for"
                                 " the BNC tests".format(pin_number))

    @staticmethod
    def validate_spec_output(spec_num, io_specifications):
        """
        Validates that the output specification at the index 'spec_num'
        in the io_specifications is valid for the BNC Card test suite.

        :param spec_num: The index of the output specification to
            be validated.
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :return: None, if the specification is valid, otherwise raises an
            AssertionError
        """
        spec = io_specifications[spec_num]
        if spec[BIC.OUTPUT_TYPE] == BIC.DIGITAL_3V3:
            BNCValidator.validate_spec_output_digital(spec_num,
                                                      io_specifications)
        elif spec[BIC.OUTPUT_TYPE] == BIC.I2C:
            BNCValidator.validate_spec_output_i2c(spec_num, io_specifications)
        else:
            raise AssertionError(
                "{}-type output not supported".format(spec[BIC.OUTPUT_TYPE]))

    @staticmethod
    def validate_spec_output_digital(spec_num, io_specifications):
        """
        Validates that the digital output specification at the index 'spec_num'
        in the io_specifications is valid for the BNC Card test suite.

        :param spec_num: The index of the digital output specification to
            be validated.
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :return: None, if the specification is valid, otherwise raises an
            AssertionError
        """
        pin_number = io_specifications[spec_num][BIC.PIN_NUMBER]
        if pin_number not in CAPE_CONSTS.ALLOWED_DIGITAL_3V3_OUTPUT_PINS:
            raise AssertionError("{} is not a valid digital output pin for"
                                 " the BNC tests".format(pin_number))

        # Special case: User IO BNC Connectors
        # The User IOs must be configured as inputs on the BNC Card
        # to be connected to an output on the BBB
        if pin_number in [BNC_CONFIG.B_USER1_BI_DIR_L3V3,
                          BNC_CONFIG.B_USER2_BI_DIR_L3V3]:
            if pin_number == BNC_CONFIG.B_USER1_BI_DIR_L3V3:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC8_USER1_NIN_OUT
            else:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC7_USER2_NIN_OUT
            if BNCValidator.is_user_io_in_output_mode(
                    spec_num, io_specifications, nin_out_bit_location):
                raise AssertionError(
                    "{} is set as output but the corresponding user IO on the "
                    "BNC card has been set to output mode, possibly causing "
                    "contention".format(pin_number))

        # Special case: User IO pin header out
        # Pin Header User IOs must be configured as outputs on the BNC
        # Card to be connected to an output on the BBB
        if pin_number in [BNC_CONFIG.P_USER1_OUT_TO_LD,
                          BNC_CONFIG.P_USER2_OUT_TO_LD]:
            if pin_number == BNC_CONFIG.P_USER1_OUT_TO_LD:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC8_USER1_NIN_OUT
            else:
                nin_out_bit_location = BNC_CONFIG.I2C_BNC7_USER2_NIN_OUT
            if not BNCValidator.is_user_io_in_output_mode(
                    spec_num, io_specifications, nin_out_bit_location):
                raise AssertionError(
                    "{} is set as output but the corresponding user IO on the "
                    "BNC card has been set to input mode, possibly causing "
                    "contention".format(pin_number))

    @staticmethod
    def is_user_io_in_output_mode(spec_num, io_specifications,
                                  nin_out_bit_location):
        """
        Determines whether a User IO configured by the IO Expander is in
        input mode or output mode.
        Specifically checks whether the User IO configured by the 8 bit
        hex str 'nin_out_bit_location' (with exactly 1 bit high) has been
        configured as an output prior to the execution of the 'spec_num'
        IO specification (zero indexed).

        For a User IO to be in output mode, there must be two prior I2C
        specifications: one that sets the IO Expander pin to be an output
        and one that drives a value of 1 on the pin.

        :param spec_num: The index before which the state of the User IO
            is to be checked
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :param nin_out_bit_location: an 8 bit hex str representing the
            IO Expander bit that controls whether the User IO is in
            input mode or output mode
        :return: If the nin_out_bit_location does not control a User IO
            pin mode, then throws an AssertionError. Returns True if is
            the User IO will be in output mode before the io_specification
            at index spec_num is run. Otherwise returns False.
        """
        if nin_out_bit_location not in [BNC_CONFIG.I2C_BNC8_USER1_NIN_OUT,
                                        BNC_CONFIG.I2C_BNC7_USER2_NIN_OUT]:
            raise AssertionError("Invalid nin_out_bit_location")
        # check that the configuration register has been set so that
        # pin is in output mode
        if not BNCValidator.is_i2c_in_output_mode(
                spec_num, io_specifications, nin_out_bit_location):
            return False
        # check that the output register has been set so that the
        # IO Expander drives a 1 on the pin
        return BNCValidator.get_i2c_spec_bit_value(
                spec_num, io_specifications, nin_out_bit_location) == 1

    @staticmethod
    def is_i2c_in_output_mode(spec_num, io_specifications, bit_location):
        """
        Determines whether an IO Expander pin will be set as an input
        or output prior to the index 'spec_num' IO specification being
        executed

        :param spec_num: The index before which the state of the IO Expander
            pin is to be checked
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :param bit_location: an 8 bit hex str representing the
            IO Expander pin that will be in input mode or output mode
        :return: Returns True if is the IO Expander pin at bit_location
            will be in output mode before the io_specification
            at index 'spec_num' is run. Otherwise returns False.
        """
        bit_int_value = int(bit_location, 16)
        for prev_spec in io_specifications[spec_num-1::-1]:
            # find the most recent I2C command that modified the
            # IO Expander configuration register
            if BNCValidator.is_io_expander_spec(prev_spec):
                nin_out_bit_value = (int(prev_spec[BIC.I2C_DATA], 16) &
                                     bit_int_value)
                data_addr = prev_spec[BIC.I2C_DATA_ADDRESS]
                if data_addr == BNC_CONFIG.I2C_IO_EXPANDER_CONFIG_REGISTER:
                    # this is the most recent I2C command that modified the
                    # IO Expander configuration register
                    if nin_out_bit_value == 0:
                        # 0 bit means output
                        return True
                    else:
                        # 1 bit means input
                        return False
        # by default, is in input mode
        return False

    @staticmethod
    def get_i2c_spec_bit_value(spec_num, io_specifications, bit_location):
        """
        Determines the value of the bit at the given 'bit_location'
        in the output register

        Note that this only checks the configured value and does not check
        whether the pin is configured as an output. Use the
        'is_i2c_in_output_mode' method for that

        :param spec_num: The index before which the value of the IO Expander
            output register is to be checked
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :param bit_location: an 8 bit hex str representing the
            IO Expander bit whose value is going to be retrieved
        :return: Returns 1 if is the IO Expander output register has a
            1 value at the bit_location according to the specification.
            Otherwise returns 0
        """
        bit_int_value = int(bit_location, 16)
        for prev_spec in io_specifications[spec_num - 1::-1]:
            # find the most recent I2C command that modified the
            # IO Expander output register
            if BNCValidator.is_io_expander_spec(prev_spec):
                data_addr = prev_spec[BIC.I2C_DATA_ADDRESS]
                if data_addr == BNC_CONFIG.I2C_IO_EXPANDER_OUTPUT_REGISTER:
                    # this is the most recent I2C command that modified the
                    # IO Expander output register
                    if (int(prev_spec[BIC.I2C_DATA], 16) & bit_int_value) != 0:
                        return 1
                    return 0
        # no value specified. Default (according to IO Expander datasheet)
        # is 1
        return 1

    @staticmethod
    def is_io_expander_spec(spec):
        """
        Determines whether an IO specification is for the IO Expander
        on the BNC Card

        :param spec: The specification to be checked
        :return: Returns True if the specification is for the BNC Card
            IO Expander. Otherwise returns False.
        """
        if spec[BIC.SPEC_TYPE] != BIC.SPEC_TYPE_OUTPUT:
            return False
        if spec[BIC.OUTPUT_TYPE] != BIC.I2C:
            return False
        if spec[BIC.I2CBUS] != BNC_CONFIG.I2C_IO_EXPANDER_I2CBUS:
            return False
        chip_address = spec[BIC.I2C_CHIP_ADDRESS]
        if chip_address != BNC_CONFIG.I2C_IO_EXPANDER_CHIP_ADDRESS:
            return False
        return True

    @staticmethod
    def validate_spec_output_i2c(spec_num, io_specifications):
        """
        Validates that the I2C specification at the index 'spec_num'
        in the io_specifications is valid for the BNC Card test suite.

        :param spec_num: The index of the digital output specification to
            be validated.
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :return: None, if the specification is valid, otherwise raises an
            AssertionError
        """
        spec = io_specifications[spec_num]
        i2cbus = spec[BIC.I2CBUS]
        if i2cbus not in CAPE_CONSTS.ALLOWED_I2C_BUSES:
            raise AssertionError("{} is not a valid I2C bus for the BNC"
                                 " tests".format(i2cbus))

        chip_address = spec[BIC.I2C_CHIP_ADDRESS]
        if chip_address not in CAPE_CONSTS.ALLOWED_I2C_CHIP_ADDRESSES:
            raise AssertionError("{} is not a valid I2C chip address for "
                                 "the BNC tests".format(chip_address))

        data_address = spec[BIC.I2C_DATA_ADDRESS]
        if data_address not in CAPE_CONSTS.ALLOWED_I2C_DATA_ADDRESSES:
            raise AssertionError("{} is not a valid I2C data address for "
                                 "the BNC tests".format(data_address))

        is_setting_io_expander_config_register = (
            BNCValidator.is_io_expander_spec(spec) and
            data_address == BNC_CONFIG.I2C_IO_EXPANDER_CONFIG_REGISTER
        )
        if is_setting_io_expander_config_register:
            BNCValidator.validate_i2c_io_expander_config(spec_num,
                                                         io_specifications)
        is_setting_io_expander_output_register = (
            BNCValidator.is_io_expander_spec(spec) and
            data_address == BNC_CONFIG.I2C_IO_EXPANDER_OUTPUT_REGISTER
        )

        if is_setting_io_expander_output_register:
            BNCValidator.validate_i2c_io_expander_output(spec_num,
                                                         io_specifications)

    @staticmethod
    def validate_i2c_io_expander_config(spec_num, io_specifications):
        """
        Verifies that when there is a change to the config register in the
        IO specification, there is also a corresponding output register
        change *before* the config register change, unless that config
        register change sets all I2C lines to inputs

        Throws an AssertionError otherwise

        :param spec_num: Index of the specification to be checked
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :return: True, if the specification is valid, otherwise raises an
            AssertionError
        """
        spec = io_specifications[spec_num]
        data = spec[BIC.I2C_DATA]
        if int(data, 16) == 255:
            # setting everything to inputs, allow
            return True
        # otherwise this is setting at least one output
        # check that a previous step set the output I2C values
        for prev_spec in io_specifications[0:spec_num]:
            if not BNCValidator.on_same_i2c_device(prev_spec, spec):
                continue
            prev_data_addr = prev_spec[BIC.I2C_DATA_ADDRESS]
            if prev_data_addr == BNC_CONFIG.I2C_IO_EXPANDER_OUTPUT_REGISTER:
                # previously set output values, good to go
                return True
        raise AssertionError("Never set output values for IO Expander "
                             "but tried to set a pin as output")

    @staticmethod
    def validate_i2c_io_expander_output(spec_num, io_specifications):
        """
        Verifies that when there is a change to the output register in the
        IO specification, there is also a corresponding config register
        change either before or after the output register change

        Throws an AssertionError otherwise

        :param spec_num: Index of the specification to be checked
        :param io_specifications: the list of input and output
            specifications that will be executed on the BBB
        :return: True, if the specification is valid, otherwise raises an
            AssertionError
        """
        current_spec = io_specifications[spec_num]
        other_io_specifications = (
            io_specifications[:spec_num] + io_specifications[spec_num+1:])
        for other_spec in other_io_specifications:
            if not BNCValidator.on_same_i2c_device(other_spec, current_spec):
                continue
            prev_data_addr = other_spec[BIC.I2C_DATA_ADDRESS]
            if prev_data_addr == BNC_CONFIG.I2C_IO_EXPANDER_CONFIG_REGISTER:
                # other_spec is for config register
                if int(other_spec[BIC.I2C_DATA], 16) != 255:
                    # Setting at least one pin as output
                    return True

        raise AssertionError("Never set config values for IO Expander "
                             "but tried to set a pin as output")

    @staticmethod
    def on_same_i2c_device(spec_one, spec_two):
        """
        Determines whether two specifications configure the same I2C device

        :param spec_one: the first I2C specification to compare
        :param spec_two: the second I2C specification to compare
        :return: True, if the specifications are for the same I2C device.
            False otherwise
        """
        if spec_one[BIC.SPEC_TYPE] != BIC.SPEC_TYPE_OUTPUT:
            # not an output
            return False
        if spec_one[BIC.OUTPUT_TYPE] != BIC.I2C:
            # not I2C
            return False
        if spec_one[BIC.I2CBUS] != spec_two[BIC.I2CBUS]:
            # different bus
            return False
        if spec_one[BIC.I2C_CHIP_ADDRESS] != spec_two[BIC.I2C_CHIP_ADDRESS]:
            # different bus
            return False
        return True
