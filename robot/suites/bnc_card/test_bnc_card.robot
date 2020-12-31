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

*** Test Cases ***

# Tag: PIN_HEADER_OUT_EQUALS_BNC_IN
# Tests that when a digital signal is input to a specified BNC connector, the
# same signal is output on the appropriate pin header

Check BNC1 REF_IN Input = Pin Header REF_IN For Digital High
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC1_REF_IN_BNC}      ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${REF_IN_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${REF_IN_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check BNC1 REF_IN Input = Pin Header REF_IN For Digital Low
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC1_REF_IN_BNC}      ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${REF_IN_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${REF_IN_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital High
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC6_SYNC_IN_BNC}      ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${SYNC_IN_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${SYNC_IN_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check BNC6 SYNC_IN Input = Pin Header SYNC_IN For Digital Low
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC6_SYNC_IN_BNC}      ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${SYNC_IN_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${SYNC_IN_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check BNC7 USER1 IO Input = Pin Header USER1 IO For Digital High With I2C Input Mode
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC7_USER1_IO_BNC}      ${DIGITAL}    ${DIGITAL_HIGH}
    ${user1_io_i2c_data} =    Get I2C For IO Mode     ${USER1_IO_I2C_NAME}    ${INPUT_MODE}
    Specify BBB I2C Output    1    ${user1_io_i2c_data}
    Specify BBB Input     ${USER1_IO_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${USER1_IO_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check BNC7 USER1 IO Input = Pin Header USER1 IO For Digital Low With I2C Input Mode
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC7_USER1_IO_BNC}      ${DIGITAL}    ${DIGITAL_LOW}
    ${user1_io_i2c_data} =    Get I2C For IO Mode     ${USER1_IO_I2C_NAME}    ${INPUT_MODE}
    Specify BBB I2C Output    1    ${user1_io_i2c_data}
    Specify BBB Input     ${USER1_IO_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${USER1_IO_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check BNC8 USER2 IO Input = Pin Header USER2 IO For Digital High With I2C Input Mode
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC8_USER2_IO_BNC}      ${DIGITAL}    ${DIGITAL_HIGH}
    ${user2_io_i2c_data} =    Get I2C For IO Mode     ${USER2_IO_I2C_NAME}    ${INPUT_MODE}
    Specify BBB I2C Output    1    ${user2_io_i2c_data}
    Specify BBB Input     ${USER2_IO_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${USER2_IO_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check BNC8 USER2 IO Input = Pin Header USER2 IO For Digital Low With I2C Input Mode
    [Tags]     PIN_HEADER_OUT_EQUALS_BNC_IN
    Specify BBB Output    ${BNC8_USER2_IO_BNC}      ${DIGITAL}    ${DIGITAL_LOW}
    ${user2_io_i2c_data} =    Get I2C For IO Mode     ${USER2_IO_I2C_NAME}    ${INPUT_MODE}
    Specify BBB I2C Output    1    ${user2_io_i2c_data}
    Specify BBB Input     ${USER2_IO_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${USER2_IO_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

# Tag: BNC_OUT_EQUALS_PIN_HEADER_IN
# Tests that when a digital signal is input to a specified pin hedaer, the same
# signal is output on the appropriate BNC connector

Check Pin Header REF_OUT Input = BNC2 REF_OUT Output For Digital High
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${REF_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${BNC2_REF_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC2_REF_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check Pin Header REF_OUT Input = BNC2 REF_OUT Output For Digital Low
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${REF_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${BNC2_REF_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC2_REF_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check Pin Header TDC_OUT Input = BNC3 TDC_OUT Output For Digital High
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${REF_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${BNC3_TDC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC3_TDC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check Pin Header TDC_OUT Input = BNC3 TDC_OUT Output For Digital Low
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${TDC_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${BNC3_TDC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC3_TDC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check Pin Header VETO_OUT Input = BNC4 VETO_OUT Output For Digital High With I2C Driven Mode
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${VETO_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_HIGH}
    ${veto_out_i2c_data} =    Get I2C For IO Mode     ${VETO_OUT_I2C_MODE}    ${DRIVEN_MODE}
    Specify BBB I2C Output    1    ${veto_out_i2c_data}
    Specify BBB Input     ${BNC4_VETO_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC4_VETO_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check Pin Header VETO_OUT Input = BNC4 VETO_OUT Output For Digital Low With I2C Driven Mode
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${VETO_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_LOW}
    ${veto_out_i2c_data} =    Get I2C For IO Mode     ${VETO_OUT_I2C_MODE}    ${DRIVEN_MODE}
    Specify BBB I2C Output    1    ${veto_out_i2c_data}
    Specify BBB Input     ${BNC4_VETO_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC4_VETO_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital High
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${SYNC_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${BNC5_SYNC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC5_SYNC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital Low
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${SYNC_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${BNC5_SYNC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC5_SYNC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check Pin Header USER1_IO Input = BNC7 USER1_IO Output For Digital High With I2C Output Mode
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${SYNC_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_HIGH}
    ${user1_io_i2c_data} =    Get I2C For IO Mode     ${USER1_IO_I2C_NAME}    ${OUTPUT_MODE}
    Specify BBB I2C Output    1    ${user1_io_i2c_data}
    Specify BBB Input     ${BNC5_SYNC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC5_SYNC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check Pin Header USER1_IO Input = BNC7 USER1_IO Output For Digital Low With I2C Output Mode
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${SYNC_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_LOW}
    ${user1_io_i2c_data} =    Get I2C For IO Mode     ${USER1_IO_I2C_NAME}    ${OUTPUT_MODE}
    Specify BBB I2C Output    1    ${user1_io_i2c_data}
    Specify BBB Input     ${BNC5_SYNC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC5_SYNC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital High With I2C Output Mode
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${SYNC_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_HIGH}
    ${user2_io_i2c_data} =    Get I2C For IO Mode     ${USER2_IO_I2C_NAME}    ${OUTPUT_MODE}
    Specify BBB I2C Output    1    ${user2_io_i2c_data}
    Specify BBB Input     ${BNC5_SYNC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC5_SYNC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check Pin Header SYNC_OUT Input = BNC5 SYNC_OUT Output For Digital Low With I2C Output Mode
    [Tags]     BNC_OUT_EQUALS_PIN_HEADER_IN
    Specify BBB Output    ${SYNC_OUT_PIN_HEADER}    ${DIGITAL}    ${DIGITAL_LOW}
    ${user2_io_i2c_data} =    Get I2C For IO Mode     ${USER2_IO_I2C_NAME}    ${OUTPUT_MODE}
    Specify BBB I2C Output    1    ${user2_io_i2c_data}
    Specify BBB Input     ${BNC5_SYNC_OUT_BNC}      ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get BBB Input Value    ${result}    ${BNC5_SYNC_OUT_BNC}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}


*** Keywords ***
Setup BBB For BNC Card Tests
    # TODO: Add detailed manual instructions for setting up tests
    Manual Instruction    add setup instructions here

    # set up a socket connection to BBB
    Connect To BBB
