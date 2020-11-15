*** Settings ***
Documentation    A suite of tests for the SKF G5 BNC Card


Library    bnc_card_test_utils.py


*** Test Cases ***
Test Pure Robot
    Should Be Equal    ${TRUE}    ${TRUE}


Test Python Function
    ${python_result} =     Return Python True
    Should Be Equal    ${TRUE}    ${python_result}
