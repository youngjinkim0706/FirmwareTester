#
# Copyright (c) 2019 - 2020, Nordic Semiconductor ASA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form, except as embedded into a Nordic
#    Semiconductor ASA integrated circuit in a product or a software update for
#    such product, must reproduce the above copyright notice, this list of
#    conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of Nordic Semiconductor ASA nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# 4. This software, with or without modification, must only be used with a
#    Nordic Semiconductor ASA integrated circuit.
#
# 5. Any software provided in binary form under this license must not be reverse
#    engineered, decompiled, modified and/or disassembled.
#
# THIS SOFTWARE IS PROVIDED BY NORDIC SEMICONDUCTOR ASA "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY, NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NORDIC SEMICONDUCTOR ASA OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Common constants, defined by Zigbee specification.
from enum import Enum

class TYPES:
    BOOL    = 0x10
    UINT8   = 0x20
    UINT16  = 0x21
    UINT32  = 0x23
    UINT64  = 0x27
    SINT8   = 0x28
    SINT16  = 0x29
    SINT64  = 0x2f
    ENUM8   = 0x30
    MAP8    = 0x18
    MAP16   = 0x19
    EUI64   = 0xF0
    STRING  = 0x42



DEFAULT_ZIGBEE_PROFILE_ID = 0x0104 # HA profile ID
BROADCAST_ADDRESS_ALL_DEVICES=0xffff
UNKNOWN_IEEE_ADDRESS = 0xFFFFFFFFFFFFFFFF

# Add New Cluster Here

BASIC_CLUSTER       = 0x0000
IDENTIFY_CLUSTER    = 0x0003
SCENE_CLUSTER       = 0X0005               
ON_OFF_CLUSTER      = 0x0006
LVL_CTRL_CLUSTER    = 0x0008
OTA_CLUSTER         = 0x0019
COLOR_CTRL_CLUSTER  = 0x0300
TEMPERATURE_CLUSTER = 0x0402
PRESSURE_CLUSTER    = 0x0403

# Add cluster name and value into dictionary

clusters = {}
clusters['BASIC_CLUSTER'] = BASIC_CLUSTER
clusters['IDENTIFY_CLUSTER'] = IDENTIFY_CLUSTER
clusters['SCENE_CLUSTER'] = SCENE_CLUSTER
clusters['ON_OFF_CLUSTER'] = ON_OFF_CLUSTER
clusters['LVL_CTRL_CLUSTER'] = LVL_CTRL_CLUSTER
clusters['OTA_CLUSTER'] = OTA_CLUSTER
clusters['COLOR_CTRL_CLUSTER'] = COLOR_CTRL_CLUSTER
clusters['TEMPERATURE_CLUSTER'] = TEMPERATURE_CLUSTER
clusters['PRESSURE_CLUSTER'] = PRESSURE_CLUSTER



ZCL_VERSION_ATTR              = 0x0000
IDENTIFY_IDENTIFY_TIME_ATTR   = 0x0000

CLUSTER_REVISION_ATTR         = 0xfffd      # added by @hipiphock
ATTR_REPORTING_STATUS_ATTR    = 0xfffe      # added by @hipiphock

SCENE_SCENE_COUNT_ATTR        = 0X0000      # added by @hipiphock
SCENE_CURRENT_SCENE_ATTR      = 0x0001      # added by @hipiphock
SCENE_CURRENT_GROUP_ATTR      = 0X0002      # added by @hipiphock
SCENE_SCENE_VALID_ATTR        = 0X0003      # added by @hipiphock
SCENE_NAME_SUPPORT_ATTR       = 0X0004      # added by @hipiphock

ON_OFF_ONOFF_ATTR             = 0x0000

LVL_CTRL_CURR_LVL_ATTR        = 0x0000
LVL_CTRL_REMAIN_TIME_ATTR     = 0X0001      # added by @hipiphock
LVL_CTRL_ONOFF_TRANS_TIME_ATTR= 0x0010      # added by @hipiphock
LVL_CTRL_ON_LEVEL_ATTR        = 0X0011      # added by @hipiphock

