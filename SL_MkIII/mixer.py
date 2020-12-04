#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/mixer.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import chr
from future.moves.itertools import zip_longest
from ableton.v2.base import liveobj_valid, listens, listens_group
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v2.control_surface.control import ButtonControl, ColorSysexControl, control_list
from .channel_strip import ChannelStripComponent
from .control import ConfigurableTextDisplayControl, TextDisplayControl
from .elements import SESSION_WIDTH
from .util import color_for_track

class MixerComponent(MixerComponentBase):
    send_up_button = ButtonControl(color=u'Mixer.Send')
    send_down_button = ButtonControl(color=u'Mixer.Send')
    pan_value_display = ConfigurableTextDisplayControl(segments=(u'',) * SESSION_WIDTH)
    send_value_display = ConfigurableTextDisplayControl(segments=(u'',) * SESSION_WIDTH)
    mixer_display = TextDisplayControl(segments=(u'Mixer',))
    pan_display = TextDisplayControl(segments=(u'Pan',))
    send_index_display = ConfigurableTextDisplayControl(segments=(u'',))
    send_encoder_color_fields = control_list(ColorSysexControl, SESSION_WIDTH)
    selected_track_color_field = ColorSysexControl()

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(channel_strip_component_type=ChannelStripComponent, *a, **k)
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()
        self.pan_value_display.set_data_sources([ strip.pan_value_display_data_source for strip in self._channel_strips ])
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
                if send_index != None and send_index < len(sends):
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
            display.set_data_sources([ strip.track_name_data_source() for strip in self._channel_strips ])

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
        self.send_up_button.enabled = send_index != None and send_index > 0
        self.send_down_button.enabled = send_index != None and send_index < self.num_sends - 1

    def _update_send_index_display(self):
        send_index = self.send_index
        self.send_index_display[0] = u'Send ' + chr(send_index + 65) if send_index != None else u''

    def _update_send_value_display(self):
        for index, send in enumerate(self.controlled_sends):
            self.send_value_display[index] = str(send) if send else u''

    def _update_send_encoder_color_fields(self):
        for index, send in enumerate(self.controlled_sends):
            self.send_encoder_color_fields[index].color = u'Mixer.Send' if send else u'DefaultButton.Disabled'

    def _update_selected_track_color_field(self):
        self.selected_track_color_field.color = color_for_track(self.song.view.selected_track)

    def _update_send_value_subjects(self):
        self.__on_send_value_changed.replace_subjects(self.controlled_sends)

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._update_selected_strip()
        self._update_selected_track_color_field()
        self.__on_selected_track_color_changed.subject = self.song.view.selected_track

    @listens(u'color')
    def __on_selected_track_color_changed(self):
        self._update_selected_track_color_field()

    @listens_group(u'value')
    def __on_send_value_changed(self, _):
        self._update_send_value_display()

    def _reassign_tracks(self):
        super(MixerComponent, self)._reassign_tracks()
        self._update_send_value_subjects()
        self._update_send_value_display()
        self._update_send_encoder_color_fields()
