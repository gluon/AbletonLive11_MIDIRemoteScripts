# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\sysex.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 8971 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import chunks
from ableton.v2.control_surface import midi
from pushbase.sysex import LIVE_MODE, USER_MODE
from pushbase.touch_strip_element import TouchStripModes, TouchStripStates
PAD_VELOCITY_CURVE_CHUNK_SIZE = 16
MODE_SWITCH_MESSAGE_ID = 10

def make_mono_aftertouch_enabled_message(scene, track, is_enabled):
    return make_message(51, (scene, track, int(is_enabled)))


def make_aftertouch_mode_message(mode_id):
    mode_byte = 0 if mode_id == 'mono' else 1
    return make_message(30, (mode_byte,))


def make_mode_switch_messsage(mode_id):
    return make_message(MODE_SWITCH_MESSAGE_ID, mode_id)


def make_rgb_palette_entry_message(index, hex_color, white_balance):
    r, g, b = _make_rgb_from_hex(hex_color)
    return make_message(3, (index,) + to_7L1M(r) + to_7L1M(g) + to_7L1M(b) + to_7L1M(white_balance))


def _make_rgb_from_hex(hex_value):
    r = hex_value >> 16
    g = hex_value >> 8 & 255
    b = hex_value & 255
    return (
     r, g, b)


def make_reapply_palette_message():
    return make_message(5)


def make_touch_strip_mode_message(mode):
    mode_bytes = ()
    if mode == TouchStripModes.CUSTOM_PITCHBEND:
        mode_bytes = int('1111001', 2)
    else:
        if mode == TouchStripModes.CUSTOM_VOLUME:
            mode_bytes = int('0000001', 2)
        else:
            if mode == TouchStripModes.CUSTOM_PAN:
                mode_bytes = int('0010001', 2)
            else:
                if mode == TouchStripModes.CUSTOM_DISCRETE:
                    mode_bytes = int('0011001', 2)
                else:
                    if mode == TouchStripModes.CUSTOM_FREE:
                        mode_bytes = int('0001011', 2)
                    else:
                        if mode == TouchStripModes.MODWHEEL:
                            mode_bytes = int('0000100', 2)
                        else:
                            if mode == TouchStripModes.PITCHBEND:
                                mode_bytes = int('1111000', 2)
                            else:
                                raise RuntimeError('Touch strip mode %i not supported' % mode)
    return make_message(23, (mode_bytes,))


TOUCHSTRIP_STATE_TO_BRIGHTNESS = {TouchStripStates.STATE_OFF: 0, 
 TouchStripStates.STATE_HALF: 1, 
 TouchStripStates.STATE_FULL: 6}

def _make_touch_strip_light(state):
    if len(state) == 2:
        return state[0] | state[1] << 3
    return state[0]


def make_touch_strip_light_message(states):
    states = [TOUCHSTRIP_STATE_TO_BRIGHTNESS[state] for state in states]
    return make_message(25, tuple([_make_touch_strip_light(state) for state in chunks(states, 2)]))


def make_pad_velocity_curve_message(index, velocities):
    return make_message(32, (index,) + tuple(velocities))


def make_pad_threshold_message(threshold1, threshold2, lower_channel_pressure_threshold, upper_channel_pressure_threshold):
    args = to_7L5M(threshold1) + to_7L5M(threshold2) + to_7L5M(lower_channel_pressure_threshold) + to_7L5M(upper_channel_pressure_threshold)
    return make_message(27, args)


def make_led_brightness_message(brightness):
    return make_message(6, (brightness,))


def make_display_brightness_message(brightness):
    return make_message(8, to_7L1M(brightness))


def extract_identity_response_info(data):
    major = data[12]
    minor = data[13]
    build = from_7L7M(data[14], data[15])
    sn = from_7L7777M(data[16:21])
    board_revision = data[21] if len(data) > 22 else 0
    return (
     major, minor, build, sn, board_revision)


def make_pad_setting_message(scene_index, track_index, setting):
    return make_message(40, (scene_index, track_index, setting))


MANUFACTURER_ID = (0, 33, 29)
MESSAGE_START = (
 midi.SYSEX_START,) + MANUFACTURER_ID + (1, 1)
IDENTITY_RESPONSE_PRODUCT_ID_BYTES = MANUFACTURER_ID + (103, 50, 2, 0)

def make_message(command_id, arguments=tuple()):
    return MESSAGE_START + (command_id,) + arguments + (midi.SYSEX_END,)


def make_message_identifier(command_id):
    return MESSAGE_START + (command_id,)


def to_7L1M(value):
    return (
     value & 127, value >> 7 & 1)


def to_7L5M(value):
    return (
     value & 127, value >> 7 & 31)


def from_7L7M(lsb, msb):
    return lsb + (msb << 7)


def from_7L7777M(data):
    return data[0] + (data[1] << 7) + (data[2] << 14) + (data[3] << 21) + (data[4] << 28)