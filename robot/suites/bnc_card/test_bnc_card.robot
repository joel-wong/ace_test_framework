*** Settings ***
Documentation    Test Suite for the SKF G5 BNC Card

Library      Collections
Library      Dialogs

Variables    ace_bbsm/BBB_IO_CONSTANTS.py
Library      bbbio/bbb_io_manager.py
Variables    manual/MANUAL_TEST_CONSTANTS.py

Library      bnc_card_test_utils.py
Variables    BNC_CONFIG.py

Suite Setup    Setup BBB For BNC Card Tests
Test Setup     Set BNC Card and BeagleBone IOs Back to Inputs

Suite Teardown    Reset BNC Card and BBB IOs then Disconnect From BBB

*** Variables ***
${CURRENT_AND_VOLTAGE_SENSING}    CURRENT_AND_VOLTAGE_SENSING

${PIN_HEADER_OUT_EQUALS_BNC_IN}    PIN_HEADER_OUT_EQUALS_BNC_IN
# Tag: PIN_HEADER_OUT_EQUALS_BNC_IN
# Tests that when a digital signal is input to a specified BNC connector, the
# same signal is output on the appropriate pin header

${USER_IO_DEFAULT_INPUT}    USER_IO_DEFAULT_INPUT
# Tag: USER_IO_DEFAULT_INPUT
# Tests that when a digital signal is input to a user IO BNC connector, the
# same signal is output on the appropriate USER_OUT pin header by default

${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}    BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN
# Tag: BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN
# Tests that when a digital signal is input to a specified pin header, the
# negation of the signal is output on the appropriate BNC connector

${USER_IO_OUTPUT}    USER_IO_OUTPUT_NEGATED
# Tag: USER_IO_OUTPUT
# Tests that when a digital signal is input to a User IO pin header with the
# User IO set to output mode, the negation of the signal is output on the
# appropriate BNC connector

${TERMINATION_RESISTOR_CHECK}      TERMINATION_RESISTOR_CHECK
# Tag: TERMINATION_RESISTOR_CHECK
# Tests that the terminiation resistor can be enabled and disabled for a
# specified BNC connector

${OPEN_DRAIN_FUNCTIONALITY_CHECK}    OPEN_DRAIN_FUNCTIONALITY_CHECK
# Tag: OPEN_DRAIN_FUNCTIONALITY_CHECK
# Tests that the open drain mode is enabled when set via I2C input

${LED_CHECK}    LED_CHECK
# Tag: OPEN_DRAIN_FUNCTIONALITY_CHECK
# Tests that the open drain mode is enabled when set via I2C input

${ABORT_MESSAGE}    Voltage or current limits exceeded. Remove circuit card from BeagleBone immediately
${VETO_OUT_DEFAULT_OPEN_DRAIN_MESSAGE}    Veto out should be in open drain mode by default
${VETO_OUT_FORCED_OPEN_DRAIN_MESSAGE}    When the open drain mode is set (not just default), it should still negate VETO_OUT
${USER_IO_DEFAULT_INPUT_MESSAGE}    User IOs should be in input mode by default
${LED_OFF_CHECK_MESSAGE}    Press PASS if the BNC Card LED is \n\n*** OFF ***\n\n otherwise press FAIL

*** Test Cases ***

Current Sense 3.3V Bus
    [Tags]    ${CURRENT_AND_VOLTAGE_SENSING}
    Specify BBB Analog Input    ${ADC_3V3_C_SENSE_TO_AIN}
    Execute BNC Card Test via BBB
    ${pin_values} =    Get BBB Input Value    ${ADC_3V3_C_SENSE_TO_AIN}
    ${analog_value} =    Set Variable    ${pin_values[0]}
    Run Keyword If    ${ADC_3V3_C_SENSE_ANALOG_MAXIMUM} <= ${analog_value}
    ...    Pause Execution    ${ABORT_MESSAGE}
    Run Keyword If    ${ADC_3V3_C_SENSE_ANALOG_MAXIMUM} <= ${analog_value}    Fatal Error
    # Technically the next line will always be true if we complete the previous
    # two lines without errors, but we keep it anyway for test report clarity
    Should Be True    ${analog_value} < ${ADC_3V3_C_SENSE_ANALOG_MAXIMUM}

