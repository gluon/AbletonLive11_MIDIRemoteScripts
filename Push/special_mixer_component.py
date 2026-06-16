# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\special_mixer_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 7238 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from future.moves.itertools import zip_longest
from ableton.v2.base import listens
from ableton.v2.control_surface import components
from ableton.v2.control_surface.elements import DisplayDataSource
from .special_chan_strip_component import SpecialChanStripComponent

class SpecialMixerComponent(components.MixerComponent):
    num_label_segments = 4

    def __init__(self, *a, **k):
        (super(SpecialMixerComponent, self).__init__)(a, channel_strip_component_type=SpecialChanStripComponent, **k)
        self._pan_send_index = 0
        self._pan_send_controls = None
        self._pan_send_names_display = None
        self._pan_send_values_display = None
        self._pan_send_graphics_display = None
        self._pan_send_toggle_skip = False
        self._selected_track_data_sources = list(map(DisplayDataSource, ('', ) * self.num_label_segments))
        self._selected_track_data_sources[0].set_display_string('Track Selection:')
        self._selected_track_name_data_source = self._selected_track_data_sources[1]
        self._on_selected_track_name_changed.subject = self.song.view
        self._on_track_list_changed.subject = self.song
        self._update_selected_track_name()

    def set_pan_send_toggle(self, toggle):
        self._pan_send_toggle = toggle
        self._on_pan_send_value.subject = toggle
        self._pan_send_toggle_skip = True

    def set_selected_track_name_display(self, display):
        if display:
            display.set_data_sources(self._selected_track_data_sources)

    def set_track_select_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_select_button(button)

    def set_solo_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_solo_button(button)

    def set_mute_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_mute_button(button)

    def set_track_names_display(self, display):
        if display:
            sources = [strip.track_name_data_source() for strip in self._channel_strips]
            display.set_data_sources(sources)

    def set_volume_names_display(self, display):
        self._set_parameter_names_display(display, 0)

    def set_volume_values_display(self, display):
        self._set_parameter_values_display(display, 0)

    def set_volume_graphics_display(self, display):
        self._set_parameter_graphics_display(display, 0)

    def set_volume_controls(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.set_volume_control(control)

    def set_pan_send_names_display(self, display):
        self._normalize_pan_send_index()
        self._pan_send_names_display = display
        self._set_parameter_names_display(display, self._pan_send_index + 1)

    def set_pan_send_values_display(self, display):
        self._normalize_pan_send_index()
        self._pan_send_values_display = display
        self._set_parameter_values_display(display, self._pan_send_index + 1)

    def set_pan_send_graphics_display(self, display):
        self._normalize_pan_send_index()
        self._pan_send_graphics_display = display
        self._set_parameter_graphics_display(display, self._pan_send_index + 1)

    def set_pan_send_controls(self, controls):
        self.set_send_controls(None)
        self.set_pan_controls(None)
        self._pan_send_controls = controls
        self._normalize_pan_send_index()
        if self._pan_send_index == 0:
            self.set_pan_controls(controls)
        else:
            sends = self._pan_send_index - 1
            self.set_send_controls([(None, ) * sends + (ctl,) for ctl in controls or []])

    @listens('visible_tracks')
    def _on_track_list_changed(self):
        self._update_pan_sends()

    def set_pan_controls(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.set_pan_control(control)

    def set_send_controls(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.set_send_controls(control)

    def _set_parameter_names_display(self, display, parameter):
        if display:
            sources = [strip.track_parameter_name_sources(parameter) for strip in self._channel_strips]
            display.set_data_sources(sources)

    def _set_parameter_values_display(self, display, parameter):
        if display:
            sources = [strip.track_parameter_data_sources(parameter) for strip in self._channel_strips]
            display.set_data_sources(sources)

    def _set_parameter_graphics_display(self, display, parameter):
        if display:
            sources = [strip.track_parameter_graphic_sources(parameter) for strip in self._channel_strips]
            display.set_data_sources(sources)

    @listens('value')
    def _on_pan_send_value(self, value):
        if not self._pan_send_toggle_skip or self.is_enabled():
            if not (value or self._pan_send_toggle.is_momentary()):
                self._pan_send_index += 1
                self._update_pan_sends()
            self._pan_send_toggle_skip = False

    def _update_pan_sends(self):
        self.set_pan_send_controls(self._pan_send_controls)
        self.set_pan_send_names_display(self._pan_send_names_display)
        self.set_pan_send_graphics_display(self._pan_send_graphics_display)

    def _normalize_pan_send_index(self):
        if len(self.song.tracks) == 0 or self._pan_send_index > len(self.song.tracks[0].mixer_device.sends):
            self._pan_send_index = 0

    @listens('selected_track.name')
    def _on_selected_track_name_changed(self):
        self._update_selected_track_name()

    def _update_selected_track_name(self):
        selected = self.song.view.selected_track
        self._selected_track_name_data_source.set_display_string(selected.name)