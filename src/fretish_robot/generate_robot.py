# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import dataclasses
import itertools
import logging
import pathlib
import re

from robot.running.model import Body, Keyword, TestCase, TestSuite

from fretish_robot.requirements import FRETRequirement

logger = logging.getLogger(__name__)


def _get_testsuite():
    suite = TestSuite(f"Generated FRET Testsuite")
    return suite


def _add_libs(suite: TestSuite, extra_libs: list[str]):

    for lib in ["fretish_robot.FRETLib"] + extra_libs:
        suite.resource.imports.library(lib)


def _to_python_expr(expr: str) -> str:

    # normal replacement
    for cur, new in [
        (" ^ ", " ** "),
        (" & ", " and "),
        (" | ", " or "),
        (" = ", " == "),
    ]:
        expr = expr.replace(cur, new)

    # regex replacement
    for cur, new in [
        (r"!(?!=)", r"not "),  # replace '!', but not '!='
    ]:
        expr = re.sub(cur, new, expr)

    return expr


def _prefix_vars(expr: str, variables: list[str]) -> str:

    variable_find_expression = f"({'|'.join(variables)})"

    match_expr_unexpanding = rf"(?<![^\W]){variable_find_expression}(?![^\W])"

    expr_with_vars = re.sub(match_expr_unexpanding, r"$\1", expr)

    return expr_with_vars


TAG = str


def _extract_scope_modes(fret_req: FRETRequirement) -> list[tuple[str | None, TAG]]:

    scope_mode = fret_req.scope_mode
    if scope_mode != None:
        if scope_mode.startswith('"(') and scope_mode.endswith(')"'):
            result = []
            different_modes = scope_mode[2:-2].split("|")
            for mode in different_modes:
                scope_expr = fret_req.scope.replace(scope_mode, mode)
                result.append((scope_expr, mode))

            return result

        else:
            return [(fret_req.scope, scope_mode)]
    else:
        return [(None, "always")]


def _extract_events(fret_req: FRETRequirement) -> list[tuple[str | None, TAG]]:

    event = fret_req.trigger_event
    if event != None:
        if event.startswith("(") and event.endswith(")"):
            result = []
            different_events = event[1:-1].split("|")
            for diff_event in different_events:
                diff_event = diff_event.strip()
                result.append((diff_event, diff_event))
            return result
        else:
            return [(event, event)]
        ...

    else:
        return [(None, "always")]


def _construct_taglist(req_id: str, mode: str, event: str) -> list[tuple[str, str]]:
    tags = [("REQID", req_id), ("SCOPE", mode), ("TRIGGER", event)]

    return tags


def _add_single_test(suite: TestSuite, fret_req: FRETRequirement) -> None:

    req_id = fret_req.req_id
    extracted_scopes = _extract_scope_modes(fret_req)
    extracted_events = _extract_events(fret_req)

    test_number = 0

    for scope, scope_tag in extracted_scopes:
        for event, event_tag in extracted_events:

            test_number += 1

            tags = _construct_taglist(req_id, scope_tag, event_tag)

            test: TestCase = suite.tests.create(
                f"TEST_{req_id}-{test_number}", tags=[f"{k}={v}" for k, v in tags]
            )
            body: Body = test.body

            if scope:
                body.create_keyword(scope)

            if event:
                body.create_keyword("Upon", args=[event])

            condition = fret_req.condition_to_check
            condition = _to_python_expr(condition)
            condition = _prefix_vars(condition, fret_req.variables)

            if " -> " in condition:
                antecedent, consequence = condition[1:-1].split(" -> ")
                satisfiable = Keyword(
                    "Satisfy", args=[f"when {antecedent} then {consequence}"]
                )
            else:
                satisfiable = Keyword("Satisfy", args=[condition])

            timing = fret_req.timing.lower()
            if timing.startswith("within") or timing.startswith("after"):
                word, timing_cond = timing.split(" ", maxsplit=1)

                body.create_keyword(word.capitalize(), args=[timing_cond, satisfiable])
            elif timing in ["immediately", "at the next timepoint"]:
                body.create_keyword(timing.capitalize(), args=[satisfiable])
            else:
                logger.warning(
                    f"{req_id} has timing requirement {timing}, not implemented!"
                )
                body.create_keyword(
                    "FAIL", args=[f"timing requirement '{timing}' not implemented"]
                )


def _add_tests_from_requirements(
    suite: TestSuite, fret_requirements: list[FRETRequirement]
) -> None:

    for fret_req in fret_requirements:
        _add_single_test(suite, fret_req)


def generate_robot_suite_from_fret(
    fret_requirements: list[FRETRequirement], extra_libs: list[str]
) -> TestSuite:

    suite = _get_testsuite()

    _add_libs(suite, extra_libs)
    _add_tests_from_requirements(suite, fret_requirements)

    return suite
