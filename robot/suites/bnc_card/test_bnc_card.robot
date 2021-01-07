*** Settings ***
Documentation    Test Suite for the SKF G5 BNC Card

Library      Collections

Library      ../../shared/lib/bbbio/bbb_io_manager.py
Library      ../../shared/lib/manual/manual_step.py
Variables    ../../shared/lib/bbbio/BBB_IO_CONSTANTS.py

Library      bnc_card_test_utils.py
Variables    BNC_CONFIG.py

Suite Setup    Setup BBB For BNC Card Tests
Test Setup     Reset BBB IO Specifications

Suite Teardown    Disconnect From BBB

*** Variables ***
${PIN_HEADER_OUT_EQUALS_BNC_IN}    PIN_HEADER_OUT_EQUALS_BNC_IN
# Tag: PIN_HEADER_OUT_EQUALS_BNC_IN
# Tests that when a digital signal is input to a specified BNC connector, the
# same signal is output on the appropriate pin header

${BNC_OUT_EQUALS_PIN_HEADER_IN}    BNC_OUT_EQUALS_PIN_HEADER_IN
# Tag: BNC_OUT_EQUALS_PIN_HEADER_IN
# Tests that when a digital signal is input to a specified pin hedaer, the same
# signal is output on the appropriate BNC connector

${TERMINATION_RESISTOR_CHECK}      TERMINATION_RESISTOR_CHECK
# Tag: TERMINATION_RESISTOR_CHECK
# Tests that the terminiation resistor can be enabled and disabled for a
# specified BNC connector

${OPEN_DRAIN_FUNCTIONALITY_CHECK}    OPEN_DRAIN_FUNCTIONALITY_CHECK
# Tag: OPEN_DRAIN_FUNCTIONALITY_CHECK
# Tests that the open drain mode is enabled when set via I2C input

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

Check BNC7 USER1 IO Input = Pin Header USER1 IO For Digital High With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${I2C_BNC8_USER1_NIN_OUT}    ${INPUT_MODE}
    Check Digital High Passed Through    ${B_USER1_L3V3}    ${USER1_IO_PIN_HEADER}

Check BNC7 USER1 IO Input = Pin Header USER1 IO For Digital Low With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${I2C_BNC8_USER1_NIN_OUT}    ${INPUT_MODE}
    Check Digital Low Passed Through    ${B_USER1_L3V3}    ${USER1_IO_PIN_HEADER}

Check BNC8 USER2 IO Input = Pin Header USER2 IO For Digital High With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${BNC7_USER2_NIN_OUT}    ${INPUT_MODE}
    Check Digital High Passed Through    ${B_USER2_L3V3}    ${USER2_IO_PIN_HEADER}

Check BNC8 USER2 IO Input = Pin Header USER2 IO For Digital Low With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${BNC7_USER2_NIN_OUT}    ${INPUT_MODE}
    Check Digital Low Passed Through    ${B_USER2_L3V3}    ${USER2_IO_PIN_HEADER}



Check Pin Header REF_OUT Input = BNC2 REF_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital High Passed Through    ${P_REF_OUT_L3V3}    ${B_REF_OUT_L3V3}

Check Pin Header REF_OUT Input = BNC2 REF_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital Low Passed Through    ${P_REF_OUT_L3V3}    ${B_REF_OUT_L3V3}

Check Pin Header TDC_OUT Input = BNC3 TDC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital High Passed Through    ${P_TDC_OUT_L3V3}    ${B_TDC_OUT_L3V3}

Check Pin Header TDC_OUT Input = BNC3 TDC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital Low Passed Through    ${P_TDC_OUT_L3V3}    ${B_TDC_OUT_L3V3}

Check Pin Header VETO_OUT Input = BNC4 VETO_OUT Output For Digital High With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${I2C_BNC4_VETO_OUT_OC}    ${DRIVEN_MODE}
    Check Digital High Passed Through    ${P_VETO_OUT_L3V3}    ${B_VETO_OUT_L3V3}

Check Pin Header VETO_OUT Input = BNC4 VETO_OUT Output For Digital Low With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${I2C_BNC4_VETO_OUT_OC}    ${DRIVEN_MODE}
    Check Digital Low Passed Through    ${P_VETO_OUT_L3V3}    ${B_VETO_OUT_L3V3}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital High Passed Through    ${P_SYNC_OUT_L3V3}    ${B_SYNC_OUT_L3V3}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital Low Passed Through    ${P_SYNC_OUT_L3V3}    ${B_SYNC_OUT_L3V3}

Check Pin Header USER1_IO Input = BNC7 USER1_IO Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${I2C_BNC8_USER1_NIN_OUT}    ${OUTPUT_MODE}
    Check Digital High Passed Through    ${USER1_IO_PIN_HEADER}    ${B_USER1_L3V3}

Check Pin Header USER1_IO Input = BNC7 USER1_IO Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${I2C_BNC8_USER1_NIN_OUT}    ${OUTPUT_MODE}
    Check Digital Low Passed Through    ${USER1_IO_PIN_HEADER}    ${B_USER1_L3V3}

Check Pin Header USER2_IO Input = BNC8 USER2_IO Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${BNC7_USER2_NIN_OUT}    ${OUTPUT_MODE}
    Check Digital High Passed Through    ${USER2_IO_PIN_HEADER}    ${B_USER2_L3V3}

