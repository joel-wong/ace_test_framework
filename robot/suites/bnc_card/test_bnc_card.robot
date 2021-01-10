*** Settings ***
Documentation    Test Suite for the SKF G5 BNC Card

Library      Collections
Library      Dialogs

Variables    bbbio/BBB_IO_CONSTANTS.py
Library      bbbio/bbb_io_manager.py

Library      bnc_card_test_utils.py
Variables    BNC_CONFIG.py

Suite Setup    Setup BBB For BNC Card Tests
Test Setup     Reset BBB IO Specifications

Test Teardown     Set BNC Card and BeagleBone IOs Back to Inputs
Suite Teardown    Disconnect From BBB

*** Variables ***
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

${VETO_OUT_DEFAULT_DRIVEN_MESSAGE}    Veto out should be in driven mode by default
${USER_IO_DEFAULT_INPUT_MESSAGE}    User IOs should be in input mode by default

*** Test Cases ***

Check BNC1 REF_IN Input = Pin Header REF_IN For Digital High
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check Digital High Passed Through    ${B_REF_IN_L3V3}    ${P_REF_IN_L3V3}

Check BNC1 REF_IN Input = Pin Header REF_IN For Digital Low
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check Digital Low Passed Through    ${B_REF_IN_L3V3}    ${P_REF_IN_L3V3}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital High
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check Digital High Passed Through    ${B_SYNC_IN_L3V3}    ${P_SYNC_IN_L3V3}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital Low
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check Digital Low Passed Through    ${B_SYNC_IN_L3V3}    ${P_SYNC_IN_L3V3}


Check BNC8 USER1 IO Input = Pin Header USER1 IO For Digital High With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check BNC User IO Digital High Passed Through    ${B_USER1_L3V3}    ${P_USER1_IN_L3V3}

Check BNC8 USER1 IO Input = Pin Header USER1 IO For Digital Low With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check BNC User IO Digital Low Passed Through    ${B_USER1_L3V3}    ${P_USER1_IN_L3V3}

Check BNC7 USER2 IO Input = Pin Header USER2 IO For Digital High With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check BNC User IO Digital High Passed Through    ${B_USER2_L3V3}    ${P_USER2_IN_L3V3}

Check BNC7 USER2 IO Input = Pin Header USER2 IO For Digital Low With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}    ${USER_IO_DEFAULT_INPUT}
    Log    ${USER_IO_DEFAULT_INPUT_MESSAGE}
    Check BNC User IO Digital Low Passed Through    ${B_USER2_L3V3}    ${P_USER2_IN_L3V3}



Check Pin Header REF_OUT Input is Negated on BNC2 REF_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Digital High Negated    ${P_REF_OUT_L3V3}    ${B_REF_OUT_L3V3}

Check Pin Header REF_OUT Input is Negated on BNC2 REF_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Digital Low Negated    ${P_REF_OUT_L3V3}    ${B_REF_OUT_L3V3}

Check Pin Header TDC_OUT Input is Negated on BNC3 TDC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Digital High Negated    ${P_TDC_OUT_L3V3}    ${B_TDC_OUT_L3V3}

Check Pin Header TDC_OUT Input is Negated on BNC3 TDC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Digital Low Negated    ${P_TDC_OUT_L3V3}    ${B_TDC_OUT_L3V3}

Check Pin Header VETO_OUT Input is Negated on BNC4 VETO_OUT Output For Digital High With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Log    ${VETO_OUT_DEFAULT_DRIVEN_MESSAGE}
    Check Digital High Negated    ${P_VETO_OUT_L3V3}    ${B_VETO_OUT_L3V3}

Check Pin Header VETO_OUT Input is Negated on BNC4 VETO_OUT Output For Digital Low With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Log    ${VETO_OUT_DEFAULT_DRIVEN_MESSAGE}
    Check Digital Low Negated    ${P_VETO_OUT_L3V3}    ${B_VETO_OUT_L3V3}

Check Pin Header SYNC_OUT Input is Negated on BNC5 SYNC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Digital High Negated    ${P_SYNC_OUT_L3V3}    ${B_SYNC_OUT_L3V3}

Check Pin Header SYNC_OUT Input is Negated on BNC5 SYNC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Digital Low Negated    ${P_SYNC_OUT_L3V3}    ${B_SYNC_OUT_L3V3}

Check Pin Header USER1_IO Input is Negated on BNC8 USER1_IO Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header User IO Digital High Negated
    ...    ${I2C_BNC8_USER1_NIN_OUT}    ${P_USER1_OUT_L3V3}    ${B_USER1_L3V3}

Check Pin Header USER1_IO Input is Negated on BNC8 USER1_IO Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header User IO Digital Low Negated
    ...    ${I2C_BNC8_USER1_NIN_OUT}    ${P_USER1_OUT_L3V3}    ${B_USER1_L3V3}

Check Pin Header USER2_IO Input is Negated on BNC7 USER2_IO Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header User IO Digital High Negated
    ...    ${I2C_BNC7_USER2_NIN_OUT}    ${P_USER2_OUT_L3V3}    ${B_USER2_L3V3}