Current Sense 5V Bus
    [Tags]    ${CURRENT_AND_VOLTAGE_SENSING}
    Specify BBB Analog Input    ${ADC_5V_C_SENSE_TO_AIN}
    Execute BNC Card Test via BBB
    ${pin_values} =    Get BBB Input Value    ${ADC_5V_C_SENSE_TO_AIN}
    ${analog_value} =    Set Variable    ${pin_values[0]}
    Run Keyword If    ${ADC_5V_C_SENSE_ANALOG_MAXIMUM} <= ${analog_value}
    ...    Pause Execution    ${ABORT_MESSAGE}
    Run Keyword If    ${ADC_5V_C_SENSE_ANALOG_MAXIMUM} <= ${analog_value}    Fatal Error
    # Technically the next line will always be true if we complete the previous
    # two lines without errors, but we keep it anyway for test report clarity
    Should Be True    ${analog_value} < ${ADC_5V_C_SENSE_ANALOG_MAXIMUM}

Voltage Sense 5V Bus
    [Tags]    ${CURRENT_AND_VOLTAGE_SENSING}
    Specify BBB Analog Input    ${VDD_5V_TO_AIN}
    Execute BNC Card Test via BBB
    ${pin_values} =    Get BBB Input Value    ${VDD_5V_TO_AIN}
    ${analog_value} =    Set Variable    ${pin_values[0]}
    # if we are exceeding maximum, do not run any additional tests
    Run Keyword If    ${analog_value} <= ${VDD_5V_ANALOG_MINIMUM}
    ...    Pause Execution    ${ABORT_MESSAGE}
    Run Keyword If    ${analog_value} <= ${VDD_5V_ANALOG_MINIMUM}    Fatal Error
    # Technically the next line will always be true if we complete the previous
    # two lines without errors, but we keep it anyway for test report clarity
    Should Be True    ${VDD_5V_ANALOG_MINIMUM} < ${analog_value}
    Run Keyword If    ${VDD_5V_ANALOG_MAXIMUM} <= ${analog_value}
    ...    Pause Execution    ${ABORT_MESSAGE}
    Run Keyword If    ${VDD_5V_ANALOG_MAXIMUM} <= ${analog_value}    Fatal Error
    # Technically the next line will always be true if we complete the previous
    # two lines without errors, but we keep it anyway for test report clarity
    Should Be True    ${analog_value} < ${VDD_5V_ANALOG_MAXIMUM}



Check BNC1 REF_IN Input = Pin Header REF_IN For Digital High
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check BNC to Pin Header High Passed Through    ${B_REF_IN_TO_EUT_L3V3}    ${P_REF_IN_TO_BBB}

Check BNC1 REF_IN Input = Pin Header REF_IN For Digital Low
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check BNC to Pin Header Low Passed Through    ${B_REF_IN_TO_EUT_L3V3}    ${P_REF_IN_TO_BBB}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital High
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check BNC to Pin Header High Passed Through    ${B_SYNC_IN_TO_EUT_L3V3}    ${P_SYNC_IN_TO_BBB}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital Low
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check BNC to Pin Header Low Passed Through    ${B_SYNC_IN_TO_EUT_L3V3}    ${P_SYNC_IN_TO_BBB}


Check BNC8 USER1 IO Input = Pin Header USER1 IO For Digital High With Default I2C Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check User IO BNC to Pin Header High Passed Through    ${B_USER1_BI_DIR_L3V3}    ${P_USER1_IN_TO_BBB}

Check BNC8 USER1 IO Input = Pin Header USER1 IO For Digital Low With Default I2C Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check User IO BNC to Pin Header Low Passed Through    ${B_USER1_BI_DIR_L3V3}    ${P_USER1_IN_TO_BBB}

Check BNC7 USER2 IO Input = Pin Header USER2 IO For Digital High With Default I2C Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check User IO BNC to Pin Header High Passed Through    ${B_USER2_BI_DIR_L3V3}    ${P_USER2_IN_TO_BBB}

Check BNC7 USER2 IO Input = Pin Header USER2 IO For Digital Low With Default I2C Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check User IO BNC to Pin Header Low Passed Through    ${B_USER2_BI_DIR_L3V3}    ${P_USER2_IN_TO_BBB}


