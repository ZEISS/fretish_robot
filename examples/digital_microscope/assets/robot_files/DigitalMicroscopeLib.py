# SPDX-FileCopyrightText: Copyright (c) 2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0


from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn

ZEPHYR_LIB_NAME = "twister_harness.robot_framework.ZephyrLibrary"

FAIL_INDICATORS = ["Usage:", "command not found", "Unknown", "Failed:", "Denied:"]


@library(scope="SUITE", listener="SELF")
class DigitalMicroscopeLib:
    def __init__(self):
        self._requests = []
        self._responses = []

        self._builtin = BuiltIn()

    def _start_suite(self, testsuite, result):
        self._builtin.import_library(ZEPHYR_LIB_NAME)
        self._lib = self._builtin.get_library_instance(ZEPHYR_LIB_NAME)

        self._builtin.run_keyword("Get a device")
        self._builtin.run_keyword("Run device")

    def _start_test(self, testcase, result):
        self._exec("system reset")

        self._requests.clear()
        self._responses.clear()

    def _end_suite(self, testsuite, result):
        self._builtin.run_keyword("Close device")

    @keyword("In ${mode_name} mode")
    def in_mode_name_mode(self, mode_name):
        self._exec(f"mode set {mode_name}", check_command=True)

    @keyword("request_move_${dir}")
    def request_move_dir(self, dir):
        self._exec(f"tube move {dir}", check_command=True)

    @keyword
    def tube_moving_upwards(self):
        res = self._exec("tube move get dir", check_command=True)
        return self._search_for_response("Tube is moving upwards", res)

    @keyword
    def tube_moving_downwards(self):
        res = self._exec("tube move get dir", check_command=True)
        return self._search_for_response("Tube is moving downwards", res)

    @keyword("tube_upper_end")
    def tube_upper_end(self):
        res = self._exec("tube position is_upper")
        return self._search_for_response("Tube is in the upper position", res)

    @keyword("tube_bottom_end")
    def tube_bottom_end(self):
        res = self._exec("tube position is_bottom")
        return self._search_for_response("Tube is in the bottom position", res)

    @keyword("request_illuminate_${onoff}")
    def request_illuminate_onoff(self, onoff):
        self._exec(f"illumination active {onoff}", check_command=True)

    @keyword
    def illumination_on(self):
        res = self._exec("illumination active get")
        return self._search_for_response("Illumination is on", res)

    @keyword
    def request_brightness_increase(self):
        self._exec("illumination value increase", check_command=True)

    @keyword
    def configured_brightness(self):
        res = self._exec("illumination value get configured", check_command=True)
        if not self._search_for_response("Configured illumination value", res):
            return False
        value = self._extract_brightness_value(res)
        return value

    @keyword
    def actual_brightness(self):
        res = self._exec("illumination value get actual", check_command=True)
        if not self._search_for_response("Actual illumination value", res):
            return False
        value = self._extract_brightness_value(res)
        return value

    @keyword
    def max_brightness(self):
        res = self._exec("illumination value get max", check_command=True)
        if not self._search_for_response("Maximum illumination value", res):
            return False
        value = self._extract_brightness_value(res)
        return value

    def _extract_brightness_value(self, res: list[str]) -> int:
        content_line = res[1]
        if not self._search_for_response("illumination value:", [content_line]):
            raise AssertionError("The response lines are not correct")
        value = int(content_line.split(":")[1].strip())
        return value

    @keyword
    def configured_brightness_increased_by_10_percent(self):
        configured = self.configured_brightness()
        actual = self.actual_brightness()
        return actual * 11 == configured * 10

    @keyword
    def request_change_objective(self):
        self._exec("objective change")

    @keyword
    def objective_lense_changed_clockwise_ok(self):
        res = self._exec("objective get")
        if not self._search_for_response("Current objective", res):
            return False
        cur_value = int(res[1].split(":")[1].strip())
        res = self._exec("objective history")
        if not self._search_for_response("Previous objectives", res):
            return False
        prev_value = int(res[1].split(":")[1].strip().split()[0])

        return (cur_value - prev_value) % 5 == 1

    @keyword
    def answer_request_ok(self):
        error = self._check_last_command_success()
        return error is None

    @keyword
    def answer_request_denied(self):
        error = self._check_last_command_success()
        # Special case for our example
        if error is not None and "Denied" in error:
            return True

        return False

    def _exec(self, command: str, check_command: bool = False) -> list[str]:
        self._requests.append(command)
        command_responses = self._builtin.run_keyword("Run command", command)
        self._responses.append(command_responses)
        if check_command:
            error = self._check_last_command_success()
            if error is not None:
                assert (
                    False
                ), f"'{command}' not executed successfully, response was {error}"
        return command_responses

    def _check_last_command_success(self) -> str | None:
        last_response_lines = self._responses[-1]
        for fail_indicator in FAIL_INDICATORS:
            for response_line in last_response_lines:
                if fail_indicator in response_line:
                    return response_line

        return None

    def _search_for_response(self, term: str, responses: list[str]):
        for response in responses:
            if term in response:
                return True

        return False