Check Pin Header USER2_IO Input is Negated on BNC7 USER2_IO Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_NEGATED_PIN_HEADER_IN}
    Check Pin Header User IO Digital Low Negated
    ...    ${I2C_BNC7_USER2_NIN_OUT}    ${P_USER2_OUT_L3V3}    ${B_USER2_L3V3}



Check BNC1 REF_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled
    ...    ${I2C_BNC1_500HM_EN}    ${B_REF_IN_L3V3}    ${TR_REF_IN_L1V8}    ${SW_REF_IN_L3V3}

Check BNC1 REF_IN Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled
    ...    ${I2C_BNC1_500HM_EN}    ${B_REF_IN_L3V3}    ${TR_REF_IN_L1V8}    ${SW_REF_IN_L3V3}

Check BNC6 SYNC_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled
    ...    ${I2C_BNC6_500HM_EN}    ${B_SYNC_IN_L3V3}    ${TR_SYNC_IN_L1V8}    ${SW_SYNC_IN_L3V3}

Check BNC6 SYNC_IN Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled
    ...    ${I2C_BNC6_500HM_EN}    ${B_SYNC_IN_L3V3}    ${TR_SYNC_IN_L1V8}    ${SW_SYNC_IN_L3V3}

Check BNC8 USER1_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled
    ...    ${I2C_BNC8_500_HM_EN}    ${B_USER1_L3V3}    ${TR_USER1_L1V8}    ${SW_USER1_IN_L3V3}

Check BNC8 USER1_IO Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled
    ...    ${I2C_BNC8_500_HM_EN}    ${B_USER1_L3V3}    ${TR_USER1_L1V8}    ${SW_USER1_IN_L3V3}

Check BNC7 USER2_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled
    ...    ${I2C_BNC7_500_HM_EN}    ${B_USER2_L3V3}    ${TR_USER2_L1V8}    ${SW_USER2_IN_L3V3}

Check BNC7 USER2_IO Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled
    ...    ${I2C_BNC7_500_HM_EN}    ${B_USER2_L3V3}    ${TR_USER2_L1V8}    ${SW_USER2_IN_L3V3}



Check Pin Header VETO_OUT High Input has Low Output on BNC4 VETO_OUT With Open Drain Mode
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Veto Out To Open Drain Mode
    Specify BBB Output    ${P_VETO_OUT_L3V3}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${B_VETO_OUT_L3V3}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${B_VETO_OUT_L3V3}
    Log                   A digital high input with open drain mode should drive a low output
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check Pin Header VETO_OUT Low Input has High Impedence Output on BNC4 VETO_OUT With Open Drain Mode
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Veto Out To Open Drain Mode
    Specify BBB Output    ${P_VETO_OUT_L3V3}    ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${B_VETO_OUT_L3V3}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${B_VETO_OUT_L3V3}
    Log                   A digital low input with open drain mode should have a high impedence output
    Log                   Due to a pull up resistor, this should result in a digital high output
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}



Check Green LED
    [Tags]    ${LED_CHECK}
    Specify BBB Output    ${P_TDC_LED_L3V3}    ${DIGITAL}    ${DIGITAL_LOW}
    Send IO Specifications to BBB
    Execute Manual Step    Press PASS if the LED on the BNC card is green, otherwise press FAIL

Check Orange LED
    [Tags]    ${LED_CHECK}
    Set IO Expander Pin to Output    ${I2C_RLED}
    ${turn_red_led_on_i2c} =    Get I2C to Turn on LED    ${I2C_RLED}
    Specify BBB I2C Output Dict    2    ${turn_red_led_on_i2c}
    Send IO Specifications to BBB
    Execute Manual Step    Press PASS if the LED on the BNC card is orange, otherwise press FAIL



*** Keywords ***
Setup BBB For BNC Card Tests
    # TODO: Add detailed manual instructions for setting up tests
    Execute Manual Step    During development, remove all external circuitry from the BeagleBone. Press PASS when complete.

    # set up a socket connection to BBB
    Connect To BBB

Set BNC Card and BeagleBone IOs Back to Inputs
    Reset BBB IO Specifications
    ${all_input_i2c} =    Get I2C to Set All IO Expander IOs As Inputs
    Specify BBB I2C Output Dict    1    ${all_input_i2c}
    Send IO Specifications to BBB
    Log     BeagleBone IOs are automatically set to inputs when receiving an IO Specification

Set Pin Mode Via I2C
    [Arguments]    ${i2c_pin_name}    ${pin_mode}
    ${i2c_data} =    Get I2C For IO Mode     ${i2c_pin_name}    ${INPUT_MODE}
    Specify BBB I2C Output Dict    1    ${i2c_data}

Check Digital High Passed Through
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Output    ${bbb_output_pin}      ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${bbb_input_pin}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${bbb_input_pin}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check Digital Low Passed Through
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Output    ${bbb_output_pin}      ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${bbb_input_pin}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${bbb_input_pin}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check BNC User IO Digital High Passed Through
    [Arguments]    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}
    Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Check Digital High Passed Through    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}