#Check BNC8 USER1 IO Input = Pin Header USER1 IO For Digital High With I2C Input Mode
#    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
#    Check User IO BNC to Pin Header High Passed Through in Forced Input Mode
#    ...    ${I2C_BNC8_USER1_NIN_OUT}    ${B_USER1_BI_DIR_L3V3}    ${P_USER1_IN_TO_BBB}
#
#Check BNC8 USER1 IO Input = Pin Header USER1 IO For Digital Low With I2C Input Mode
#    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
#    Check User IO BNC to Pin Header Low Passed Through in Forced Input Mode
#    ...    ${I2C_BNC8_USER1_NIN_OUT}    ${B_USER1_BI_DIR_L3V3}    ${P_USER1_IN_TO_BBB}
#
#Check BNC7 USER2 IO Input = Pin Header USER2 IO For Digital High With I2C Input Mode
#    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
#    Check User IO BNC to Pin Header High Passed Through in Forced Input Mode
#    ...    ${I2C_BNC7_USER2_NIN_OUT}    ${B_USER2_BI_DIR_L3V3}    ${P_USER2_IN_TO_BBB}
#
#Check BNC7 USER2 IO Input = Pin Header USER2 IO For Digital Low With I2C Input Mode
#    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
#    Check User IO BNC to Pin Header Low Passed Through in Forced Input Mode
#    ...    ${I2C_BNC7_USER2_NIN_OUT}    ${B_USER2_BI_DIR_L3V3}    ${P_USER2_IN_TO_BBB}


Check Pin Header REF_OUT Input is Negated on BNC2 REF_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header to BNC High Negated    ${P_REF_OUT_TO_LD}    ${B_REF_OUT_TO_BBB_L3V3}

Check Pin Header REF_OUT Input is Negated on BNC2 REF_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header to BNC Low Negated    ${P_REF_OUT_TO_LD}    ${B_REF_OUT_TO_BBB_L3V3}

Check Pin Header TDC_OUT Input is Negated on BNC3 TDC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header to BNC High Negated    ${P_TDC_OUT_TO_LD}    ${B_TDC_OUT_TO_BBB_L3V3}

Check Pin Header TDC_OUT Input is Negated on BNC3 TDC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header to BNC Low Negated    ${P_TDC_OUT_TO_LD}    ${B_TDC_OUT_TO_BBB_L3V3}

Check Pin Header VETO_OUT Input is Negated on BNC4 VETO_OUT Output For Digital High With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Set Veto Out To Driven Mode
    Check Pin Header to BNC High Negated    ${P_VETO_OUT_TO_LD}    ${B_VETO_OUT_TO_BBB_L3V3}

Check Pin Header VETO_OUT Input is Negated on BNC4 VETO_OUT Output For Digital Low With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Set Veto Out To Driven Mode
    Check Pin Header to BNC Low Negated    ${P_VETO_OUT_TO_LD}    ${B_VETO_OUT_TO_BBB_L3V3}

Check Pin Header SYNC_OUT Input is Negated on BNC5 SYNC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header to BNC High Negated    ${P_SYNC_OUT_TO_LD}    ${B_SYNC_OUT_TO_BBB_L3V3}

Check Pin Header SYNC_OUT Input is Negated on BNC5 SYNC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header to BNC Low Negated    ${P_SYNC_OUT_TO_LD}    ${B_SYNC_OUT_TO_BBB_L3V3}


Check Pin Header USER1_IO Input is Negated on BNC8 USER1_IO Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check User IO Pin Header To BNC High Negated
    ...    ${I2C_BNC8_USER1_NIN_OUT}    ${P_USER1_OUT_TO_LD}    ${B_USER1_BI_DIR_L3V3}

Check Pin Header USER1_IO Input is Negated on BNC8 USER1_IO Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check User IO Pin Header To BNC Low Negated
    ...    ${I2C_BNC8_USER1_NIN_OUT}    ${P_USER1_OUT_TO_LD}    ${B_USER1_BI_DIR_L3V3}

Check Pin Header USER2_IO Input is Negated on BNC7 USER2_IO Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check User IO Pin Header To BNC High Negated
    ...    ${I2C_BNC7_USER2_NIN_OUT}    ${P_USER2_OUT_TO_LD}    ${B_USER2_BI_DIR_L3V3}

Check Pin Header USER2_IO Input is Negated on BNC7 USER2_IO Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check User IO Pin Header To BNC Low Negated
    ...    ${I2C_BNC7_USER2_NIN_OUT}    ${P_USER2_OUT_TO_LD}    ${B_USER2_BI_DIR_L3V3}



