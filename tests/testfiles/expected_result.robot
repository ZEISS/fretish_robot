# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Name    Generated FRET Testsuite
Library    fretish_robot.FRETLib
Library    fretish_robot.example_user_lib.ExampleUserLib

*** Test Cases ***
TEST_REQ-123-1
    [Tags]    REQID=REQ-123    SCOPE=test    TRIGGER=request_to_set_two
    In test mode
    Upon    request_to_set_two
    Within    100 milliseconds    Satisfy    when $get_random_bool then ($get_true and ($result == 2))

TEST_REQ-125-1
    [Tags]    REQID=REQ-125    SCOPE=test    TRIGGER=request_to_set_two
    In test mode
    Upon    request_to_set_two
    Within    100 milliseconds    Satisfy    when $get_random_bool then ($get_true and ($result == 2))

TEST_REQ-125-2
    [Tags]    REQID=REQ-125    SCOPE=second    TRIGGER=request_to_set_two
    In second mode
    Upon    request_to_set_two
    Within    100 milliseconds    Satisfy    when $get_random_bool then ($get_true and ($result == 2))

TEST_REQ-126-1
    [Tags]    REQID=REQ-126    SCOPE=test    TRIGGER=request_to_set_one
    In test mode
    Upon    request_to_set_one
    Within    100 milliseconds    Satisfy    ((1 <= $result) and ($result <= 2))

TEST_REQ-126-2
    [Tags]    REQID=REQ-126    SCOPE=test    TRIGGER=request_to_set_two
    In test mode
    Upon    request_to_set_two
    Within    100 milliseconds    Satisfy    ((1 <= $result) and ($result <= 2))
