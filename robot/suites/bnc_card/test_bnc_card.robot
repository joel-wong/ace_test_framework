*** Settings ***
Documentation    Test Suite for the SKF G5 BNC Card

Library    bnc_card_test_utils.py


*** Test Cases ***
# Placeholder test cases. TODO: add actual test cases later
Test Pure Robot
    Should Be Equal    ${TRUE}    ${TRUE}


Test Python Function
    ${python_result} =     Return Python True
    Should Be Equal        ${TRUE}    ${python_result}
    Sleep                  10s