Check BNC1 REF_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled
    ...    ${I2C_BNC1_500HM_EN}    ${B_REF_IN_TO_EUT_L3V3}    ${TR_REF_IN_TO_AIN}

Check BNC1 REF_IN Termination Resistor Is Default Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Is Default Disabled
    ...    ${B_REF_IN_TO_EUT_L3V3}    ${TR_REF_IN_TO_AIN}

#Check BNC1 REF_IN Termination Resistor Can Be Force Disabled
#    [Tags]    ${TERMINATION_RESISTOR_CHECK}
#    Check Termination Resistor Can Be Force Disabled
#    ...    ${I2C_BNC1_500HM_EN}    ${B_REF_IN_TO_EUT_L3V3}    ${TR_REF_IN_TO_AIN}

Check BNC6 SYNC_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled
    ...    ${I2C_BNC6_500HM_EN}    ${B_SYNC_IN_TO_EUT_L3V3}    ${TR_SYNC_IN_TO_AIN}

Check BNC6 SYNC_IN Termination Resistor Is Default Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Is Default Disabled
    ...    ${B_SYNC_IN_TO_EUT_L3V3}    ${TR_SYNC_IN_TO_AIN}

#Check BNC6 SYNC_IN Termination Resistor Can Be Disabled
#    [Tags]    ${TERMINATION_RESISTOR_CHECK}
#    Check Termination Resistor Can Be Force Disabled
#    ...    ${I2C_BNC6_500HM_EN}    ${B_SYNC_IN_TO_EUT_L3V3}    ${TR_SYNC_IN_TO_AIN}


Check BNC8 USER1_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check User IO Termination Resistor Can Be Enabled
    ...    ${I2C_BNC8_500_HM_EN}    ${B_USER1_BI_DIR_L3V3}    ${TR_USER1_TO_AIN}

Check BNC8 USER1_IO Termination Resistor Is Default Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check User IO Termination Resistor Is Default Disabled
    ...    ${B_USER1_BI_DIR_L3V3}    ${TR_USER1_TO_AIN}

#Check BNC8 USER1_IO Termination Resistor Can Be Force Disabled
#    [Tags]    ${TERMINATION_RESISTOR_CHECK}
#    Check User IO Termination Resistor Can Be Force Disabled
#    ...    ${I2C_BNC8_500_HM_EN}    ${B_USER1_BI_DIR_L3V3}    ${TR_USER1_TO_AIN}


Check BNC7 USER2_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check User IO Termination Resistor Can Be Enabled
    ...    ${I2C_BNC7_500_HM_EN}    ${B_USER2_BI_DIR_L3V3}    ${TR_USER2_TO_AIN}

Check BNC7 USER2_IO Termination Resistor Is Default Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check User IO Termination Resistor Is Default Disabled
    ...    ${B_USER2_BI_DIR_L3V3}    ${TR_USER2_TO_AIN}

#Check BNC7 USER2_IO Termination Resistor Can Be Force Disabled
#    [Tags]    ${TERMINATION_RESISTOR_CHECK}
#    Check User IO Termination Resistor Can Be Force Disabled
#    ...    ${I2C_BNC7_500_HM_EN}    ${B_USER2_BI_DIR_L3V3}    ${TR_USER2_TO_AIN}



Check Pin Header VETO_OUT High Input has Low Output on BNC4 VETO_OUT With Default Mode
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Log    ${VETO_OUT_DEFAULT_OPEN_DRAIN_MESSAGE}
    Log    A digital high input is automatically negated as the input to an NMOS
    Log    With open drain mode, there should have a high impedence output
    Log    Due to a pull up resistor, this should result in a digital high output
    Check Pin Header to BNC High Passed Through    ${P_VETO_OUT_TO_LD}    ${B_VETO_OUT_TO_BBB_L3V3}

Check Pin Header VETO_OUT Low Input has High Impedence Output on BNC4 VETO_OUT With Default Mode
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Log    ${VETO_OUT_DEFAULT_OPEN_DRAIN_MESSAGE}
    Log    A digital low input with open drain mode should drive a low output
    Check Pin Header to BNC Low Passed Through    ${P_VETO_OUT_TO_LD}    ${B_VETO_OUT_TO_BBB_L3V3}


