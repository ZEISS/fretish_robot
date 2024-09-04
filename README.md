# FRET support for Robot files

This package provides the framework and capabilities to run [FRET requirements](https://github.com/NASA-SW-VnV/fret)
in [Robot Framework](https://robotframework.org/).

This package provides, on the one hand, a script `fret-to-robot` to convert parsed FRET JSON files into Robot
Framework `.robot` files together with an example implementation for events specified in requirements.
Hereby, a few new keywords are used to keep the requirement transformation readable and understandable, to
enable proper reviews and traceability.

On the other hand, a Robot Framework library ``FRETLib`` is implemented that breaks down these requirements
into built-in Robot Framework keywords, to maintain semantic but also reduce maintenance work.

## Installation

Install the package and requirements via

```sh
pip install -e .
```

## Usage

### Script

To convert a parsed FRET JSON into Robot test files and the generated keyword calls, call

```sh
fret-to-robot <path_to_fret.json>
```

This will generate a file ``tests.robot`` in the `robot_files` folder.

For configuration options, like the path to the file, output, or additional libraries to include,
use the ``--help`` option.

### FRETLib

The ``FRETLib`` keywords can be used by importing the library:

```robot
Library    fretish_robot.FRETLib
```

**Note**: This is already done by ``fret-to-robot``.

### Requirement behavior implementation

The ``FretLib`` library transforms FRET keywords into standard
Robot Framework keywords. All non-FRET keywords of the Robot files must be
provided by a user library, see [the example library implementation](src/fretish_robot/example_user_lib/).

E.g., while `fret-to-robot` outputs

```robot
Upon    request_set_two,
Satisfies  ($answer_message_good & $answer_is_two)
```

, the library provides `Upon` and `Satisfies`, but not things like
`request_set_two`, `answer_message_good` and `answer_is_two`.
A user library must provide a keyword implementation for these.

This can be done in two steps:

* Implement a Robot Framework library with proper keywords. An example can be seen in
`fretish_robot.example_user_lib.ExampleUserLib`.
* Pass --extra-libraries with the proper path, e.g. ``--extra-libraries  fretish_robot.example_user_lib.ExampleUserLib``
  when generating, so it is part of the `.robot` files.

**Note**: It is not necessary to adjust the robot execution then, if all libraries are installed.

### Executing generated Robot files

To run the generated files, just do

```sh
robot ./robot_files/result.robot
```

## Limitations

There are some implementation details and restrictions to consider when using:

* Only 'if then' and pure expressions are supported in the 'Satisfy' clause.
* Formatting of printed requirements is fine, but not pretty. This could be improved in newer versions if needed.
