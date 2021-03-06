import random
from DongleHandler import constants

DEFAULT_DURATION = 0.51

RANGE_FUNC = lambda : random.randrange(3, 254)


TASK_CMD = 0
TASK_READ = 1
TASK_WRITE = 2

ONOFF_COMMAND_LIST = {
    "ON" : constants.ON_OFF_ON_CMD,
    "OFF" : constants.ON_OFF_OFF_CMD,
    "TOGGLE" : constants.ON_OFF_TOGGLE_CMD
}

LEVEL_COMMAND_LIST = {
    "MOVE TO" : constants.LVL_CTRL_MV_TO_LVL_CMD,
    # "MOVE" : constants.LVL_CTRL_MOVE_CMD,
    "STEP" : constants.LVL_CTRL_STEP_CMD,
    "STOP" : constants.LVL_CTRL_STOP_CMD,
    "MOVE TO ONOFF" : constants.LVL_CTRL_MV_TO_LVL_ONOFF_CMD,
    # "MOVE ONOFF" : constants.LVL_CTRL_MOVE_ONOFF_CMD,
    "STEP ONOFF" : constants.LVL_CTRL_STEP_ONOFF_CMD,
    "STOP ONOFF" : constants.LVL_CTRL_STOP_ONOFF_CMD
}

COLOR_COMMAND_LIST = {
    "MOVE TO COLOR" : constants.COLOR_CTRL_MV_TO_COLOR_CMD,
    # "MOVE COLOR" : constants.COLOR_CTRL_MOVE_COLOR_CMD,
    "MOVE TO COLOR & TEMPERATURE" : constants.COLOR_CTRL_MV_TO_COLOR_TEMP_CMD,
    # "MOVE COLOR & TEMPERATURE": constants.COLOR_CTRL_MV_COLOR_TEMP_CMD,
    "STEP COLOR" : constants.COLOR_CTRL_STEP_COLOR_CMD,
    "STEP COLOR & TEMPERATURE": constants.COLOR_CTRL_STEP_COLOR_TEMP_CMD,
    "STOP MOVE STEP" : constants.COLOR_CTRL_STOP_MOVE_STEP_CMD,
}