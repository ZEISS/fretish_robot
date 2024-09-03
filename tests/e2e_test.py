# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import pathlib
import subprocess

import pytest
import robot


@pytest.fixture
def testfile_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "testfiles"


def test__run_fret_to_robot_cli__given_file__correct_robot_output(
    testfile_dir, tmp_path
):
    subprocess.check_call(
        [
            "fret-to-robot",
            testfile_dir / "fret_requirements.json",
            "--extra-libraries",
            "fretish_robot.example_user_lib.ExampleUserLib",
            "--robot-output-folder",
            tmp_path,
        ]
    )

    with open(tmp_path / "tests.robot") as rf:
        result = rf.read().strip()

    with open(testfile_dir / "expected_result.robot") as ef:
        expected_result = ef.read().strip()

    assert result == expected_result


def test__run_robot__on_testfile_exp_output__passes_properly(testfile_dir):
    res = robot.run_cli([testfile_dir / "expected_result.robot"], exit=False)

    assert res == 0


def test__run_robot__on_executable_file__passes_properly(testfile_dir):
    res = robot.run_cli([testfile_dir / "executable_robotfile.robot"], exit=False)

    assert res == 0
