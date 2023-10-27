# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\sysex.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 5313 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from functools import reduce
from ableton.v2.base import group, in_range
from pushbase.touch_strip_element import TouchStripModes, TouchStripStates
START = (240, 71, 127, 21)
CLEAR_LINE1 = START + (28, 0, 0, 247)
CLEAR_LINE2 = START + (29, 0, 0, 247)
CLEAR_LINE3 = START + (30, 0, 0, 247)
CLEAR_LINE4 = START + (31, 0, 0, 247)
WRITE_LINE1 = START + (24, 0, 69, 0)
WRITE_LINE2 = START + (25, 0, 69, 0)
WRITE_LINE3 = START + (26, 0, 69, 0)
WRITE_LINE4 = START + (27, 0, 69, 0)
WELCOME_MESSAGE = START + (1, 1, 247)
GOOD_BYE_MESSAGE = START + (1, 0, 247)
ALL_PADS_SENSITIVITY_PREFIX = START + (93, 0, 32)
PAD_SENSITIVITY_PREFIX = START + (90, 0, 33)
PAD_PARAMETER_PREFIX = START + (71, 0, 9)
DEFAULT_PEAK_SAMPLING_TIME = 50
DEFAULT_AFTERTOUCH_THRESHOLD = 0
DEFAULT_AFTERTOUCH_GATE_TIME = 500
SET_AFTERTOUCH_MODE = START + (92, 0, 1)
POLY_AFTERTOUCH = (0, )
MONO_AFTERTOUCH = (1, )
MODE_CHANGE = START + (98, 0, 1)

def make_pad_parameter_message(aftertouch_threshold=DEFAULT_AFTERTOUCH_THRESHOLD, peak_sampling_time=DEFAULT_PEAK_SAMPLING_TIME, aftertouch_gate_time=DEFAULT_AFTERTOUCH_GATE_TIME):
    return to_bytes(peak_sampling_time, 4) + to_bytes(aftertouch_gate_time, 4) + (aftertouch_threshold,)


def to_sysex_int(number, unused_parameter_name):
    return (
     number >> 12 & 15, number >> 8 & 15, number >> 4 & 15, number & 15)


CALIBRATION_SET = START + (87, 0, 20) + to_sysex_int(215, 'Preload Scale Factor') + to_sysex_int(1000, 'Recalibration Interval') + to_sysex_int(200, 'Stuck Pad Detection Threshold') + to_sysex_int(0, 'Stuck Pad NoteOff Threshold Adder') + to_sysex_int(200, 'Pad Ignore Time') + (247, )
IDENTITY_ENQUIRY = (240, 126, 0, 6, 1, 247)
IDENTITY_PREFIX = (240, 126, 0, 6, 2, 71, 21, 0, 25)
DONGLE_ENQUIRY_PREFIX = START + (80, )
DONGLE_PREFIX = START + (81, )

def make_presentation_message(application):
    return START + (
     96,
     0,
     4,
     65,
     application.get_major_version(),
     application.get_minor_version(),
     application.get_bugfix_version(),
     247)


TOUCHSTRIP_MODE_TO_VALUE = [
 TouchStripModes.CUSTOM_PITCHBEND,
 TouchStripModes.CUSTOM_VOLUME,
 TouchStripModes.CUSTOM_PAN,
 TouchStripModes.CUSTOM_DISCRETE,
 TouchStripModes.CUSTOM_FREE,
 TouchStripModes.PITCHBEND,
 TouchStripModes.VOLUME,
 TouchStripModes.PAN,
 TouchStripModes.DISCRETE,
 TouchStripModes.MODWHEEL]

def make_touch_strip_mode_message(mode):
    return START + (99, 0, 1, TOUCHSTRIP_MODE_TO_VALUE.index(mode), 247)


TOUCHSTRIP_STATE_TO_VALUE = {TouchStripStates.STATE_OFF: 0, 
 TouchStripStates.STATE_HALF: 1, 
 TouchStripStates.STATE_FULL: 3}

def make_touch_strip_light_message(state):
    state = [TOUCHSTRIP_STATE_TO_VALUE[s] for s in state]
    group_size = 3
    bytes = [reduce(lambda byte, idx_state: byte | idx_state[1] << 2 * idx_state[0]
, enumerate(state_group), 0) for state_group in group(state, group_size)]
    return START + (100, 0, 8) + tuple(bytes) + (247, )


def to_bytes(number, size):
    return tuple([number >> offset & 15 for offset in range((size - 1) * 4, -1, -4)])