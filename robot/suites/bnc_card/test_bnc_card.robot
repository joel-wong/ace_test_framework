*** Settings ***
Documentation    Test Suite for the SKF G5 BNC Card

Library     Collections

Library      ../../shared/lib/bbbio/bbb_io_manager.py
Library      ../../shared/lib/manual/manual_step.py
Variables    ../../shared/lib/bbbio/BBB_IO_CONSTANTS.py

Library     bnc_card_test_utils.py
Variables   BNC_CONFIG.py

Suite Setup    Setup BBB For BNC Card Tests
Test Setup     Reset BBB IO Specifications

Suite Teardown    Disconnect From BBB

*** Test Cases ***
Check BNC REF_IN Input = Pin Header REF_IN For Digital High
    Specify BBB Output    ${BNC1_REFERENCE_IN_BNC}    ${DIGITAL}    ${DIGITAL_HIGH}
    Specify BBB Input     ${BNC1_REFERENCE_IN_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get From Dictionary    ${result["inputs"]}    ${BNC1_REFERENCE_IN_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_HIGH}

Check BNC REF_IN Input = Pin Header REF_IN For Digital Low
    Specify BBB Output    ${BNC1_REFERENCE_IN_BNC}    ${DIGITAL}    ${DIGITAL_LOW}
    Specify BBB Input     ${BNC1_REFERENCE_IN_PIN_HEADER}    ${DIGITAL}
    ${result} =           Send IO Specifications To BBB
    ${pin_output} =       Get From Dictionary    ${result["inputs"]}    ${BNC1_REFERENCE_IN_PIN_HEADER}
    Should Be Equal       ${pin_output}    ${DIGITAL_LOW}

#  TODO: add more test cases

*** Keywords ***
Setup BBB For BNC Card Tests
    # TODO: Add detailed manual instructions for setting up tests
    Manual Instruction    add setup instructions here

    # automatically setup a socket connection to BBB
    Connect To BBB
