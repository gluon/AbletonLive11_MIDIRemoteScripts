# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL_Classic\DisplayController.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 8509 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range, str
from ableton.v3.base import as_ascii
from .consts import *
from .RemoteSLComponent import RemoteSLComponent

class DisplayController(RemoteSLComponent):

    def __init__(self, remote_sl_parent):
        RemoteSLComponent.__init__(self, remote_sl_parent)
        self._DisplayController__left_strip_names = [str() for x in range(NUM_CONTROLS_PER_ROW)]
        self._DisplayController__left_strip_parameters = [None for x in range(NUM_CONTROLS_PER_ROW)]
        self._DisplayController__right_strip_names = [str() for x in range(NUM_CONTROLS_PER_ROW)]
        self._DisplayController__right_strip_parameters = [None for x in range(NUM_CONTROLS_PER_ROW)]
        self.refresh_state()

    def disconnect(self):
        self._DisplayController__send_clear_displays()

    def setup_left_display(self, names, parameters):
        self._DisplayController__left_strip_names = names
        self._DisplayController__left_strip_parameters = parameters

    def setup_right_display(self, names, parameters):
        self._DisplayController__right_strip_names = names
        self._DisplayController__right_strip_parameters = parameters

    def update_display(self):
        for row_id in (1, 2, 3, 4):
            message_string = ''
            if row_id == 1 or row_id == 2:
                if row_id == 1:
                    strip_names = self._DisplayController__left_strip_names
                else:
                    strip_names = self._DisplayController__right_strip_names
                if len(strip_names) == NUM_CONTROLS_PER_ROW:
                    for s in strip_names:
                        message_string += self._DisplayController__generate_strip_string(s)

                else:
                    message_string += strip_names[0]
            else:
                if row_id == 3 or row_id == 4:
                    if row_id == 3:
                        parameters = self._DisplayController__left_strip_parameters
                    else:
                        parameters = self._DisplayController__right_strip_parameters
                    for p in parameters:
                        if p:
                            message_string += self._DisplayController__generate_strip_string(str(p))
                        else:
                            message_string += self._DisplayController__generate_strip_string('')

                else:
                    pass
                self._DisplayController__send_display_string(message_string, row_id, offset=0)

    def refresh_state(self):
        self._DisplayController__last_send_row_id_messages = [
         None, [], [], [], []]

    def __send_clear_displays(self):
        start_clear_sysex = (240, 0, 32, 41, 3, 3, 18, 0)
        left_end_sysex = (ABLETON_PID, 0, 2, 2, 4, 247)
        right_end_sysex = (ABLETON_PID, 0, 2, 2, 5, 247)
        self.send_midi(start_clear_sysex + left_end_sysex)
        self.send_midi(start_clear_sysex + right_end_sysex)

    def __send_display_string(self, message, row_id, offset=0):
        final_message = ' ' * offset + message
        if len(final_message) < NUM_CHARS_PER_DISPLAY_LINE:
            fill_up = NUM_CHARS_PER_DISPLAY_LINE - len(final_message)
            final_message = final_message + ' ' * fill_up
        else:
            if len(final_message) >= NUM_CHARS_PER_DISPLAY_LINE:
                final_message = final_message[0:NUM_CHARS_PER_DISPLAY_LINE]
        final_offset = 0
        sysex_header = (
         240,
         0,
         32,
         41,
         3,
         3,
         18,
         0,
         ABLETON_PID,
         0,
         2,
         1)
        sysex_pos = (
         final_offset, row_id)
        sysex_text_command = (4, )
        sysex_text = tuple(as_ascii(final_message))
        sysex_close_up = (247, )
        full_sysex = sysex_header + sysex_pos + sysex_text_command + sysex_text + sysex_close_up
        if self._DisplayController__last_send_row_id_messages[row_id] != full_sysex:
            self._DisplayController__last_send_row_id_messages[row_id] = full_sysex
            self.send_midi(full_sysex)

    def __generate_strip_string(self, display_string):
        if not display_string:
            return ' ' * NUM_CHARS_PER_DISPLAY_STRIP
        if len(display_string.strip()) > NUM_CHARS_PER_DISPLAY_STRIP - 1:
            if display_string.endswith('dB'):
                if display_string.find('.') != -1:
                    display_string = display_string[:-2]
        if len(display_string) > NUM_CHARS_PER_DISPLAY_STRIP - 1:
            for um in (' ', 'i', 'o', 'u', 'e', 'a'):
                while len(display_string) > NUM_CHARS_PER_DISPLAY_STRIP - 1:
                    if display_string.rfind(um, 1) != -1:
                        um_pos = display_string.rfind(um, 1)
                        display_string = display_string[:um_pos] + display_string[um_pos + 1:]

        else:
            display_string = display_string.center(NUM_CHARS_PER_DISPLAY_STRIP - 1)
        return display_string[:NUM_CHARS_PER_DISPLAY_STRIP - 1] + ' '