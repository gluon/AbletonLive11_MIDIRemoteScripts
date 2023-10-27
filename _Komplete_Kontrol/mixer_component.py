# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\mixer_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2178 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import zip
from future.moves.itertools import zip_longest
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase

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