Check Pin Header USER2_IO Input = BNC8 USER2_IO Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${BNC7_USER2_NIN_OUT}    ${OUTPUT_MODE}
    Check Digital Low Passed Through    ${USER2_IO_PIN_HEADER}    ${B_USER2_L3V3}



Check BNC1 REF_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled    ${I2C_BNC1_500HM_EN}    ${B_REF_IN_L3V3}    ${TR_REF_IN_1V8}

Check BNC1 REF_IN Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled    ${I2C_BNC1_500HM_EN}    ${B_REF_IN_L3V3}    ${TR_REF_IN_1V8}

Check BNC6 SYNC_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled    ${I2C_BNC6_500HM_EN}    ${B_SYNC_IN_L3V3}    ${TR_SYNC_IN_L1V8}

Check BNC6 SYNC_IN Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled    ${I2C_BNC6_500HM_EN}    ${B_SYNC_IN_L3V3}    ${TR_SYNC_IN_L1V8}

Check BNC7 USER1_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${I2C_BNC8_USER1_NIN_OUT}    ${INPUT_MODE}
    Check Termination Resistor Can Be Enabled    ${I2C_BNC8_USER1_NIN_OUT}    ${B_USER1_L3V3}    ${TR_USER1_L1V8}

Check BNC7 USER1_IO Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${I2C_BNC8_USER1_NIN_OUT}    ${INPUT_MODE}
    Check Termination Resistor Can Be Disabled    ${I2C_BNC8_USER1_NIN_OUT}    ${B_USER1_L3V3}    ${TR_USER1_L1V8}

Check BNC8 USER2_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${BNC7_USER2_NIN_OUT}    ${INPUT_MODE}
    Check Termination Resistor Can Be Enabled    ${BNC7_USER2_NIN_OUT}    ${B_USER2_L3V3}    ${TR_USER2_L1V8}

Check BNC8 USER2_IO Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${BNC7_USER2_NIN_OUT}    ${INPUT_MODE}
    Check Termination Resistor Can Be Disabled    ${BNC7_USER2_NIN_OUT}    ${B_USER2_L3V3}    ${TR_USER2_L1V8}


Check BNC4 VETO_OUT Digital High Passed Through
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Pin Mode Via I2C    ${I2C_BNC4_VETO_OUT_OC}    ${OPEN_DRAIN_MODE}
    Check Digital High Passed Through    ${P_VETO_OUT_L3V3}    ${B_VETO_OUT_L3V3}

Check BNC4 VETO_OUT Digital Low Passed Through
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Pin Mode Via I2C    ${I2C_BNC4_VETO_OUT_OC}    ${OPEN_DRAIN_MODE}
    Check Digital Low Passed Through    ${P_VETO_OUT_L3V3}    ${B_VETO_OUT_L3V3}

Check BNC4 VETO_OUT High Impedance Input Has Digital High Output
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Pin Mode Via I2C    ${I2C_BNC4_VETO_OUT_OC}    ${OPEN_DRAIN_MODE}
    Specify BBB Input     ${P_VETO_OUT_L3V3}    ${DIGITAL}
    Specify BBB Input     ${B_VETO_OUT_L3V3}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${B_VETO_OUT_L3V3}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}



*** Keywords ***
Setup BBB For BNC Card Tests
    # TODO: Add detailed manual instructions for setting up tests
    Manual Instruction    add setup instructions here

    # set up a socket connection to BBB
    Connect To BBB

Set Pin Mode Via I2C
    [Arguments]    ${i2c_pin_name}    ${pin_mode}
    ${i2c_data} =    Get I2C For IO Mode     ${i2c_pin_name}    ${INPUT_MODE}
    Specify BBB I2C Output    1    ${i2c_data}

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

Check Termination Resistor Can Be Enabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}
    Enable Termination Resistor    ${pin_i2c_name}
    Specify BBB Output    ${bnc_pin_number}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${bnc_analog_pin_number}    ${ANALOG}
    ${result} =           Send IO Specifications To BBB
    ${analog_output} =    Get BBB Input Value    ${result}    ${bnc_analog_pin_number}
    Should Have Termination Resistance Enabled    ${analog_output}

Enable Termination Resistor
    [Arguments]    ${pin_i2c_name}
    ${i2c_data} =    Get I2C To Enable Termination Resistor    ${pin_i2c_name}
    Specify BBB I2C Output    2    ${i2c_data}

Check Termination Resistor Can Be Disabled
    [Arguments]    ${pin_i2c_name}    ${bnc_pin_number}    ${bnc_analog_pin_number}
    Disable Termination Resistor    ${pin_i2c_name}
    Specify BBB Output    ${bnc_pin_number}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${bnc_analog_pin_number}    ${ANALOG}
    ${result} =           Send IO Specifications To BBB
    ${analog_output} =    Get BBB Input Value    ${result}    ${bnc_analog_pin_number}
    Should Have Termination Resistance Disabled    ${analog_output}

Disable Termination Resistor
    [Arguments]    ${pin_i2c_name}
    ${i2c_data} =    Get I2C To Disable Termination Resistor    ${pin_i2c_name}
    Specify BBB I2C Output    2    ${i2c_data}

Should Have Termination Resistance Enabled
    [Arguments]    ${analog_value}
    Should Be True    ${analog_value} < ${ANALOG_LOW_MAXIMUM}

Should Have Termination Resistance Disabled
    [Arguments]    ${analog_value}
    Should Be True    ${analog_value} > ${ANALOG_HIGH_MINIMUM}