#Check Pin Header VETO_OUT High Input has Low Output on BNC4 VETO_OUT With Open Drain Mode
#    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
#    Log    ${VETO_OUT_FORCED_OPEN_DRAIN_MESSAGE}
#    Set Veto Out To Open Drain Mode
#    Check Pin Header to BNC High Passed Through    ${P_VETO_OUT_TO_LD}    ${B_VETO_OUT_TO_BBB_L3V3}

#Check Pin Header VETO_OUT Low Input has High Impedence Output on BNC4 VETO_OUT With Open Drain Mode
#    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
#    Log    ${VETO_OUT_FORCED_OPEN_DRAIN_MESSAGE}
#    Set Veto Out To Open Drain Mode
#    Check Pin Header to BNC Low Passed Through    ${P_VETO_OUT_TO_LD}    ${B_VETO_OUT_TO_BBB_L3V3}


Check Green LED
    [Tags]    ${LED_CHECK}    ${MANUAL_TEST_TAG}
    Execute Manual Step    ${LED_OFF_CHECK_MESSAGE}
    Specify BBB Digital Output    ${P_TDC_LED_TO_LD}    ${DIGITAL_LOW}
    Enable Line Drivers
    Execute BNC Card Test via BBB
    Execute Manual Step    Press PASS if the LED on the BNC card is \n\n*** GREEN ***\n\n, otherwise press FAIL

Check Orange LED
    [Tags]    ${LED_CHECK}    ${MANUAL_TEST_TAG}
    Execute Manual Step    ${LED_OFF_CHECK_MESSAGE}
    ${turn_red_led_on_i2c} =    Get I2C to Turn on LED    ${I2C_RLED}
    Specify BBB I2C Output Dict    ${turn_red_led_on_i2c}
    Set IO Expander Pin to Output    ${I2C_RLED}
    Specify BBB Digital Output    ${P_TDC_LED_TO_LD}    ${DIGITAL_LOW}
    Enable Line Drivers
    Execute BNC Card Test via BBB
    Execute Manual Step    Press PASS if the LED on the BNC card is \n\n*** ORANGE ***\n\n, otherwise press FAIL



*** Keywords ***
Setup BBB For BNC Card Tests
    # TODO: Add detailed manual instructions for setting up tests
    Execute Manual Step    During development, remove all external circuitry from the BeagleBone. Press PASS when complete.

    # set up a socket connection to BBB
    Connect To BBB

Execute BNC Card Test via BBB
    Send IO Specifications to BBB    ${NONE}

Set BNC Card and BeagleBone IOs Back to Inputs
    Reset BBB IO Specifications
    ${all_input_i2c} =    Get I2C to Set All IO Expander IOs As Inputs
    Specify BBB I2C Output Dict    ${all_input_i2c}
    Log     BeagleBone IOs are automatically set to inputs when receiving an IO Specification
    Execute BNC Card Test via BBB
    Reset BBB IO Specifications

Reset BNC Card and BBB IOs then Disconnect From BBB
    Set BNC Card and BeagleBone IOs Back to Inputs
    Disconnect from BBB

Enable Level Shifters
    Log    Enables level shifting on all signals
    Specify BBB Digital Output    ${OE_LS}    ${DIGITAL_LOW}

Enable Line Drivers
    Log    Enables line drivers on all signals
    Specify BBB Digital Output    ${OE_LD}    ${DIGITAL_LOW}

Check BNC to Pin Header High Passed Through
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Digital Output    ${bbb_output_pin}    ${DIGITAL_HIGH}
    Enable Level Shifters
    Enable Line Drivers
    Specify BBB Digital Input     ${bbb_input_pin}
    Execute BNC Card Test via BBB
    ${pin_output} =       Get BBB Input Value    ${bbb_input_pin}
    Should Be Equal       ${pin_output[0]}    ${DIGITAL_HIGH}

Check BNC to Pin Header Low Passed Through
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Digital Output    ${bbb_output_pin}    ${DIGITAL_LOW}
    Enable Level Shifters
    Enable Line Drivers
    Specify BBB Digital Input     ${bbb_input_pin}
    Execute BNC Card Test via BBB
    ${pin_output} =       Get BBB Input Value    ${bbb_input_pin}
    Should Be Equal       ${pin_output[0]}    ${DIGITAL_LOW}

Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    # Note that this doesn't actually turn on the User IO level shifter.
    # To do that, you will need to call the 'Enable Level Shifters'
    # function
    Specify BBB Digital Output    ${DIR_L3}    ${DIGITAL_HIGH}

