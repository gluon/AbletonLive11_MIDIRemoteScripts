# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\TimeDisplay.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4062 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range, str
from .MackieControlComponent import *

class TimeDisplay(MackieControlComponent):

    def __init__(self, main_script):
        MackieControlComponent.__init__(self, main_script)
        self._TimeDisplay__main_script = main_script
        self._TimeDisplay__show_beat_time = False
        self._TimeDisplay__smpt_format = Live.Song.TimeFormat.smpte_25
        self._TimeDisplay__last_send_time = []
        self.show_beats()

    def destroy(self):
        self.clear_display()
        MackieControlComponent.destroy(self)

    def show_beats(self):
        self._TimeDisplay__show_beat_time = True
        self.send_midi((NOTE_ON_STATUS, SELECT_BEATS_NOTE, BUTTON_STATE_ON))
        self.send_midi((NOTE_ON_STATUS, SELECT_SMPTE_NOTE, BUTTON_STATE_OFF))

    def show_smpte(self, smpte_mode):
        self._TimeDisplay__show_beat_time = False
        self._TimeDisplay__smpt_format = smpte_mode
        self.send_midi((NOTE_ON_STATUS, SELECT_BEATS_NOTE, BUTTON_STATE_OFF))
        self.send_midi((NOTE_ON_STATUS, SELECT_SMPTE_NOTE, BUTTON_STATE_ON))

    def toggle_mode(self):
        if self._TimeDisplay__show_beat_time:
            self.show_smpte(self._TimeDisplay__smpt_format)
        else:
            self.show_beats()

    def clear_display(self):
        time_string = [' ' for i in range(10)]
        self._TimeDisplay__send_time_string(time_string, show_points=False)
        self.send_midi((NOTE_ON_STATUS, SELECT_BEATS_NOTE, BUTTON_STATE_OFF))
        self.send_midi((NOTE_ON_STATUS, SELECT_SMPTE_NOTE, BUTTON_STATE_OFF))

    def refresh_state(self):
        self.show_beats()
        self._TimeDisplay__last_send_time = []

    def on_update_display_timer(self):
        if self._TimeDisplay__show_beat_time:
            time_string = str(self.song().get_current_beats_song_time())
        else:
            time_string = str(self.song().get_current_smpte_song_time(self._TimeDisplay__smpt_format))
        time_string = [c for c in time_string if c not in ('.', ':')]
        if self._TimeDisplay__last_send_time != time_string:
            self._TimeDisplay__last_send_time = time_string
            self._TimeDisplay__send_time_string(time_string, show_points=True)

    def __send_time_string(self, time_string, show_points):
        for c in range(0, 10):
            char = time_string[9 - c].upper()
            char_code = g7_seg_led_conv_table[char]
            if show_points:
                if c in (3, 5, 7):
                    char_code += 64
            self.send_midi((176, 64 + c, char_code))