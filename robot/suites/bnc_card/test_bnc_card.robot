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
    Check Digital High Passed Through    ${BNC1_REF_IN_BNC}    ${REF_IN_PIN_HEADER}

Check BNC1 REF_IN Input = Pin Header REF_IN For Digital Low
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check Digital Low Passed Through    ${BNC1_REF_IN_BNC}    ${REF_IN_PIN_HEADER}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital High
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check Digital High Passed Through    ${BNC6_SYNC_IN_BNC}    ${SYNC_IN_PIN_HEADER}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital Low
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Check Digital Low Passed Through    ${BNC6_SYNC_IN_BNC}    ${SYNC_IN_PIN_HEADER}

Check BNC7 USER1 IO Input = Pin Header USER1 IO For Digital High With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${USER1_IO_I2C_NAME}    ${INPUT_MODE}
    Check Digital High Passed Through    ${BNC7_USER1_IO_BNC}    ${USER1_IO_PIN_HEADER}

Check BNC7 USER1 IO Input = Pin Header USER1 IO For Digital Low With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${USER1_IO_I2C_NAME}    ${INPUT_MODE}
    Check Digital Low Passed Through    ${BNC7_USER1_IO_BNC}    ${USER1_IO_PIN_HEADER}

Check BNC8 USER2 IO Input = Pin Header USER2 IO For Digital High With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${USER2_IO_I2C_NAME}    ${INPUT_MODE}
    Check Digital High Passed Through    ${BNC8_USER2_IO_BNC}    ${USER2_IO_PIN_HEADER}

Check BNC8 USER2 IO Input = Pin Header USER2 IO For Digital Low With I2C Input Mode
    [Tags]     ${PIN_HEADER_OUT_EQUALS_BNC_IN}
    Set Pin Mode Via I2C    ${USER2_IO_I2C_NAME}    ${INPUT_MODE}
    Check Digital Low Passed Through    ${BNC8_USER2_IO_BNC}    ${USER2_IO_PIN_HEADER}



Check Pin Header REF_OUT Input = BNC2 REF_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital High Passed Through    ${REF_OUT_PIN_HEADER}    ${BNC2_REF_OUT_BNC}

Check Pin Header REF_OUT Input = BNC2 REF_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital Low Passed Through    ${REF_OUT_PIN_HEADER}    ${BNC2_REF_OUT_BNC}

Check Pin Header TDC_OUT Input = BNC3 TDC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital High Passed Through    ${TDC_OUT_PIN_HEADER}    ${BNC3_TDC_OUT_BNC}

Check Pin Header TDC_OUT Input = BNC3 TDC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital Low Passed Through    ${TDC_OUT_PIN_HEADER}    ${BNC3_TDC_OUT_BNC}

Check Pin Header VETO_OUT Input = BNC4 VETO_OUT Output For Digital High With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${VETO_OUT_I2C_NAME}    ${DRIVEN_MODE}
    Check Digital High Passed Through    ${VETO_OUT_PIN_HEADER}    ${BNC4_VETO_OUT_BNC}

Check Pin Header VETO_OUT Input = BNC4 VETO_OUT Output For Digital Low With I2C Driven Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${VETO_OUT_I2C_NAME}    ${DRIVEN_MODE}
    Check Digital Low Passed Through    ${VETO_OUT_PIN_HEADER}    ${BNC4_VETO_OUT_BNC}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital High
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital High Passed Through    ${SYNC_OUT_PIN_HEADER}    ${BNC5_SYNC_OUT_BNC}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital Low
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Check Digital Low Passed Through    ${SYNC_OUT_PIN_HEADER}    ${BNC5_SYNC_OUT_BNC}

Check Pin Header USER1_IO Input = BNC7 USER1_IO Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${USER1_IO_I2C_NAME}    ${OUTPUT_MODE}
    Check Digital High Passed Through    ${USER1_IO_PIN_HEADER}    ${BNC7_USER1_IO_BNC}

Check Pin Header USER1_IO Input = BNC7 USER1_IO Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${USER1_IO_I2C_NAME}    ${OUTPUT_MODE}
    Check Digital Low Passed Through    ${USER1_IO_PIN_HEADER}    ${BNC7_USER1_IO_BNC}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital High With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${USER2_IO_I2C_NAME}    ${OUTPUT_MODE}
    Check Digital High Passed Through    ${USER2_IO_PIN_HEADER}    ${BNC8_USER2_IO_BNC}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital Low With I2C Output Mode
    [Tags]     ${BNC_OUT_EQUALS_PIN_HEADER_IN}
    Set Pin Mode Via I2C    ${USER2_IO_I2C_NAME}    ${OUTPUT_MODE}
    Check Digital Low Passed Through    ${USER2_IO_PIN_HEADER}    ${BNC8_USER2_IO_BNC}



Check BNC1 REF_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled    ${REF_IN_I2C_NAME}    ${BNC1_REF_IN_BNC}    ${BNC1_REF_IN_ANALOG_PIN}

Check BNC1 REF_IN Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled    ${REF_IN_I2C_NAME}    ${BNC1_REF_IN_BNC}    ${BNC1_REF_IN_ANALOG_PIN}