COLOR_CTRL_CURR_HUE_ATTR                = 0x0000
COLOR_CTRL_CURR_SAT_ATTR                = 0x0001
COLOR_CTRL_REMAIN_TIME_ATTR             = 0x0002        # added by @hipiphock
COLOR_CTRL_CURR_X_ATTR                  = 0X0003        # added by @hipiphock
COLOR_CTRL_CURR_Y_ATTR                  = 0X0004        # added by @hipiphock
COLOR_CTRL_COLOR_TEMP_MIRED_ATTR        = 0X0007        # added by @hipiphock
COLOR_CTRL_COLOR_MODE_ATTR              = 0X0008        # added by @hipiphock
COLOR_CTRL_ENHANCED_COLOR_MODE_ATTR     = 0x4001        # added by @hipiphock
COLOR_CTRL_COLOR_CAPABILITY_ATTR        = 0x400a        # added by @hipiphock
COLOR_CTRL_COLOR_TEMP_MIN_MIRED_ATTR    = 0x400b        # added by @hipiphock
COLOR_CTRL_COLOR_TEMP_MAX_MIRED_ATTR    = 0x400c        # added by @hipiphock

attributes = {}

attributes['ON_OFF_ONOFF_ATTR'] = (ON_OFF_ONOFF_ATTR, TYPES.BOOL)

attributes['LVL_CTRL_CURR_LVL_ATTR']    = (LVL_CTRL_CURR_LVL_ATTR, TYPES.UINT8)
attributes['LVL_CTRL_REMAIN_TIME_ATTR'] = (LVL_CTRL_REMAIN_TIME_ATTR, TYPES.UINT16)
attributes['LVL_CTRL_ONOFF_TRANS_TIME_ATTR'] = (LVL_CTRL_ONOFF_TRANS_TIME_ATTR, TYPES.UINT16)
attributes['LVL_CTRL_ON_LEVEL_ATTR']    = (LVL_CTRL_ON_LEVEL_ATTR, TYPES.UINT8)

attributes['COLOR_CTRL_CURR_HUE_ATTR']      = (COLOR_CTRL_CURR_HUE_ATTR, TYPES.UINT8)
attributes['COLOR_CTRL_CURR_SAT_ATTR']      = (COLOR_CTRL_CURR_SAT_ATTR, TYPES.UINT8)
attributes['COLOR_CTRL_REMAIN_TIME_ATTR']   = (COLOR_CTRL_REMAIN_TIME_ATTR, TYPES.UINT16)
attributes['COLOR_CTRL_CURR_X_ATTR']        = (COLOR_CTRL_CURR_X_ATTR, TYPES.UINT16)
attributes['COLOR_CTRL_CURR_Y_ATTR']        = (COLOR_CTRL_CURR_Y_ATTR, TYPES.UINT16)
attributes['COLOR_CTRL_COLOR_TEMP_MIRED_ATTR']      = (COLOR_CTRL_COLOR_TEMP_MIRED_ATTR, TYPES.UINT16)
attributes['COLOR_CTRL_COLOR_MODE_ATTR']    = (COLOR_CTRL_COLOR_MODE_ATTR, TYPES.ENUM8)
attributes['COLOR_CTRL_ENHANCED_COLOR_MODE_ATTR']   = (COLOR_CTRL_ENHANCED_COLOR_MODE_ATTR, TYPES.ENUM8)
attributes['COLOR_CTRL_COLOR_CAPABILITY_ATTR']      = (COLOR_CTRL_COLOR_CAPABILITY_ATTR, TYPES.MAP16)
attributes['COLOR_CTRL_COLOR_TEMP_MIN_MIRED_ATTR']  = (COLOR_CTRL_COLOR_TEMP_MIN_MIRED_ATTR, TYPES.UINT16)
attributes['COLOR_CTRL_COLOR_TEMP_MAX_MIRED_ATTR']  = (COLOR_CTRL_COLOR_TEMP_MAX_MIRED_ATTR, TYPES.UINT16)



OTA_CURRENT_FILE_VERSION_ATTR = 0x0002
OTA_UPGRADE_SERVER_ID_ATTR    = 0x0000

IDENTIFY_IDENTIFY_CMD                = 0x00
IDENTIFY_IDENTIFY_QUERY_CMD          = 0x01
IDENTIFY_EZ_MODE_INVOKE_CMD          = 0x02
IDENTIFY_UPDATE_COMMISSION_STATE_CMD = 0x03

