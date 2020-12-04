#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/channel_strip.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import str
from past.utils import old_div
import Live
from ableton.v2.base import clamp, listens, liveobj_valid, old_round
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v2.control_surface.elements import DisplayDataSource, SysexRGBColor
from ableton.v2.control_surface.control import ButtonControl, ColorSysexControl
from .control import BinaryControl
from .messenger import Messenger
from .parameter_mapping_sensitivities import CONTINUOUS_MAPPING_SENSITIVITY
from .util import color_for_track, convert_parameter_value_to_midi_value, normalized_parameter_value

def hex_to_channels(color_in_hex):
    return ((color_in_hex & 16711680) >> 16, (color_in_hex & 65280) >> 8, color_in_hex & 255)


monitoring_states = Live.Track.Track.monitoring_states
MONITORING_STATES_TO_STR = {monitoring_states.IN: u'In',
 monitoring_states.AUTO: u'Auto',
 monitoring_states.OFF: u'Off'}

def has_monitoring_state(track):
    return liveobj_valid(track) and track.can_be_armed


class ChannelStripComponent(ChannelStripComponentBase, Messenger):
    empty_color = u'DefaultButton.Disabled'
    monitoring_state_button = ButtonControl()
    pan_encoder_color_field = ColorSysexControl()
    track_color_field = ColorSysexControl()
    volume_led = ColorSysexControl()
    track_selection_field = BinaryControl()

    def __init__(self, *a, **k):
        super(ChannelStripComponent, self).__init__(*a, **k)
        self._pan_value_display_data_source = DisplayDataSource()
        self.__on_selected_track_changed.subject = self.song.view

    @property
    def pan_value_display_data_source(self):
        return self._pan_value_display_data_source

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        self._update_pan_encoder_color_field()
        self._update_track_selection_field()
        self._update_listeners()

    def set_volume_control(self, control):
        super(ChannelStripComponent, self).set_volume_control(control)
        self.__on_volume_control_value_received.subject = control

    def set_pan_control(self, control):
        if control != None:
            control.mapping_sensitivity = CONTINUOUS_MAPPING_SENSITIVITY
        super(ChannelStripComponent, self).set_pan_control(control)

    def set_send_controls(self, controls):
        for control in controls or []:
            if control != None:
                control.mapping_sensitivity = CONTINUOUS_MAPPING_SENSITIVITY

        super(ChannelStripComponent, self).set_send_controls(controls)

    @monitoring_state_button.pressed
    def monitoring_state_button(self, _):
        if has_monitoring_state(self.track):
            self.track.current_monitoring_state = (self.track.current_monitoring_state + 1) % len(monitoring_states.values)
            self._message_monitoring_state()

    def _message_monitoring_state(self):
        track = self.track
        self.message(track.name, u'Monitor {}'.format(MONITORING_STATES_TO_STR[track.current_monitoring_state]))

    def _update_monitoring_state_button(self):
        color = self.empty_color
        if liveobj_valid(self.track):
            if has_monitoring_state(self.track):
                color = u'Monitor.{}'.format(MONITORING_STATES_TO_STR[self.track.current_monitoring_state])
            else:
                color = u'Monitor.Disabled'
        self.monitoring_state_button.color = color

    def _update_volume_led(self):
        track = self.track
        value = (0, 0, 0)
        if liveobj_valid(track):
            value = tuple([ clamp(int(old_round(old_div(channel * normalized_parameter_value(track.mixer_device.volume), 2))), 0, 127) for channel in hex_to_channels(track.color) ])
        self.volume_led.color = SysexRGBColor(value)

    def _message_volume_value(self):
        track = self.track
        if liveobj_valid(track):
            self.message(track.name, str(track.mixer_device.volume))

    def _update_pan_encoder_color_field(self):
        self.pan_encoder_color_field.color = u'Mixer.Pan' if liveobj_valid(self.track) else u'DefaultButton.Disabled'

    def _update_pan_value_display(self):
        track = self.track
        self.pan_value_display_data_source.set_display_string(str(track.mixer_device.panning) if liveobj_valid(track) else u'')

    def _update_track_color_field(self):
        self.track_color_field.color = color_for_track(self.track)

    def _update_select_button(self):
        track = self.track
        color = u'DefaultButton.Disabled'
        if liveobj_valid(track):
            if track == self.song.view.selected_track:
                color = color_for_track(track)
            else:
                color = u'Mixer.TrackSelect'
        self.select_button.color = color

    def _update_track_selection_field(self):
        self.track_selection_field.is_on = self.track == self.song.view.selected_track

    @listens(u'current_monitoring_state')
    def __on_track_monitoring_state_changed(self):
        self._update_monitoring_state_button()

    @listens(u'value')
    def __on_volume_changed(self):
        self._update_volume_led()

    @listens(u'value')
    def __on_pan_changed(self):
        self._update_pan_value_display()

    @listens(u'color')
    def __on_track_color_changed(self):
        self._update_track_color_field()
        self._update_select_button()
        self._update_volume_led()

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._update_select_button()
        self._update_track_selection_field()

    @listens(u'value')
    def __on_volume_control_value_received(self, _):
        self._message_volume_value()

    def _update_listeners(self):
        track = self.track
        self.__on_track_monitoring_state_changed.subject = track
        self.__on_track_monitoring_state_changed()
        self.__on_volume_changed.subject = track.mixer_device.volume if liveobj_valid(track) else None
        self.__on_volume_changed()
        self.__on_pan_changed.subject = track.mixer_device.panning if liveobj_valid(track) else None
        self.__on_pan_changed()
        self.__on_track_color_changed.subject = track if liveobj_valid(track) else None
        self.__on_track_color_changed()
