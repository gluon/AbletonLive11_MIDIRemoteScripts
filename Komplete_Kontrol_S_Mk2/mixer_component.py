#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Komplete_Kontrol_S_Mk2/mixer_component.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from future.moves.itertools import zip_longest
from functools import partial
from ableton.v2.control_surface.control.control import InputControl
from _Komplete_Kontrol.mixer_component import MixerComponent as MixerComponentBase
from .channel_strip_component import ChannelStripComponent
from .meter_display_element import METERS_PER_SEGMENT

class MixerComponent(MixerComponentBase):
    selection_control = InputControl()
    mute_control = InputControl()
    solo_control = InputControl()

    def set_selected_track_volume_control(self, control):
        self._selected_strip.set_volume_control(control)

    def set_selected_track_pan_control(self, control):
        self._selected_strip.set_pan_control(control)

    def set_selected_track_type_display(self, control):
        self._selected_strip.track_type_display.set_control_element(control)

    def set_selected_track_muted_via_solo_display(self, control):
        self._selected_strip.track_muted_via_solo_display.set_control_element(control)

    def set_track_meter_display(self, display):
        for index, strip in enumerate(self._channel_strips):
            strip.set_meter_display_callback(partial(display.update_meter_display, index * METERS_PER_SEGMENT) if display else None)

    def set_track_arm_displays(self, displays):
        for strip, display in zip_longest(self._channel_strips, displays or []):
            strip.track_arm_display.set_control_element(display)

    @selection_control.value
    def selection_control(self, index, _):
        if index in range(self._provider.num_tracks):
            self._channel_strips[index].select_track()

    @mute_control.value
    def mute_control(self, index, _):
        if index in range(self._provider.num_tracks):
            self._channel_strips[index].mute_track()

    @solo_control.value
    def solo_control(self, index, _):
        if index in range(self._provider.num_tracks):
            self._channel_strips[index].solo_track()