SCENE_ADD_SCENE_CMD               = 0x00    # added by @hipiphock
SCENE_VEIW_SCENE_CMD              = 0X01    # added by @hipiphock
SCENE_REMOVE_SCENE_CMD            = 0X02    # added by @hipiphock
SCENE_REMOVE_ALL_SCENE_CMD        = 0X03    # added by @hipiphock
SCENE_STORE_SCENE_CMD             = 0X04    # added by @hipiphock
SCENE_RECALL_SCENE_CMD            = 0X05    # added by @hipiphock
SCENE_GET_SCENE_MEMBERSHIP_CMD    = 0X06    # added by @hipiphock
SCENE_ENHANCED_ADD_SCENE_CMD      = 0X40    # added by @hipiphock
SCENE_ENHANCED_VIEW_SCENE_CMD     = 0X41    # added by @hipiphock
SCENE_COPY_SCENE_CMD              = 0X42    # added by @hipiphock

ON_OFF_OFF_CMD                    = 0x00
ON_OFF_ON_CMD                     = 0x01
ON_OFF_TOGGLE_CMD                 = 0X02    # added by @hipiphock

LVL_CTRL_MV_TO_LVL_CMD            = 0x00
LVL_CTRL_MOVE_CMD                 = 0X01    # added by @hipiphock
LVL_CTRL_STEP_CMD                 = 0X02    # added by @hipiphock
LVL_CTRL_STOP_CMD                 = 0X03    # added by @hipiphock
LVL_CTRL_MV_TO_LVL_ONOFF_CMD      = 0x04    # added by @hipiphock
LVL_CTRL_MOVE_ONOFF_CMD           = 0X05    # added by @hipiphock
LVL_CTRL_STEP_ONOFF_CMD           = 0X06    # added by @hipiphock
LVL_CTRL_STOP_ONOFF_CMD           = 0X07    # added by @hipiphock

COLOR_CTRL_MV_TO_HUE_CMD          = 0x00
COLOR_CTRL_MV_TO_SAT_CMD          = 0x03
COLOR_CTRL_MV_TO_HUE_SAT_CMD      = 0x06
COLOR_CTRL_MV_TO_COLOR_CMD        = 0X07    # added by @hipiphock
COLOR_CTRL_MOVE_COLOR_CMD         = 0X08    # added by @hipiphock
COLOR_CTRL_STEP_COLOR_CMD         = 0X09    # added by @hipiphock
COLOR_CTRL_MV_TO_COLOR_TEMP_CMD   = 0X0a    # added by @hipiphock
COLOR_CTRL_STOP_MOVE_STEP_CMD     = 0X47    # added by @hipiphock
COLOR_CTRL_MV_COLOR_TEMP_CMD      = 0X4B    # added by @hipiphock
COLOR_CTRL_STEP_COLOR_TEMP_CMD    = 0X4C    # added by @hipiphock

OTA_QUERY_NEXT_IMAGE_RESPONSE_CMD = 0x02
CONFIGURE_REPORTING_CMD           = 0x06
READ_ATTRIBUTES_CMD               = 0x00

commands = {}
commands['ON_OFF_CLUSTER']                  = {}
commands['ON_OFF_CLUSTER']['OFF']           = ON_OFF_OFF_CMD
commands['ON_OFF_CLUSTER']['ON']            = ON_OFF_ON_CMD
commands['ON_OFF_CLUSTER']['TOGGLE']        = ON_OFF_TOGGLE_CMD
commands['LVL_CTRL_CLUSTER']                = {}
commands['LVL_CTRL_CLUSTER']['MOVE_TO']     = LVL_CTRL_MV_TO_LVL_CMD
commands['LVL_CTRL_CLUSTER']['MOVE']        = LVL_CTRL_MOVE_CMD # we don't know the range of RATE
commands['LVL_CTRL_CLUSTER']['STEP']        = LVL_CTRL_STEP_CMD
commands['LVL_CTRL_CLUSTER']['STOP']        = LVL_CTRL_STOP_CMD
commands['LVL_CTRL_CLUSTER']['MOVE_TO_ONOFF'] = LVL_CTRL_MV_TO_LVL_ONOFF_CMD
commands['LVL_CTRL_CLUSTER']['MOVE_ONOFF']  = LVL_CTRL_MOVE_ONOFF_CMD
commands['LVL_CTRL_CLUSTER']['STEP_ONOFF']  = LVL_CTRL_STEP_ONOFF_CMD
commands['LVL_CTRL_CLUSTER']['STOP_ONOFF']  = LVL_CTRL_STOP_ONOFF_CMD
commands['COLOR_CTRL_CLUSTER']                          = {}
commands['COLOR_CTRL_CLUSTER']['MOVE_TO_MIRED']         = COLOR_CTRL_MV_TO_COLOR_TEMP_CMD
commands['COLOR_CTRL_CLUSTER']['MOVE_TO_HUE']           = COLOR_CTRL_MV_TO_HUE_CMD
commands['COLOR_CTRL_CLUSTER']['MOVE_TO_SAT']           = COLOR_CTRL_MV_TO_SAT_CMD
commands['COLOR_CTRL_CLUSTER']['MOVE_TO_HUE_AND_SAT']   = COLOR_CTRL_MV_TO_HUE_SAT_CMD
commands['COLOR_CTRL_CLUSTER']['MOVE_TO_COLOR']         = COLOR_CTRL_MV_TO_COLOR_CMD
commands['COLOR_CTRL_CLUSTER']['MOVE_COLOR']            = COLOR_CTRL_MOVE_COLOR_CMD
commands['COLOR_CTRL_CLUSTER']['STEP_COLOR']            = COLOR_CTRL_STEP_COLOR_CMD
commands['COLOR_CTRL_CLUSTER']['STOP_MOVE_STEP']        = COLOR_CTRL_STOP_MOVE_STEP_CMD
commands['COLOR_CTRL_CLUSTER']['MOVE_MIRED']            = COLOR_CTRL_MV_COLOR_TEMP_CMD
commands['COLOR_CTRL_CLUSTER']['STEP_MIRED']            = COLOR_CTRL_STEP_COLOR_TEMP_CMD



