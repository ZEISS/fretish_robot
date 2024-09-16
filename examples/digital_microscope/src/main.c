/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 Carl Zeiss Meditec AG
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <string.h>

#include <zephyr/shell/shell.h>
#include <zephyr/logging/log.h>
#include <stdlib.h>

enum mode_state {
  MODE_NORMAL,
  MODE_HOMING,
  MODE_SAMPLE_PREP,
  MODE_CAPTURE,
  MODE_TUBE_MOVING
};

enum illumination_state {
  ILLUMINATION_UNKNOWN,
  ILLUMINATION_ON,
  ILLUMINATION_OFF
};

static const int max_illumination_value = 100;

enum tube_movement_state { TUBE_HOLD, TUBE_MOVING_UP, TUBE_MOVING_DOWN };

static const int tube_min_height = 0;
static const int tube_max_height = 10;

static const int max_objectives = 5;

struct state {
  enum mode_state current_mode;
  enum illumination_state current_illumination;
  enum tube_movement_state current_tube_state;
  int actual_illumination_value;
  int configured_illumination_value;
  int tube_height;
  int current_objective;
  int objective_history[2];
};

#define INIT_STATE(s)                                                          \
  struct state s = {                                                           \
      MODE_NORMAL, ILLUMINATION_UNKNOWN, TUBE_HOLD, 50, 50, 5, 1, {-1, -1}}

INIT_STATE(default_state);
INIT_STATE(state);

static int cmd_mode_set(const struct shell *shell, size_t argc, char **argv) {
  if (argc < 2) {
    shell_print(shell, "Usage: mode set <normal|in_prepare|capture>");
    return -EINVAL;
  }

  if (strcmp(argv[1], "normal") == 0) {
    state.current_mode = MODE_NORMAL;
    shell_print(shell, "Mode set to normal");
  } else if (strcmp(argv[1], "homing") == 0) {
    state.current_mode = MODE_HOMING;
    shell_print(shell, "Mode set to homing");
  } else if (strcmp(argv[1], "sample_prep") == 0) {
    state.current_mode = MODE_SAMPLE_PREP;
    shell_print(shell, "Mode set to sample_prep");
  } else if (strcmp(argv[1], "capture") == 0) {
    state.current_mode = MODE_CAPTURE;
    shell_print(shell, "Mode set to capture");
  } else if (strcmp(argv[1], "tube_moving") == 0) {
    state.current_mode = MODE_TUBE_MOVING;
    shell_print(shell, "Mode set to tube_moving");
  } else {
    shell_print(shell, "Unknown mode: %s", argv[1]);
    return -EINVAL;
  }

  return 0;
}

static int cmd_illumination_active_on(const struct shell *shell, size_t argc,
                                      char **argv) {
  state.current_illumination = ILLUMINATION_ON;
  shell_print(shell, "Illumination turned on");
  return 0;
}

static int cmd_illumination_active_off(const struct shell *shell, size_t argc,
                                       char **argv) {
  state.current_illumination = ILLUMINATION_OFF;
  shell_print(shell, "Illumination turned off");
  return 0;
}

static int cmd_illumination_active_get(const struct shell *shell, size_t argc,
                                       char **argv) {
  switch (state.current_illumination) {
  case ILLUMINATION_ON:
    shell_print(shell, "Illumination is on");
    break;
  case ILLUMINATION_OFF:
    shell_print(shell, "Illumination is off");
    break;
  default:
    shell_print(shell, "Illumination state is unknown");
    break;
  }
  return 0;
}

static int cmd_illumination_value_get_actual(const struct shell *shell,
                                             size_t argc, char **argv) {
  shell_print(shell, "Actual illumination value: %d",
              state.actual_illumination_value);
  return 0;
}

static int cmd_illumination_value_get_configured(const struct shell *shell,
                                                 size_t argc, char **argv) {
  shell_print(shell, "Configured illumination value: %d",
              state.configured_illumination_value);
  return 0;
}