Check BNC User IO Digital Low Passed Through
    [Arguments]    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}
    Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Check Digital Low Passed Through    ${bbb_user_io_output_pin}    ${bbb_user_io_input_pin}

Set User IO Level Shifter to Shift from 3.3 to 5 Volts
    Specify BBB Output    ${DIR_L3}    ${DIGITAL}    ${DIGITAL_HIGH}

Set User IO Level Shifter to Shift from 5 to 3.3 Volts
    Specify BBB Output    ${DIR_L3}    ${DIGITAL}    ${DIGITAL_LOW}

Check Digital High Negated
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Output    ${bbb_output_pin}      ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${bbb_input_pin}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${bbb_input_pin}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check Digital Low Negated
    [Arguments]    ${bbb_output_pin}    ${bbb_input_pin}
    Specify BBB Output    ${bbb_output_pin}      ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${bbb_input_pin}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${bbb_input_pin}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Set IO Expander Pin to Output
    [Arguments]    ${i2c_pin_name}
    ${configure_io_expander_output_i2c} =   Get I2C To Configure IO Expander IOs    ${i2c_pin_name}
    Specify BBB I2C Output Dict    1    ${configure_io_expander_output_i2c}

Set Veto Out To Open Drain Mode
    Set IO Expander Pin to Output    ${I2C_BNC4_VETO_OUT_OC}
    ${veto_out_driven_mode_i2c_data} =    Get I2C for Open Drain Mode    ${I2C_BNC4_VETO_OUT_OC}
    Specify BBB I2C Output Dict    1    ${veto_out_driven_mode_i2c_data}

Specify User IO Output Mode
    [Arguments]    ${i2c_user_io_nin_out}
    Set IO Expander Pin to Output    ${i2c_user_io_nin_out}
    ${configure_user_io_output} =    Get I2C for User IO Output Mode    ${i2c_user_io_nin_out}
    Specify BBB I2C Output Dict    2    ${configure_user_io_output}

Check Pin Header User IO Digital High Negated
    [Arguments]   ${i2c_user_io_nin_out}    ${bbb_output}    ${bbb_input}
    Set User IO Level Shifter to Shift from 5 to 3.3 Volts
    Specify User IO Output Mode    ${i2c_user_io_nin_out}
    Check Digital High Negated     ${bbb_output}    ${bbb_input}

Check Pin Header User IO Digital Low Negated
    [Arguments]   ${i2c_user_io_nin_out}    ${bbb_output}    ${bbb_input}
    Set User IO Level Shifter to Shift from 5 to 3.3 Volts
    Specify User IO Output Mode    ${i2c_user_io_nin_out}
    Check Digital Low Negated     ${bbb_output}    ${bbb_input}

Check Termination Resistor Can Be Enabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}    ${term_resistor_circuit_switch}
    Enable Termination Resistor    ${pin_i2c_name}
    Specify BBB Output    ${bnc_pin_number}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Output    ${term_resistor_circuit_switch}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${bnc_analog_pin_number}    ${ANALOG}
    ${result} =           Send IO Specifications To BBB
    ${analog_output} =    Get BBB Input Value    ${result}    ${bnc_analog_pin_number}
    Should Have Termination Resistance Enabled    ${analog_output}

Enable Termination Resistor
    [Arguments]    ${pin_i2c_name}
    ${configure_io_expander_output_i2c} =   Get I2C To Configure IO Expander IOs    ${pin_i2c_name}
    Specify BBB I2C Output Dict    1    ${configure_io_expander_output_i2c}
    ${i2c_data} =    Get I2C To Enable Termination Resistor    ${pin_i2c_name}
    Specify BBB I2C Output Dict    2    ${i2c_data}

Check Termination Resistor Can Be Disabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}    ${term_resistor_circuit_switch}
    Log    Termination resistors should be disabled by default
    Specify BBB Output    ${bnc_pin_number}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Output    ${term_resistor_circuit_switch}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${bnc_analog_pin_number}    ${ANALOG}
    ${result} =           Send IO Specifications To BBB
    ${analog_output} =    Get BBB Input Value    ${result}    ${bnc_analog_pin_number}
    Should Have Termination Resistance Disabled    ${analog_output}

Should Have Termination Resistance Enabled
    [Arguments]    ${analog_value}
    Should Be True    ${TERMINATION_RESISTOR_ENABLED_ANALOG_MINIMUM} < ${analog_value}
    Should Be True    ${analog_value} < ${TERMINATION_RESISTOR_ENABLED_ANALOG_MAXIMUM}

Should Have Termination Resistance Disabled
    [Arguments]    ${analog_value}
    Should Be True    ${TERMINATION_RESISTOR_DISABLED_ANALOG_MINIMUM} < ${analog_value}
    Should Be True    ${analog_value} < ${TERMINATION_RESISTOR_DISABLED_ANALOG_MAXIMUM}
