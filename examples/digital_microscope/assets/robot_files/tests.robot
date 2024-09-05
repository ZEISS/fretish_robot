# SPDX-FileCopyrightText: Copyright 2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Name    Generated FRET Testsuite
Library    fretish_robot.FRETLib

*** Test Cases ***
TEST_REQ-01-01-1
    [Tags]    REQID=REQ-01-01    SCOPE=normal    TRIGGER=request_move_up
    In normal mode
    Upon    request_move_up
    Within    200 millisecond    Satisfy    when (not $tube_upper_end) then ($tube_moving_upwards and $answer_request_ok)

TEST_REQ-01-01-2
    [Tags]    REQID=REQ-01-01    SCOPE=homing    TRIGGER=request_move_up
    In homing mode
    Upon    request_move_up
    Within    200 millisecond    Satisfy    when (not $tube_upper_end) then ($tube_moving_upwards and $answer_request_ok)

TEST_REQ-01-02-1
    [Tags]    REQID=REQ-01-02    SCOPE=always    TRIGGER=tube_moving_upwards & tube_at_upper_end
    Upon    tube_moving_upwards & tube_at_upper_end
    At the next timepoint    Satisfy    $tube_position_hold

TEST_REQ-01-03-1
    [Tags]    REQID=REQ-01-03    SCOPE=always    TRIGGER=tube_moving_downwards & tube_at_bottom_end
    Upon    tube_moving_downwards & tube_at_bottom_end
    At the next timepoint    Satisfy    $tube_position_hold

TEST_REQ-01-04-1
    [Tags]    REQID=REQ-01-04    SCOPE=normal    TRIGGER=request_move_down
    In normal mode
    Upon    request_move_down
    Within    200 millisecond    Satisfy    when (not $tube_bottom_end) then ($tube_moving_downwards and $answer_request_ok)

TEST_REQ-01-04-2
    [Tags]    REQID=REQ-01-04    SCOPE=homing    TRIGGER=request_move_down
    In homing mode
    Upon    request_move_down
    Within    200 millisecond    Satisfy    when (not $tube_bottom_end) then ($tube_moving_downwards and $answer_request_ok)

TEST_REQ-01-05-1
    [Tags]    REQID=REQ-01-05    SCOPE=always    TRIGGER=always
    FAIL    timing requirement 'always' not implemented

TEST_REQ-02-01-1
    [Tags]    REQID=REQ-02-01    SCOPE=sample_prep    TRIGGER=request_illuminate_on
    In sample_prep mode
    Upon    request_illuminate_on
    Within    200 millisecond    Satisfy    (($illumination_on and ($actual_brightness == $configured_brightness)) and $answer_request_ok)

TEST_REQ-02-01-2
    [Tags]    REQID=REQ-02-01    SCOPE=capture    TRIGGER=request_illuminate_on
    In capture mode
    Upon    request_illuminate_on
    Within    200 millisecond    Satisfy    (($illumination_on and ($actual_brightness == $configured_brightness)) and $answer_request_ok)

TEST_REQ-02-02-1
    [Tags]    REQID=REQ-02-02    SCOPE=always    TRIGGER=always
    FAIL    timing requirement 'always' not implemented

TEST_REQ-02-03-1
    [Tags]    REQID=REQ-02-03    SCOPE=sample_prep    TRIGGER=request_brightness_increase
    In sample_prep mode
    Upon    request_brightness_increase
    Within    200 milliseconds    Satisfy    when ($illumination_on and (not ($actual_brightness == $max_brightness))) then ($configured_brightness_increased_by_10_percent and $answer_request_ok)

TEST_REQ-02-03-2
    [Tags]    REQID=REQ-02-03    SCOPE=capture    TRIGGER=request_brightness_increase
    In capture mode
    Upon    request_brightness_increase
    Within    200 milliseconds    Satisfy    when ($illumination_on and (not ($actual_brightness == $max_brightness))) then ($configured_brightness_increased_by_10_percent and $answer_request_ok)

TEST_REQ-03-01-1
    [Tags]    REQID=REQ-03-01    SCOPE=sample_prep    TRIGGER=request_change_objective
    In sample_prep mode
    Upon    request_change_objective
    Within    1 second    Satisfy    ($objective_lense_changed_clockwise_ok and $answer_request_ok)

TEST_REQ-03-01-2
    [Tags]    REQID=REQ-03-01    SCOPE=capture    TRIGGER=request_change_objective
    In capture mode
    Upon    request_change_objective
    Within    1 second    Satisfy    ($objective_lense_changed_clockwise_ok and $answer_request_ok)

TEST_REQ-03-02-1
    [Tags]    REQID=REQ-03-02    SCOPE=tube_moving    TRIGGER=request_change_objective
    In tube_moving mode
    Upon    request_change_objective
    Within    100 milliseconds    Satisfy    $answer_request_denied