static int cmd_illumination_value_get_max(const struct shell *shell,
                                          size_t argc, char **argv) {
  shell_print(shell, "Maximum illumination value: %d", max_illumination_value);
  return 0;
}

static int cmd_illumination_value_increase(const struct shell *shell,
                                           size_t argc, char **argv) {
  // Increase by 10%
  int increase_amount = (max_illumination_value * 10) / 100;
  state.configured_illumination_value += increase_amount;

  if (state.configured_illumination_value > max_illumination_value) {
    state.configured_illumination_value = max_illumination_value;
  }

  shell_print(shell, "Configured illumination value increased by 10%% to: %d",
              state.configured_illumination_value);
  return 0;
}

static int cmd_illumination_value_get(const struct shell *shell, size_t argc,
                                      char **argv) {

  if (argc < 2) {
    shell_print(shell, "Usage: illumination value get <actual|configured|max>");
    return -EINVAL;
  }

  if (strcmp(argv[1], "actual") == 0) {
    return cmd_illumination_value_get_actual(shell, argc, argv);
  } else if (strcmp(argv[1], "configured") == 0) {
    return cmd_illumination_value_get_configured(shell, argc, argv);
  } else if (strcmp(argv[1], "max") == 0) {
    return cmd_illumination_value_get_max(shell, argc, argv);
  } else {
    shell_print(shell, "Unknown parameter: %s", argv[1]);
    return -EINVAL;
  }
}

static void update_tube_height() {
  if (state.current_tube_state == TUBE_MOVING_UP) {
    state.tube_height++;
    if (state.tube_height >= tube_max_height) {
      state.current_tube_state = TUBE_HOLD;
      state.current_mode = MODE_NORMAL;
    }
  } else if (state.current_tube_state == TUBE_MOVING_DOWN) {
    state.tube_height--;
    if (state.tube_height <= tube_min_height) {
      state.current_tube_state = TUBE_HOLD;
      state.current_mode = MODE_NORMAL;
    }
  }
}

static int cmd_tube_position_is_upper(const struct shell *shell, size_t argc,
                                      char **argv) {
  // simulate tube movement by calls
  update_tube_height();

  if (state.tube_height == tube_max_height) {
    shell_print(shell, "Tube is in the upper position (height: %d)",
                state.tube_height);
  } else {
    shell_print(shell, "Tube is not in the upper position (current height: %d)",
                state.tube_height);
  }
  return 0;
}

static int cmd_tube_position_is_bottom(const struct shell *shell, size_t argc,
                                       char **argv) {
  // simulate tube movement by calls
  update_tube_height();

  if (state.tube_height == tube_min_height) {
    shell_print(shell, "Tube is in the bottom position (height: %d)",
                state.tube_height);
  } else {
    shell_print(shell,
                "Tube is not in the bottom position (current height: %d)",
                state.tube_height);
  }
  return 0;
}

static int cmd_tube_move_up(const struct shell *shell, size_t argc,
                            char **argv) {
  state.current_tube_state = TUBE_MOVING_UP;
  state.current_mode = MODE_TUBE_MOVING;
  shell_print(shell, "Tube is moving up");
  return 0;
}

static int cmd_tube_move_down(const struct shell *shell, size_t argc,
                              char **argv) {
  state.current_tube_state = TUBE_MOVING_DOWN;
  state.current_mode = MODE_TUBE_MOVING;
  shell_print(shell, "Tube is moving down");
  return 0;
}

static int cmd_tube_move_get(const struct shell *shell, size_t argc,
                             char **argv) {
  switch (state.current_tube_state) {
  case TUBE_MOVING_UP:
    shell_print(shell, "Tube is moving upwards");
    break;
  case TUBE_MOVING_DOWN:
    shell_print(shell, "Tube is moving downwards");
    break;
  case TUBE_HOLD:
    shell_print(shell, "Tube is on hold");
    break;
  default:
    shell_print(shell, "Tube state is unknown");
  }
  return 0;
}

static void update_objective_history(int previous_objective) {
  state.objective_history[1] = state.objective_history[0];
  state.objective_history[0] = previous_objective;
}

