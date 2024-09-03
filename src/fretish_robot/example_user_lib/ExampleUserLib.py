# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import random

from fretish_robot.example_user_lib.example_model import ExampleModel


class ExampleUserLib:

    def __init__(self):
        # This makes this library also a visitor, allowing reactions on test start, ...
        self.ROBOT_LIBRARY_LISTENER = self

        self.model = ExampleModel()

    # Prefix visitor methods with _underscore, so they don't become keywords by accident
    def _start_test(self, data, result):
        self.model.reset()

    def in_test_mode(self):
        self.model.set_test_mode()

    def in_second_mode(self):
        self.model.set_second_mode()

    def request_to_set_one(self):
        self.model.set(1)

    def request_to_set_two(self):
        self.model.set(2)

    def result(self):
        return self.model.get()

    @staticmethod
    def get_random_bool():
        return random.random() < 0.5

    @staticmethod
    def get_true():
        return True
