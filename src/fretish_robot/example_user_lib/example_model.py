# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import enum


class Modes(enum.Enum):
    UNKNOWN = enum.auto()
    TEST = enum.auto()
    SECOND = enum.auto()


class ExampleModel:
    def __init__(self) -> None:
        self.mode = Modes.UNKNOWN
        self.number = 0

    def reset(self):
        self.__init__()

    def set_test_mode(self):
        self.mode = Modes.TEST

    def set_second_mode(self):
        self.mode = Modes.SECOND

    def set(self, param: int):
        self.number = param

    def get(self):
        return self.number