static int cmd_objective_change(const struct shell *shell, size_t argc,
                                char **argv) {

  if (state.current_mode == MODE_TUBE_MOVING) {
    shell_print(shell,
                "Denied: Change of objective is not allowed while tube moving");
    return -EACCES;
  }

  int previous_objective = state.current_objective;

  // objective numbers start with 1
  state.current_objective = (state.current_objective % max_objectives) + 1;

  update_objective_history(previous_objective);

  shell_print(shell, "Objective changed to %d", state.current_objective);
  return 0;
}

static int cmd_objective_get(const struct shell *shell, size_t argc,
                             char **argv) {
  shell_print(shell, "Current objective: %d", state.current_objective);
  return 0;
}

static int cmd_objective_history(const struct shell *shell, size_t argc,
                                 char **argv) {
  shell_print(shell, "Previous objectives: %d %d", state.objective_history[0],
              state.objective_history[1]);
  return 0;
}

static int cmd_system_reset(const struct shell *shell, size_t argc,
                            char **argv) {
  shell_print(shell, "Resetting system...");

  state = default_state;

  return 0;
}

SHELL_STATIC_SUBCMD_SET_CREATE(subcmd_mode,
                               SHELL_CMD(set, NULL, "Set mode", cmd_mode_set),
                               SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(
    subcmd_illumination_active,
    SHELL_CMD(on, NULL, "Turn illumination on", cmd_illumination_active_on),
    SHELL_CMD(off, NULL, "Turn illumination off", cmd_illumination_active_off),
    SHELL_CMD(get, NULL, "Get illumination state", cmd_illumination_active_get),
    SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(subcmd_illumination_value,
                               SHELL_CMD(get, NULL, "Get illumination value",
                                         cmd_illumination_value_get),
                               SHELL_CMD(increase, NULL,
                                         "Increase illumination value by 10%%",
                                         cmd_illumination_value_increase),
                               SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(subcmd_illumination,
                               SHELL_CMD(active, &subcmd_illumination_active,
                                         "Control illumination state", NULL),
                               SHELL_CMD(value, &subcmd_illumination_value,
                                         "Get illumination value", NULL),
                               SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(
    subcmd_tube_position,
    SHELL_CMD(is_upper, NULL, "Check if tube is in the upper position",
              cmd_tube_position_is_upper),
    SHELL_CMD(is_bottom, NULL, "Check if tube is in the bottom position",
              cmd_tube_position_is_bottom),
    SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(
    subcmd_tube_move, SHELL_CMD(up, NULL, "Move tube up", cmd_tube_move_up),
    SHELL_CMD(down, NULL, "Move tube down", cmd_tube_move_down),
    SHELL_CMD(get, NULL, "Move tube down", cmd_tube_move_get),
    SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(
    subcmd_tube, SHELL_CMD(move, &subcmd_tube_move, "Move tube", NULL),
    SHELL_CMD(position, &subcmd_tube_position, "Check tube position", NULL),
    SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(
    subcmd_objective,
    SHELL_CMD(change, NULL, "Change to the next objective",
              cmd_objective_change),
    SHELL_CMD(get, NULL, "Get the current objective", cmd_objective_get),
    SHELL_CMD(history, NULL, "Get the last two objectives",
              cmd_objective_history),
    SHELL_SUBCMD_SET_END);

SHELL_STATIC_SUBCMD_SET_CREATE(subcmd_system,
                               SHELL_CMD(reset, NULL, "Reboot the system",
                                         cmd_system_reset),
                               SHELL_SUBCMD_SET_END);

SHELL_CMD_REGISTER(mode, &subcmd_mode, "Mode management", NULL);
SHELL_CMD_REGISTER(illumination, &subcmd_illumination, "Illumination control",
                   NULL);
SHELL_CMD_REGISTER(tube, &subcmd_tube, "Tube control", NULL);
SHELL_CMD_REGISTER(objective, &subcmd_objective, "Objective management", NULL);
SHELL_CMD_REGISTER(system, &subcmd_system, "System commands", NULL);
