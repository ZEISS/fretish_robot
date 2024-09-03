# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Library    fretish_robot.FRETLib
Library    fretish_robot.example_user_lib.ExampleUserLib

*** Test Cases ***
TEST_REQ-124
    [Tags]    REQID=REQ-124
    In test mode
    Upon    request_to_set_two
    After    100 milliseconds    Satisfy    when $get_random_bool then ($get_true and ($result == 2))

*** Test Cases ***
TEST_REQ-124-2
    [Tags]    REQID=REQ-124-2
    In test mode
    Upon    request_to_set_two
    Immediately    Satisfy    ($result == 2)

*** Test Cases ***
TEST_REQ-124-3
    [Tags]    REQID=REQ-124-3
    In test mode
    Upon    request_to_set_two
    At The Next Timepoint    Satisfy    ($result == 2)
