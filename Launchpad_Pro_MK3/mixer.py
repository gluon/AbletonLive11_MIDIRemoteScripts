#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Pro_MK3/mixer.py
from __future__ import absolute_import, print_function, unicode_literals
from future.moves.itertools import zip_longest
from ableton.v2.base import clamp, listens_group, liveobj_valid
from ableton.v2.control_surface.control import control_list, SendValueControl
from novation.fixed_radio_button_group import FixedRadioButtonGroup
from novation.mixer import MixerComponent as MixerComponentBase
from novation.util import get_midi_color_value_for_track
from .control import SendReceiveValueControl
NUM_SENDS = 8
SEND_FADER_BANK = 2

class MixerComponent(MixerComponentBase):
    send_select_buttons = FixedRadioButtonGroup(control_count=8, unchecked_color=u'Mode.Sends.Bank.Available')
    return_track_color_controls = control_list(SendValueControl, control_count=8)
    stop_fader_control = SendReceiveValueControl()

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(*a, **k)
        self.on_send_index_changed()
        self._next_send_index = self.send_index

    def update(self):
        super(MixerComponent, self).update()
        if self.is_enabled():
            self._update_send_control_colors()

    @send_select_buttons.checked
    def send_select_buttons(self, button):
        self.stop_fader_control.send_value(SEND_FADER_BANK)
        self._next_send_index = button.index

    @stop_fader_control.value
    def stop_fader_control(self, value, _):
        self.send_index = self._next_send_index

    def on_num_sends_changed(self):
        self.send_select_buttons.active_control_count = clamp(self.num_sends, 0, NUM_SENDS)
        self._update_send_control_colors()
        self.__on_return_track_color_changed.replace_subjects(self.song.return_tracks[:NUM_SENDS])

    def on_send_index_changed(self):
        if self.send_index is None:
            self.send_select_buttons.active_control_count = 0
        elif self.send_index < self.send_select_buttons.active_control_count:
            self.send_select_buttons[self.send_index].is_checked = True
        self._update_send_control_colors()

    def _update_send_control_colors(self):
        self._update_send_select_button_colors()
        self._update_return_track_color_controls()

    def _update_send_select_button_colors(self):
        for select_button, track in zip_longest(self.send_select_buttons, self.song.return_tracks[:NUM_SENDS]):
            if select_button:
                select_button.checked_color = get_midi_color_value_for_track(track)

    def _update_return_track_color_controls(self):
        value = 0
        if self.send_select_buttons.active_control_count:
            value = self.send_select_buttons[self.send_index].checked_color
        for strip, control in zip_longest(self._channel_strips, self.return_track_color_controls):
            control.value = value if liveobj_valid(strip.track) else 0

    @listens_group(u'color')
    def __on_return_track_color_changed(self, _):
        self._update_send_control_colors()
