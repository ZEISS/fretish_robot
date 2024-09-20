# FRETish robot examples

This folder contains some examples to demonstrate the use of `fret-to-robot`.

## Preparation

You should be familiar with Zephyr and the basic setup as described in the
[Getting Started Guide](https://docs.zephyrproject.org/latest/develop/getting_started/index.html).

For a setup in an example, create a virtual environment, source it, and install `west` (Steps 1 to 5)
in the Getting Started Guide.

Now, also install the `fretish_robot` library. If you are in the current directory, do
this by calling

```
pip install ../
```

Then, create a new workspace for the example by calling (e.g. for digital_microscope)

```sh
west init -l digital_microscope
west update
```

This also fetches a Zephyr with (currently custom) `robotframework` harness support for Twister, and all
necessary modules.

## Creating tests for example

To create Robot Framework tests for an example, move into the `assets` folder of the example and call
`fret-to-robot` properly. For example:

```sh
fret-to-robot req_fret.json --extra-libraries DigitalMicroscopeLib
```

The `extra-libraries` argument is necessary as we implement keyword functionality in a library
called `DigitalMicroscopeLib` (see `assets/robot_files/DigitalMicroscopeLib.py`).

Now, the generated files can be found in `assets/robot_files/tests.robot`.

## Execute tests

Now, you can execute the tests with a proper Twister execution.

To execute all tests for `native_sim_64` platform, do

```
PYTHONPATH=digital_microscope/assets/robot_files west twister -p native_sim_64 -vvv -c -T digital_microscope/
```

The setting of `PYTHONPATH` is necessary as we have a custom library for implementation,
`-vvv` makes it more verbose to see progress.

Afterwards, the results of the test executions are shown (4 of 15 fail, as `always` FRET keyword is not implemented).