Check User IO BNC to Pin Header High Passed Through
    [Arguments]    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}
    Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Check BNC to Pin Header High Passed Through    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}

Check User IO BNC to Pin Header Low Passed Through
    [Arguments]    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}
    Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Check BNC to Pin Header Low Passed Through    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}

Check User IO BNC to Pin Header High Passed Through in Forced Input Mode
    [Arguments]    ${pin_i2c_name}    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}
    Specify User IO Input Mode    ${pin_i2c_name}
    Check User IO BNC to Pin Header High Passed Through
    ...    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}

Check User IO BNC to Pin Header Low Passed Through in Forced Input Mode
    [Arguments]    ${pin_i2c_name}    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}
    Specify User IO Input Mode    ${pin_i2c_name}
    Check User IO BNC to Pin Header Low Passed Through
    ...    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}

Check Pin Header to BNC High Negated
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Digital Output    ${bbb_output_pin}    ${DIGITAL_HIGH}
    Enable Line Drivers
    Enable Level Shifters
    Specify BBB Digital Input     ${bbb_input_pin}
    Execute BNC Card Test via BBB
    ${pin_output} =       Get BBB Input Value    ${bbb_input_pin}
    Should Be Equal       ${pin_output[0]}    ${DIGITAL_LOW}

Check Pin Header to BNC Low Negated
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Digital Output    ${bbb_output_pin}    ${DIGITAL_LOW}
    Enable Line Drivers
    Enable Level Shifters
    Specify BBB Digital Input     ${bbb_input_pin}
    Execute BNC Card Test via BBB
    ${pin_output} =       Get BBB Input Value    ${bbb_input_pin}
    Should Be Equal       ${pin_output[0]}    ${DIGITAL_HIGH}

Check Pin Header to BNC High Passed Through
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Digital Output    ${bbb_output_pin}    ${DIGITAL_HIGH}
    Enable Line Drivers
    Enable Level Shifters
    Specify BBB Digital Input     ${bbb_input_pin}
    Execute BNC Card Test via BBB
    ${pin_output} =       Get BBB Input Value    ${bbb_input_pin}
    Should Be Equal       ${pin_output[0]}    ${DIGITAL_HIGH}

Check Pin Header to BNC Low Passed Through
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Digital Output    ${bbb_output_pin}    ${DIGITAL_LOW}
    Enable Line Drivers
    Enable Level Shifters
    Specify BBB Digital Input     ${bbb_input_pin}
    Execute BNC Card Test via BBB
    ${pin_output} =       Get BBB Input Value    ${bbb_input_pin}
    Should Be Equal       ${pin_output[0]}    ${DIGITAL_LOW}

Set IO Expander Pin to Output
    [Arguments]    ${i2c_pin_name}
    ${configure_io_expander_output_i2c} =   Get I2C To Configure IO Expander IOs    ${i2c_pin_name}
    Specify BBB I2C Output Dict    ${configure_io_expander_output_i2c}

Set Veto Out To Driven Mode
    ${veto_out_driven_mode_i2c_data} =    Get I2C for Driven Mode    ${I2C_BNC4_VETO_OUT_OC}
    Specify BBB I2C Output Dict    ${veto_out_driven_mode_i2c_data}
    Set IO Expander Pin to Output    ${I2C_BNC4_VETO_OUT_OC}

Set Veto Out To Open Drain Mode
    ${veto_out_open_drain_mode_i2c_data} =    Get I2C for Open Drain Mode    ${I2C_BNC4_VETO_OUT_OC}
    Specify BBB I2C Output Dict    ${veto_out_open_drain_mode_i2c_data}
    Set IO Expander Pin to Output    ${I2C_BNC4_VETO_OUT_OC}

Specify User IO Output Mode
    [Arguments]    ${i2c_user_io_nin_out}
    ${configure_user_io_output} =    Get I2C for User IO Output Mode    ${i2c_user_io_nin_out}
    Specify BBB I2C Output Dict    ${configure_user_io_output}
    Set IO Expander Pin to Output    ${i2c_user_io_nin_out}

