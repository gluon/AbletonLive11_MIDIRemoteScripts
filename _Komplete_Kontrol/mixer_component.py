# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Komplete_Kontrol/mixer_component.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 2130 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import zip
from future.moves.itertools import zip_longest
import ableton.v2.control_surface.components as MixerComponentBase

class MixerComponent(MixerComponentBase):

    def set_mute_button(self, button):
        self._selected_strip.set_mute_button(button)

    def set_solo_button(self, button):
        self._selected_strip.set_solo_button(button)

    def set_track_name_displays(self, displays):
        for strip, display in zip(self._channel_strips, displays or []):
            display.set_data_sources((strip.track_name_data_source(),))

    def set_track_volume_displays(self, displays):
        for strip, display in zip(self._channel_strips, displays or []):
            display.set_data_sources((strip.track_volume_data_source,))

    def set_track_panning_displays(self, displays):
        for strip, display in zip(self._channel_strips, displays or []):
            display.set_data_sources((strip.track_panning_data_source,))

    def set_track_type_displays(self, displays):
        for strip, display in zip_longest(self._channel_strips, displays or []):
            strip.track_type_display.set_control_element(display)

    def set_track_selection_displays(self, displays):
        for strip, display in zip_longest(self._channel_strips, displays or []):
            strip.track_selection_display.set_control_element(display)

    def set_track_mute_displays(self, displays):
        for strip, display in zip_longest(self._channel_strips, displays or []):
            strip.track_mute_display.set_control_element(display)

    def set_track_solo_displays(self, displays):
        for strip, display in zip_longest(self._channel_strips, displays or []):
            strip.track_solo_display.set_control_element(display)

    def set_track_muted_via_solo_displays(self, displays):
        for strip, display in zip_longest(self._channel_strips, displays or []):
            strip.track_muted_via_solo_display.set_control_element(display)