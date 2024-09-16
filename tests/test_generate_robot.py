# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import pytest

from fretish_robot.generate_robot import _extract_events, _prefix_vars, _to_python_expr

TEST_EXPR = "a != 1 & b = 1 | c = 4 ^ 3 - 1 & b = 2 | d <= a"
EXPECTED_PYTHON = "a != 1 and b == 1 or c == 4 ** 3 - 1 and b == 2 or d <= a"
EXPECTED_PREFIXED = "$a != 1 and $b == 1 or $c == 4 ** 3 - 1 and $b == 2 or $d <= $a"


def test__to_python_expr__all_python_fretish_diffs__all_translated__all_():
    result = _to_python_expr(TEST_EXPR)

    assert result == EXPECTED_PYTHON


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("(d <= 2)", "(d <= 2)"),
        ("(d != 2)", "(d != 2)"),
        ("! (d == 2)", "not (d == 2)"),
        ("(d ^ 2)", "(d ** 2)"),
        ("(d & 2==2)", "(d and 2==2)"),
        ("(d | 2==2)", "(d or 2==2)"),
        ("(d | 2 = 2)", "(d or 2 == 2)"),
    ],
)
def test__to_python_expr__python_correctly_translated(expr, expected):
    result = _to_python_expr(expr)

    assert result == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("(d <= 2)", "($d <= 2)"),
        ("(d)", "($d)"),
        ("( d)", "( $d)"),
        ("(d )", "($d )"),
        ("!(d )", "!($d )"),
        ("d <= 2 and d >= 4", "$d <= 2 and $d >= 4"),
    ],
)
def test__prefix_vars__expression_different_positions_suffixes__properly_replaced(
    expr, expected
):
    result = _prefix_vars(expr, ["d"])

    assert result == expected


@pytest.mark.parametrize(
    "expr",
    [
        "(no_d <= 2)",
        "(nod <= 2)",
        "(da <= 2)",
        "(d_a <= 2)",
        "(a != 2)",
    ],
)
def test__prefix_vars__expression_with_suffixes__not_replaced(expr):
    result = _prefix_vars(expr, ["d"])

    assert result == expr


def test__prefix_vars__string_with_multiple_vars__all_prefixed():
    result = _prefix_vars(EXPECTED_PYTHON, ["a", "b", "c", "d"])

    assert result == EXPECTED_PREFIXED


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("a", [("a", "a")]),
        ("(( a | b) |c_d)", [("a", "a"), ("b", "b"), ("c_d", "c_d")]),
    ],
)
def test___extract_events__different_inputes__correctly_extracted(expr, expected):
    result = _extract_events(expr)

    assert result == expected
