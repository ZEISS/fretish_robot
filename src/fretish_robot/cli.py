# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import argparse

from fretish_robot.generate_robot import generate_robot_suite_from_fret
from fretish_robot.requirements import load_fret_requirements
from fretish_robot.writer import write_testsuite


def get_cli_arguments():
    parser = argparse.ArgumentParser(
        description="Process exported FRET JSON requirements files and generate proper Robot Framework `.robot` files "
        "depicting the requirements."
    )

    parser.add_argument(
        "--extra-libraries",
        nargs="+",
        default=[],
        help="Additional libraries to include in .robot files at the top",
    )

    parser.add_argument(
        "--robot-output-folder",
        default="./robot_files",
        help="Output folder for generated Robot Framework file(s) (default: ./robot_files)",
    )

    parser.add_argument(
        "fret_json_input_filepath",
        help="Input filepath for FRET JSON requirement file",
    )

    args = parser.parse_args()

    return args


def main():
    args = get_cli_arguments()

    fret_requirements = load_fret_requirements(args.fret_json_input_filepath)
    fret_requirements = sorted(fret_requirements, key=lambda r: r.req_id)
    suite = generate_robot_suite_from_fret(fret_requirements, args.extra_libraries)

    write_testsuite(suite, args.robot_output_folder)


if __name__ == "__main__":
    main()
