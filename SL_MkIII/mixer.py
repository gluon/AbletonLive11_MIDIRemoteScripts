# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\mixer.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6233 bytes
from __future__ import absolute_import, print_function, unicode_literals
from future.moves.itertools import zip_longest
from ableton.v2.base import listens, listens_group, liveobj_valid
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v2.control_surface.control import ButtonControl, ColorSysexControl, control_list
from .channel_strip import ChannelStripComponent
from .control import ConfigurableTextDisplayControl, TextDisplayControl
from .elements import SESSION_WIDTH
from .util import color_for_track

class MixerComponent(MixerComponentBase):
    send_up_button = ButtonControl(color='Mixer.Send')
    send_down_button = ButtonControl(color='Mixer.Send')
    pan_value_display = ConfigurableTextDisplayControl(segments=(('', ) * SESSION_WIDTH))
    send_value_display = ConfigurableTextDisplayControl(segments=(('', ) * SESSION_WIDTH))
    mixer_display = TextDisplayControl(segments=('Mixer', ))
    pan_display = TextDisplayControl(segments=('Pan', ))
    send_index_display = ConfigurableTextDisplayControl(segments=('', ))
    send_encoder_color_fields = control_list(ColorSysexControl, SESSION_WIDTH)
    selected_track_color_field = ColorSysexControl()

    def __init__(self, *a, **k):
        (super().__init__)(a, channel_strip_component_type=ChannelStripComponent, **k)
        self._MixerComponent__on_selected_track_changed.subject = self.song.view
        self._MixerComponent__on_selected_track_changed()
        self.pan_value_display.set_data_sources([strip.pan_value_display_data_source for strip in self._channel_strips])
        self.on_send_index_changed()

    @property
    def controlled_tracks(self):
        return self._track_assigner.tracks(self._provider)

    @property
    def controlled_sends(self):
        tracks = self.controlled_tracks
        controlled_sends = [None] * len(tracks)
        send_index = self.send_index
        for index, track in enumerate(tracks):
            if liveobj_valid(track):
                sends = track.mixer_device.sends
                if send_index is not None:
                    if send_index < len(sends):
                        controlled_sends[index] = sends[send_index]

        return controlled_sends

    @send_up_button.pressed
    def send_up_button(self, _):
        self.send_index -= 1

    @send_down_button.pressed
    def send_down_button(self, _):
        self.send_index += 1

    def set_track_names_display(self, display):
        if display:
            display.set_data_sources([strip.track_name_data_source() for strip in self._channel_strips])

    def set_selected_track_name_display(self, display):
        if display:
            display.set_data_sources([self._selected_strip.track_name_data_source()])

    def set_pan_encoder_color_fields(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.pan_encoder_color_field.set_control_element(control)

    def set_track_color_fields(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.track_color_field.set_control_element(control)

    def set_track_selection_fields(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.track_selection_field.set_control_element(control)

    def set_volume_leds(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.volume_led.set_control_element(control)

    def set_monitoring_state_buttons(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.monitoring_state_button.set_control_element(control)

    def on_send_index_changed(self):
        self._update_send_value_subjects()
        self._update_send_navigation_buttons()
        self._update_send_index_display()
        self._update_send_value_display()

    def on_num_sends_changed(self):
        self._update_send_navigation_buttons()
        self._update_send_value_display()

    def _update_send_navigation_buttons(self):
        send_index = self.send_index
        self.send_up_button.enabled = send_index is not None and send_index > 0
        self.send_down_button.enabled = send_index is not None and send_index < self.num_sends - 1

    def _update_send_index_display(self):
        send_index = self.send_index
        self.send_index_display[0] = 'Send ' + chr(send_index + 65) if send_index is not None else ''

    def _update_send_value_display(self):
        for index, send in enumerate(self.controlled_sends):
            self.send_value_display[index] = str(send) if send else ''

    def _update_send_encoder_color_fields(self):
        for index, send in enumerate(self.controlled_sends):
            self.send_encoder_color_fields[index].color = 'Mixer.Send' if send else 'DefaultButton.Disabled'

    def _update_selected_track_color_field(self):
        self.selected_track_color_field.color = color_for_track(self.song.view.selected_track)

    def _update_send_value_subjects(self):
        self._MixerComponent__on_send_value_changed.replace_subjects(self.controlled_sends)

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_selected_strip()
        self._update_selected_track_color_field()
        self._MixerComponent__on_selected_track_color_changed.subject = self.song.view.selected_track

    @listens('color')
    def __on_selected_track_color_changed(self):
        self._update_selected_track_color_field()

    @listens_group('value')
    def __on_send_value_changed(self, _):
        self._update_send_value_display()

    def _reassign_tracks(self):
        super()._reassign_tracks()
        self._update_send_value_subjects()
        self._update_send_value_display()
        self._update_send_encoder_color_fields()