Check BNC6 SYNC_IN Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Enabled    ${SYNC_IN_I2C_NAME}    ${BNC6_SYNC_IN_BNC}    ${BNC6_SYNC_IN_ANALOG_PIN}

Check BNC6 SYNC_IN Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Check Termination Resistor Can Be Disabled    ${SYNC_IN_I2C_NAME}    ${BNC6_SYNC_IN_BNC}    ${BNC6_SYNC_IN_ANALOG_PIN}

Check BNC7 USER1_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${USER1_IO_I2C_NAME}    ${INPUT_MODE}
    Check Termination Resistor Can Be Enabled    ${USER1_IO_I2C_NAME}    ${BNC7_USER1_IO_BNC}    ${BNC7_USER1_IO_ANALOG_PIN}

Check BNC7 USER1_IO Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${USER1_IO_I2C_NAME}    ${INPUT_MODE}
    Check Termination Resistor Can Be Disabled    ${USER1_IO_I2C_NAME}    ${BNC7_USER1_IO_BNC}    ${BNC7_USER1_IO_ANALOG_PIN}

Check BNC8 USER2_IO Termination Resistor Can Be Enabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${USER2_IO_I2C_NAME}    ${INPUT_MODE}
    Check Termination Resistor Can Be Enabled    ${USER2_IO_I2C_NAME}    ${BNC8_USER2_IO_BNC}    ${BNC8_USER2_IO_ANALOG_PIN}

Check BNC8 USER2_IO Termination Resistor Can Be Disabled
    [Tags]    ${TERMINATION_RESISTOR_CHECK}
    Set Pin Mode Via I2C    ${USER2_IO_I2C_NAME}    ${INPUT_MODE}
    Check Termination Resistor Can Be Disabled    ${USER2_IO_I2C_NAME}    ${BNC8_USER2_IO_BNC}    ${BNC8_USER2_IO_ANALOG_PIN}


Check BNC4 VETO_OUT Digital High Passed Through
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Pin Mode Via I2C    ${VETO_OUT_I2C_NAME}    ${OPEN_DRAIN_MODE}
    Check Digital High Passed Through    ${VETO_OUT_PIN_HEADER}    ${BNC4_VETO_OUT_BNC}

Check BNC4 VETO_OUT Digital Low Passed Through with Digital High
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Pin Mode Via I2C    ${VETO_OUT_I2C_NAME}    ${OPEN_DRAIN_MODE}
    Check Digital Low Passed Through    ${VETO_OUT_PIN_HEADER}    ${BNC4_VETO_OUT_BNC}

Check BNC4 VETO_OUT High Impedance Input Has Digital High Output
    [Tags]    ${OPEN_DRAIN_FUNCTIONALITY_CHECK}
    Set Pin Mode Via I2C    ${VETO_OUT_I2C_NAME}    ${OPEN_DRAIN_MODE}
    Specify BBB Input     ${VETO_OUT_PIN_HEADER}    ${DIGITAL}
    Specify BBB Input     ${BNC4_VETO_OUT_BNC}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC4_VETO_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}



*** Keywords ***
Setup BBB For BNC Card Tests
    # TODO: Add detailed manual instructions for setting up tests
    Manual Instruction    add setup instructions here

    # set up a socket connection to BBB
    Connect To BBB

Set Pin Mode Via I2C
    [Arguments]    ${i2c_pin_name}    ${pin_mode}
    ${i2c_data} =    Get I2C For IO Mode     ${USER1_IO_I2C_NAME}    ${INPUT_MODE}
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
    [Arguments]    ${PIN_I2C_NAME}    ${BNC_PIN_NUMBER}    ${BNC_ANALOG_PIN_NUMBER}
    ${i2c_data} =    Get I2C For Termination Resistor     ${PIN_I2C_NAME}    ${TRUE}
    Specify BBB I2C Output    2    ${i2c_data}
    Specify BBB Output    ${BNC_PIN_NUMBER}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${BNC_ANALOG_PIN_NUMBER}    ${ANALOG}
    ${result} =           Send IO Specifications To BBB
    ${analog_output} =    Get BBB Input Value    ${result}    ${BNC_ANALOG_PIN_NUMBER}
    Should Have Termination Resistance Enabled    ${analog_output}

Check Termination Resistor Can Be Disabled
    [Arguments]    ${PIN_I2C_NAME}    ${BNC_PIN_NUMBER}    ${BNC_ANALOG_PIN_NUMBER}
    ${i2c_data} =    Get I2C For Termination Resistor     ${PIN_I2C_NAME}    ${FALSE}
    Specify BBB I2C Output    2    ${i2c_data}
    Specify BBB Output    ${BNC_PIN_NUMBER}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${BNC_ANALOG_PIN_NUMBER}    ${ANALOG}
    ${result} =           Send IO Specifications To BBB
    ${analog_output} =    Get BBB Input Value    ${result}    ${BNC_ANALOG_PIN_NUMBER}
    Should Have Termination Resistance Disabled    ${analog_output}

Should Have Termination Resistance Enabled
    [Arguments]    ${analog_value}
    Should Be True    ${analog_value} < ${ANALOG_LOW_MAXIMUM}

Should Have Termination Resistance Disabled
    [Arguments]    ${analog_value}
    Should Be True    ${analog_value} > ${ANALOG_HIGH_MINIMUM}
