# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl_Classic\MainDisplayController.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 10141 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range, str
from .MackieControlComponent import *

class MainDisplayController(MackieControlComponent):

    def __init__(self, main_script, display):
        MackieControlComponent.__init__(self, main_script)
        self._MainDisplayController__left_extensions = []
        self._MainDisplayController__right_extensions = []
        self._MainDisplayController__displays = [
         display]
        self._MainDisplayController__own_display = display
        self._MainDisplayController__parameters = [[] for x in range(NUM_CHANNEL_STRIPS)]
        self._MainDisplayController__channel_strip_strings = ['' for x in range(NUM_CHANNEL_STRIPS)]
        self._MainDisplayController__channel_strip_mode = True
        self._MainDisplayController__show_parameter_names = False
        self._MainDisplayController__bank_channel_offset = 0
        self._MainDisplayController__meters_enabled = False
        self._MainDisplayController__show_return_tracks = False

    def destroy(self):
        self.enable_meters(False)
        MackieControlComponent.destroy(self)

    def set_controller_extensions(self, left_extensions, right_extensions):
        self._MainDisplayController__left_extensions = left_extensions
        self._MainDisplayController__right_extensions = right_extensions
        self._MainDisplayController__displays = []
        stack_offset = 0
        for le in left_extensions:
            self._MainDisplayController__displays.append(le.main_display())
            le.main_display().set_stack_offset(stack_offset)
            stack_offset += NUM_CHANNEL_STRIPS

        self._MainDisplayController__displays.append(self._MainDisplayController__own_display)
        self._MainDisplayController__own_display.set_stack_offset(stack_offset)
        stack_offset += NUM_CHANNEL_STRIPS
        for re in right_extensions:
            self._MainDisplayController__displays.append(re.main_display())
            re.main_display().set_stack_offset(stack_offset)
            stack_offset += NUM_CHANNEL_STRIPS

        self._MainDisplayController__parameters = [[] for x in range(len(self._MainDisplayController__displays) * NUM_CHANNEL_STRIPS)]
        self._MainDisplayController__channel_strip_strings = ['' for x in range(len(self._MainDisplayController__displays) * NUM_CHANNEL_STRIPS)]
        self.refresh_state()

    def enable_meters(self, enabled):
        if self._MainDisplayController__meters_enabled != enabled:
            self._MainDisplayController__meters_enabled = enabled
            self.refresh_state()

    def set_show_parameter_names(self, enable):
        self._MainDisplayController__show_parameter_names = enable

    def set_channel_offset(self, channel_offset):
        self._MainDisplayController__bank_channel_offset = channel_offset

    def parameters(self):
        return self._MainDisplayController__parameters

    def set_parameters(self, parameters):
        if parameters:
            self.set_channel_strip_strings(None)
        for d in self._MainDisplayController__displays:
            self._MainDisplayController__parameters = parameters

    def channel_strip_strings(self):
        return self._MainDisplayController__channel_strip_strings

    def set_channel_strip_strings(self, channel_strip_strings):
        if channel_strip_strings:
            self.set_parameters(None)
        self._MainDisplayController__channel_strip_strings = channel_strip_strings

    def set_show_return_track_names(self, show_returns):
        self._MainDisplayController__show_return_tracks = show_returns

    def refresh_state(self):
        for d in self._MainDisplayController__displays:
            d.refresh_state()

    def on_update_display_timer(self):
        strip_index = 0
        for display in self._MainDisplayController__displays:
            if self._MainDisplayController__channel_strip_mode:
                upper_string = ''
                lower_string = ''
                track_index_range = list(range(self._MainDisplayController__bank_channel_offset + display.stack_offset(), self._MainDisplayController__bank_channel_offset + display.stack_offset() + NUM_CHANNEL_STRIPS))
                if self._MainDisplayController__show_return_tracks:
                    tracks = self.song().return_tracks
                else:
                    tracks = self.song().visible_tracks
                for t in track_index_range:
                    if self._MainDisplayController__parameters and self._MainDisplayController__show_parameter_names:
                        if self._MainDisplayController__parameters[strip_index]:
                            upper_string += self._MainDisplayController__generate_6_char_string(self._MainDisplayController__parameters[strip_index][1])
                        else:
                            upper_string += self._MainDisplayController__generate_6_char_string('')
                    else:
                        if t < len(tracks):
                            upper_string += self._MainDisplayController__generate_6_char_string(tracks[t].name)
                        else:
                            upper_string += self._MainDisplayController__generate_6_char_string('')
                    upper_string += ' '
                    if self._MainDisplayController__parameters and self._MainDisplayController__parameters[strip_index]:
                        if self._MainDisplayController__parameters[strip_index][0]:
                            lower_string += self._MainDisplayController__generate_6_char_string(str(self._MainDisplayController__parameters[strip_index][0]))
                        else:
                            lower_string += self._MainDisplayController__generate_6_char_string('')
                    else:
                        if self._MainDisplayController__channel_strip_strings and self._MainDisplayController__channel_strip_strings[strip_index]:
                            lower_string += self._MainDisplayController__generate_6_char_string(self._MainDisplayController__channel_strip_strings[strip_index])
                        else:
                            lower_string += self._MainDisplayController__generate_6_char_string('')
                    lower_string += ' '
                    strip_index += 1

                display.send_display_string(upper_string, 0, 0)
                if not self._MainDisplayController__meters_enabled:
                    display.send_display_string(lower_string, 1, 0)
            else:
                ascii_message = '< _1234 guck ma #!?:;_ >'
                if not self._MainDisplayController__test:
                    self._MainDisplayController__test = 0
                self._MainDisplayController__test = self._MainDisplayController__test + 1
                if self._MainDisplayController__test > NUM_CHARS_PER_DISPLAY_LINE - len(ascii_message):
                    self._MainDisplayController__test = 0
                self.send_display_string(ascii_message, 0, self._MainDisplayController__test)

    def __generate_6_char_string(self, display_string):
        if not display_string:
            return '      '
        if len(display_string.strip()) > 6:
            if display_string.endswith('dB'):
                if display_string.find('.') != -1:
                    display_string = display_string[:-2]
        if len(display_string) > 6:
            for um in (' ', 'i', 'o', 'u', 'e', 'a'):
                while len(display_string) > 6:
                    if display_string.rfind(um, 1) != -1:
                        um_pos = display_string.rfind(um, 1)
                        display_string = display_string[:um_pos] + display_string[um_pos + 1:]

        else:
            display_string = display_string.center(6)
        ret = ''
        for i in range(6):
            ret += display_string[i]

        return ret