FRAME_CTRL_TYPE_PROFILE_WIDE     = 0b00
FRAME_CTRL_TYPE_CLUSTER_SPECIFIC = 0b01
FRAME_CTRL_DIRECTION_TO_CLIENT   = 0b1
FRAME_CTRL_DIRECTION_TO_SERVER   = 0b0
FRAME_CTRL_STR = "0b000{disable_def_response:01b}{direction:01b}{manuf_specific:01b}{type:02b}"

OTA_QUERY_NEXT_IMAGE_RESPONSE_CTRL = int(FRAME_CTRL_STR.format(type=FRAME_CTRL_TYPE_CLUSTER_SPECIFIC, manuf_specific=False,
                                                               direction=FRAME_CTRL_DIRECTION_TO_CLIENT, disable_def_response=True), 2)
CONFIGURE_REPORTING_CTRL = int(FRAME_CTRL_STR.format(type=FRAME_CTRL_TYPE_PROFILE_WIDE, manuf_specific=False,
                                                     direction=FRAME_CTRL_DIRECTION_TO_SERVER, disable_def_response=True), 2)

REP_CONFIG_SEND_REPORTS = 0x00
REP_CONFIG_RECV_REPORTS = 0x01
REP_CONFIG_FORMAT_STR = "{direction:02X}{attribute.id:04X}{attribute.type:02X}{min_interval:02X}{max_interval:02X}{rep_change}"

ZCL_RAW_FORMAT_STR = "{frame_ctrl:02X}{seq_num:02X}{cmd_id:02X}{payload}"



class ZCLDirection(Enum):
    DIRECTION_CLI_TO_SRV = 0x00
    DIRECTION_SRV_TO_CLI = 0x01


CLI_ENDPOINT                 = 64    # Default Zigbee CLI endpoint
DOOR_LOCK_ENDPOINT           = 8     # Default Door Lock endpoint
LIGHT_BULB_ENDPOINT          = 10    # Default Light Bulb endpoint
LIGHT_SWITCH_ENDPOINT        = 1     # Default Light Switch endpoint
THINGY_PROXY_THINGY_ENDPOINT = 10    # One of the endpoints of Thingy on the Thingy Proxy
OTA_CLIENT_ENDPOINT          = 10    # Default OTA Client endpoint

ULTRA_THIN_WAFER_ENDPOINT    = 8     # Ultra Thin Wafer Endpoint, added by @hipiphock

DOOR_LOCK_OPEN  = 1
DOOR_LOCK_CLOSE = 0

##### Additional Declaration #####
# added by @hipiphock
ZIGBEE_CONNECTION           = 0
BLE_CONNECTION              = 1

COMMAND_TASK                = 0      # added by @hipiphock
READ_ATTRIBUTE_TASK         = 1      # added by @hipiphock
WRITE_ATTRIBUTE_TASK        = 2      # added by @hipiphock



##### Value Range #####
