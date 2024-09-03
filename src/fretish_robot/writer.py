# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import pathlib

from robot.model import SuiteVisitor
from robot.running.model import Keyword, TestCase, TestSuite


def write_testsuite(testsuite: TestSuite, root_output_dir: str):
    root_output_folder = pathlib.Path(root_output_dir)
    root_output_folder.mkdir(parents=True, exist_ok=True)
    with open(root_output_folder / "tests.robot", "w") as r:
        testsuite.visit(RobotRSTPrinter(r))


class RobotRSTPrinter(SuiteVisitor):

    def __init__(self, writable):
        self._writable = writable

        self.indent = 0

    def start_suite(self, suite: TestSuite) -> bool | None:
        self._print_indented("*** Settings ***")

        self._print_indented(f"Name    {suite.name}")

        for meta_key, meta_value in suite.metadata.items():
            self._print_indented(f"Metadata    {meta_key}    {meta_value}")

        for imp in suite.resource.imports:
            self._print_indented(f"Library    {imp.name}")

        self._print_newline()
        self._print_indented("*** Test Cases ***")

        return True

    def start_test(self, test: TestCase) -> bool | None:
        self._print_indented(test.name)

        self.indent += 1

        tagline = "    ".join(["[Tags]"] + list(test.tags))
        self._print_indented(tagline)

        return True

    def end_test(self, test: TestCase) -> bool | None:
        self.indent -= 1
        self._print_newline()
        return True

    def start_keyword(self, keyword: Keyword) -> bool | None:
        self._print_indented(str(keyword))
        return True

    def _print_indented(self, line: str):
        self.__print(f"{'    ' * self.indent}{line}")

    def _print_newline(self):
        self.__print("")

    def __print(self, line: str):
        print(line, file=self._writable)
