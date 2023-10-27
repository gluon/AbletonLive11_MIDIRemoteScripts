# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\display_util.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 3284 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import as_ascii
from ableton.v3.control_surface.elements import adjust_string
from ableton.v3.live import is_song_recording, is_track_armed, song
from .midi import DISPLAY_HEADER, SYSEX_END
LINE_1_WIDTH = 10
LINE_2_WIDTH = 18
TERMINATOR_BYTE = 0
LINE_1_BYTE = 1
LINE_2_BYTE = 2
FULL_SCREEN_BYTE = 7
PARAMETER_SCREEN_BYTE = 8
BLANK_PARAMETER_BYTE = 9
NON_TRANSIENT_BYTE = 1
TRANSIENT_BYTE = 2
OPTIONS_BYTE = 31
PICTOGRAM_BYTES = {
  None: 0, 'arp': 1, 'play': 2, 'record': 3, 'arm': 4}

def format_string(string, width):
    return tuple(as_ascii(adjust_string(string, width).strip()))


def get_full_screen_option_bytes(track, display_pictograms):
    option_bytes = [
     OPTIONS_BYTE,
     FULL_SCREEN_BYTE,
     NON_TRANSIENT_BYTE,
     PICTOGRAM_BYTES[None],
     PICTOGRAM_BYTES[None],
     PICTOGRAM_BYTES[None],
     TERMINATOR_BYTE]
    if display_pictograms:
        option_bytes[3] = PICTOGRAM_BYTES['record'] if is_song_recording() else PICTOGRAM_BYTES['play'] if song().is_playing else PICTOGRAM_BYTES[None]
        option_bytes[4] = PICTOGRAM_BYTES['arm'] if is_track_armed(track) else PICTOGRAM_BYTES[None]
        option_bytes[5] = PICTOGRAM_BYTES['arp']
    return tuple(option_bytes)


def make_full_screen_message(line_1, line_2, track, display_pictograms=True):
    return DISPLAY_HEADER + get_full_screen_option_bytes(track, display_pictograms) + (LINE_1_BYTE,) + format_string(line_1, LINE_1_WIDTH) + (TERMINATOR_BYTE, LINE_2_BYTE) + format_string(line_2, LINE_2_WIDTH) + (TERMINATOR_BYTE, SYSEX_END)


def make_parameter_message(cc_no, line_1, line_2):
    return DISPLAY_HEADER + (OPTIONS_BYTE, PARAMETER_SCREEN_BYTE, TRANSIENT_BYTE, cc_no, TERMINATOR_BYTE) + (LINE_1_BYTE,) + format_string(line_1, LINE_1_WIDTH) + (TERMINATOR_BYTE, LINE_2_BYTE) + format_string(line_2, LINE_2_WIDTH) + (TERMINATOR_BYTE, SYSEX_END)


def make_blank_parameter_message(cc_no):
    return DISPLAY_HEADER + (
     OPTIONS_BYTE,
     BLANK_PARAMETER_BYTE,
     TRANSIENT_BYTE,
     cc_no,
     TERMINATOR_BYTE,
     SYSEX_END)