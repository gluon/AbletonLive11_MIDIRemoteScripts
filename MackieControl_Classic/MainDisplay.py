<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/MackieControl_Classic/MainDisplay.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 3523 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import as_ascii
from .MackieControlComponent import *

class MainDisplay(MackieControlComponent):

    def __init__(self, main_script):
        MackieControlComponent.__init__(self, main_script)
        self._MainDisplay__stack_offset = 0
        self._MainDisplay__last_send_messages = [[], []]

    def destroy(self):
        NUM_CHARS_PER_DISPLAY_LINE = 54
        upper_message = 'Ableton Live'.center(NUM_CHARS_PER_DISPLAY_LINE)
        self.send_display_string(upper_message, 0, 0)
        lower_message = 'Device is offline'.center(NUM_CHARS_PER_DISPLAY_LINE)
        self.send_display_string(lower_message, 1, 0)
        MackieControlComponent.destroy(self)

    def stack_offset(self):
        return self._MainDisplay__stack_offset

    def set_stack_offset(self, offset):
        self._MainDisplay__stack_offset = offset

    def send_display_string(self, display_string, display_row, cursor_offset):
        if display_row == 0:
            offset = cursor_offset
        else:
<<<<<<< HEAD
            if display_row == 1:
                offset = NUM_CHARS_PER_DISPLAY_LINE + 2 + cursor_offset
            else:
                pass
        message_string = as_ascii(display_string)
=======
            pass
        message_string = [ord(c) for c in display_string]
        for i in range(len(message_string)):
            if message_string[i] >= 128:
                message_string[i] = 0

>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        if self._MainDisplay__last_send_messages[display_row] != message_string:
            self._MainDisplay__last_send_messages[display_row] = message_string
            if self.main_script().is_extension():
                device_type = SYSEX_DEVICE_TYPE_XT
            else:
                device_type = SYSEX_DEVICE_TYPE
            display_sysex = (
             240, 0, 0, 102, device_type, 18, offset) + tuple(message_string) + (247, )
            self.send_midi(display_sysex)

    def refresh_state(self):
        self._MainDisplay__last_send_messages = [[], []]

    def on_update_display_timer(self):
        pass