Specify User IO Input Mode
    [Arguments]    ${i2c_user_io_nin_out}
    ${configure_user_io_input} =    Get I2C for User IO Input Mode    ${i2c_user_io_nin_out}
    Specify BBB I2C Output Dict    ${configure_user_io_input}
    Set IO Expander Pin to Output    ${i2c_user_io_nin_out}

Check User IO Pin Header To BNC High Negated
    [Arguments]   ${i2c_user_io_nin_out}    ${bbb_output}    ${bbb_input}
    Specify User IO Output Mode    ${i2c_user_io_nin_out}
    Check Pin Header to BNC High Negated     ${bbb_output}    ${bbb_input}

Check User IO Pin Header To BNC Low Negated
    [Arguments]   ${i2c_user_io_nin_out}    ${bbb_output}    ${bbb_input}
    Specify User IO Output Mode    ${i2c_user_io_nin_out}
    Check Pin Header to BNC Low Negated     ${bbb_output}    ${bbb_input}

Check Termination Resistor Can Be Enabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}
    Enable Termination Resistor    ${pin_i2c_name}
    Specify BBB Digital Output    ${bnc_pin_number}    ${DIGITAL_HIGH}
    Enable Level Shifters
    Specify BBB Analog Input     ${bnc_analog_pin_number}
    Execute BNC Card Test via BBB
    ${analog_output} =    Get BBB Input Value    ${bnc_analog_pin_number}
    Should Have Termination Resistance Enabled    ${analog_output[0]}

Enable Termination Resistor
    [Arguments]    ${pin_i2c_name}
    ${i2c_data} =    Get I2C To Enable Termination Resistor    ${pin_i2c_name}
    Specify BBB I2C Output Dict    ${i2c_data}
    Set IO Expander Pin to Output    ${pin_i2c_name}

Check Termination Resistor Is Default Disabled
    [Arguments]    ${bnc_pin_number}    ${bnc_analog_pin_number}
    Log    Termination resistors should be disabled by default
    Specify BBB Digital Output    ${bnc_pin_number}    ${DIGITAL_HIGH}
    Enable Level Shifters
    Specify BBB Analog Input     ${bnc_analog_pin_number}
    Execute BNC Card Test via BBB
    ${analog_output} =    Get BBB Input Value    ${bnc_analog_pin_number}
    Should Have Termination Resistance Disabled    ${analog_output[0]}

Check Termination Resistor Can Be Force Disabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}
    Force Disable Termination Resistor    ${pin_i2c_name}
    Specify BBB Digital Output    ${bnc_pin_number}    ${DIGITAL_HIGH}
    Enable Level Shifters
    Specify BBB Analog Input     ${bnc_analog_pin_number}
    Execute BNC Card Test via BBB
    ${analog_output} =    Get BBB Input Value    ${bnc_analog_pin_number}
    Should Have Termination Resistance Disabled    ${analog_output[0]}

Force Disable Termination Resistor
    [Arguments]    ${pin_i2c_name}
    ${i2c_data} =    Get I2C To Disable Termination Resistor    ${pin_i2c_name}
    Specify BBB I2C Output Dict    ${i2c_data}
    Set IO Expander Pin to Output    ${pin_i2c_name}

Should Have Termination Resistance Enabled
    [Arguments]    ${analog_value}
    Should Be True    ${analog_value} < ${TERMINATION_RESISTOR_ENABLED_ANALOG_MAXIMUM}

Should Have Termination Resistance Disabled
    [Arguments]    ${analog_value}
    Should Be True    ${TERMINATION_RESISTOR_DISABLED_ANALOG_MINIMUM} < ${analog_value}
    Should Be True    ${analog_value} < ${TERMINATION_RESISTOR_DISABLED_ANALOG_MAXIMUM}

Check User IO Termination Resistor Can Be Enabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}
    Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Check Termination Resistor Can Be Enabled
    ...    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}

Check User IO Termination Resistor Is Default Disabled
    [Arguments]    ${bnc_pin_number}    ${bnc_analog_pin_number}
    Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Check Termination Resistor Is Default Disabled
    ...    ${bnc_pin_number}    ${bnc_analog_pin_number}

Check User IO Termination Resistor Can Be Force Disabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}
    [Documentation]    Termination resistors should be disabled by default.
    ...    But this keyword drives termination resistor IO expander pin low and "forces" it to be disabled
    Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Check Termination Resistor Can Be Force Disabled
    ...    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}
