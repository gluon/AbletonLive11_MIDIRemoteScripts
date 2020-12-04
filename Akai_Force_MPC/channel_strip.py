#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/channel_strip.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import range
import re
from itertools import count
from ableton.v2.base import clamp, index_if, listens, listens_group, liveobj_valid
from ableton.v2.control_surface import PercussionInstrumentFinder
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v2.control_surface.control import ButtonControl, SendValueControl, TextDisplayControl, control_list
from ableton.v2.control_surface.elements import Color, DisplayDataSource
from .control import SendReceiveValueControl
from .elements import MAX_NUM_SENDS
from .skin import LIVE_COLOR_TABLE_INDEX_OFFSET
DIM_FACTOR = 0.2

def dim_color(color):
    return Color(tuple([ int(channel * DIM_FACTOR) for channel in color.midi_value ]))


NO_TRACK = 0
EMPTY_MIDI_TRACK = 1
DRUM_TRACK = 2
MELODIC_TRACK = 4
AUDIO_TRACK = 6
GROUP_TRACK = 7
RETURN_TRACK = 8
MASTER_TRACK = 9
OLED_DISPLAY_OFF = 0
OLED_DISPLAY_UNIPOLAR = 1
CROSSFADE_ASSIGN_OFF = 0
CROSSFADE_ASSIGN_A = 1
CROSSFADE_ASSIGN_B = 2
LIVE_CROSSFADE_ASSIGN_VALUES = (CROSSFADE_ASSIGN_A, CROSSFADE_ASSIGN_OFF, CROSSFADE_ASSIGN_B)
float_number_pattern = re.compile(u'-?\\d+\\.\\d+ ')

def format_volume_value_string(s):
    float_number_match = re.match(float_number_pattern, s)
    if float_number_match:
        return u'{0:.1f} dB'.format(float(float_number_match.group(0)))
    else:
        return s


def force_to_live_crossfade_assign_value(value):
    return index_if(lambda v: v == value, LIVE_CROSSFADE_ASSIGN_VALUES)


def meter_value_to_midi_value(value):
    return clamp(int(value * 127), 0, 127)


class ChannelStripComponent(ChannelStripComponentBase):
    track_type_control = SendValueControl()
    oled_display_style_control = SendValueControl()
    arm_color_control = ButtonControl()
    mute_color_control = ButtonControl()
    solo_color_control = ButtonControl()
    output_meter_left_control = SendValueControl()
    output_meter_right_control = SendValueControl()
    track_color_control = ButtonControl()
    physical_track_color_control = ButtonControl()
    volume_touch_control = ButtonControl()
    solo_mute_button = ButtonControl()
    crossfade_assign_control = SendReceiveValueControl()
    assign_a_button = ButtonControl()
    assign_b_button = ButtonControl()
    assign_a_color_control = ButtonControl()
    assign_b_color_control = ButtonControl()
    volume_value_display = TextDisplayControl()
    pan_value_display = TextDisplayControl()
    send_value_displays = control_list(TextDisplayControl, MAX_NUM_SENDS)
    mpc_mute_button = ButtonControl()

    def __init__(self, *a, **k):
        self._oled_display_track_name_data_source = DisplayDataSource()
        self._oled_display_volume_value_data_source = DisplayDataSource()
        self._track_name_or_volume_value_display = None
        self._drum_group_finder = None
        super(ChannelStripComponent, self).__init__(*a, **k)
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()
        self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=self.track))

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        self._drum_group_finder.device_parent = track
        self.__on_drum_group_found.subject = self._drum_group_finder
        self.__on_drum_group_found()
        self._update_listeners()
        self._update_controls()

    def set_volume_control(self, control):
        super(ChannelStripComponent, self).set_volume_control(control)
        self.volume_touch_control.set_control_element(control.touch_element if control else None)

    def set_track_name_display(self, display):
        if display:
            display.set_data_sources([self.track_name_data_source()])

    def set_track_name_or_volume_value_display(self, display):
        self._track_name_or_volume_value_display = display
        self._update_track_name_or_volume_value_display()

    def set_send_value_displays(self, displays):
        self.send_value_displays.set_control_element(displays)

    @volume_touch_control.pressed
    def volume_touch_control(self, _):
        self._update_track_name_or_volume_value_display()

    @volume_touch_control.released
    def volume_touch_control(self, _):
        self._update_track_name_or_volume_value_display()

    @crossfade_assign_control.value
    def crossfade_assign_control(self, value, _):
        value_to_set = force_to_live_crossfade_assign_value(value)
        if value_to_set < len(LIVE_CROSSFADE_ASSIGN_VALUES) and self._track_has_visible_crossfade_assignment_buttons():
            self.track.mixer_device.crossfade_assign = value_to_set

    @assign_a_button.pressed
    def assign_a_button(self, _):
        self._toggle_crossfade_assign(force_to_live_crossfade_assign_value(CROSSFADE_ASSIGN_A))

    @assign_b_button.pressed
    def assign_b_button(self, _):
        self._toggle_crossfade_assign(force_to_live_crossfade_assign_value(CROSSFADE_ASSIGN_B))

    @mpc_mute_button.pressed
    def mpc_mute_button(self, _):
        track = self.track
        if liveobj_valid(track) and track != self.song.master_track:
            track.mute = not track.mute

    def _on_select_button_pressed_delayed(self, _):
        if self.track.is_foldable:
            self.track.fold_state = not self.track.fold_state

    @listens(u'has_audio_output')
    def __on_has_audio_output_changed(self):
        self._update_output_meter_listeners()
        self._update_track_type_control()
        self._update_oled_display_style_control()
        self._update_crossfade_assignment_control()
        self._update_crossfade_assign_color_controls()

    def _update_output_meter_listeners(self):
        track = self.track
        subject = track if liveobj_valid(track) and track.has_audio_output else None
        self.__on_output_meter_left_changed.subject = subject
        self.__on_output_meter_right_changed.subject = subject
        if liveobj_valid(subject):
            self.__on_output_meter_left_changed()
            self.__on_output_meter_right_changed()
        else:
            self._reset_output_meter_controls()

    def _on_arm_changed(self):
        super(ChannelStripComponent, self)._on_arm_changed()
        self._update_arm_color_control()

    def _on_mute_changed(self):
        self._update_mute_color_controls()

    def _on_solo_changed(self):
        super(ChannelStripComponent, self)._on_solo_changed()
        self._update_solo_color_control()

    def _on_cf_assign_changed(self):
        super(ChannelStripComponent, self)._on_cf_assign_changed()
        self._update_crossfade_assignment_control()
        self._update_crossfade_assign_color_controls()

    def _on_sends_changed(self):
        super(ChannelStripComponent, self)._on_sends_changed()
        self._update_listeners()
        self._update_controls()

    @listens(u'output_meter_left')
    def __on_output_meter_left_changed(self):
        self.output_meter_left_control.value = meter_value_to_midi_value(self.track.output_meter_left)

    @listens(u'output_meter_right')
    def __on_output_meter_right_changed(self):
        self.output_meter_right_control.value = meter_value_to_midi_value(self.track.output_meter_right)

    @listens(u'color')
    def __on_track_color_changed(self):
        self._update_track_color_control()

    @listens(u'value')
    def __on_volume_changed(self):
        track = self.track
        value_string = format_volume_value_string(str(track.mixer_device.volume) if liveobj_valid(track) and track.has_audio_output else u'')
        self._oled_display_volume_value_data_source.set_display_string(value_string)
        self.volume_value_display[0] = value_string

    @listens(u'value')
    def __on_pan_changed(self):
        track = self.track
        self.pan_value_display[0] = str(track.mixer_device.panning) if liveobj_valid(track) and track.has_audio_output else u''

    @listens_group(u'value')
    def __on_send_value_changed(self, send_index):
        self._update_send_value_display(send_index)

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._update_select_button()
        self._update_track_color_control()

    @listens(u'muted_via_solo')
    def __on_muted_via_solo_changed(self):
        self.solo_mute_button.color = u'DefaultButton.On' if liveobj_valid(self.track) and self.track != self.song.master_track and self.track.muted_via_solo else u'DefaultButton.Off'

    @listens(u'instrument')
    def __on_drum_group_found(self):
        self._update_track_type_control()

    def _update_listeners(self):
        track = self.track
        self.__on_has_audio_output_changed.subject = track
        self.__on_has_audio_output_changed()
        self.__on_track_color_changed.subject = track
        self.__on_track_color_changed()
        self.__on_volume_changed.subject = track.mixer_device.volume if liveobj_valid(track) else None
        self.__on_volume_changed()
        self.__on_muted_via_solo_changed.subject = track
        self.__on_muted_via_solo_changed()
        self.__on_pan_changed.subject = track.mixer_device.panning if liveobj_valid(track) else None
        self.__on_pan_changed()
        track = self.track
        self.__on_send_value_changed.replace_subjects(track.mixer_device.sends if liveobj_valid(track) else [], count())

    def _update_controls(self):
        self._update_track_type_control()
        self._update_oled_display_style_control()
        for send_index in range(MAX_NUM_SENDS):
            self._update_send_value_display(send_index)

    def _update_track_type_control(self):
        track_type = NO_TRACK
        track = self.track
        if liveobj_valid(track):
            if track == self.song.master_track:
                track_type = MASTER_TRACK
            elif track in self.song.return_tracks:
                track_type = RETURN_TRACK
            elif track.is_foldable:
                track_type = GROUP_TRACK
            elif track.has_midi_input:
                if self._drum_group_finder is not None and liveobj_valid(self._drum_group_finder.drum_group):
                    track_type = DRUM_TRACK
                elif track.has_audio_output:
                    track_type = MELODIC_TRACK
                else:
                    track_type = EMPTY_MIDI_TRACK
            elif track.has_audio_output:
                track_type = AUDIO_TRACK
        self.track_type_control.value = track_type

    def _update_crossfade_assignment_control(self):
        self.crossfade_assign_control.value = LIVE_CROSSFADE_ASSIGN_VALUES[self.track.mixer_device.crossfade_assign] if self._track_has_visible_crossfade_assignment_buttons() else CROSSFADE_ASSIGN_OFF

    def _update_crossfade_assign_color_controls(self):
        off_color = u'DefaultButton.Off'
        track = self.track
        assign_a_control_color = off_color
        assign_b_control_color = off_color
        if self._track_has_visible_crossfade_assignment_buttons():
            mixer_device = track.mixer_device
            assign_a_control_color = u'Mixer.CrossfadeAssignA' if mixer_device.crossfade_assign == force_to_live_crossfade_assign_value(CROSSFADE_ASSIGN_A) else off_color
            assign_b_control_color = u'Mixer.CrossfadeAssignB' if mixer_device.crossfade_assign == force_to_live_crossfade_assign_value(CROSSFADE_ASSIGN_B) else off_color
        self.assign_a_color_control.color = assign_a_control_color
        self.assign_b_color_control.color = assign_b_control_color

    def _update_track_name_data_source(self):
        super(ChannelStripComponent, self)._update_track_name_data_source()
        self._oled_display_track_name_data_source.set_display_string(self._track.name if liveobj_valid(self._track) else u' - ')

    def _update_arm_color_control(self):
        color = u'Mixer.ArmOff'
        track = self.track
        if liveobj_valid(track) and track in self.song.tracks and track.can_be_armed and track.arm:
            color = u'Mixer.ArmOn'
        self.arm_color_control.color = color

    def _update_mute_color_controls(self):
        mute_color_control_color = u'Mixer.MuteOff'
        mute_button_color = u'Mixer.MuteOn'
        track = self.track
        if liveobj_valid(track) and (track == self.song.master_track or not track.mute):
            mute_color_control_color = u'Mixer.MuteOn'
            mute_button_color = u'Mixer.MuteOff'
        self.mute_color_control.color = mute_color_control_color
        self.mpc_mute_button.color = mute_color_control_color
        if self._mute_button:
            self._mute_button.set_light(mute_button_color)

    def _update_solo_color_control(self):
        color = u'Mixer.SoloOff'
        track = self.track
        if liveobj_valid(track) and track != self.song.master_track and track.solo:
            color = u'Mixer.SoloOn'
        self.solo_color_control.color = color

    def _update_track_color_control(self):
        color_to_send = u'DefaultButton.Off'
        selected_color_to_send = None
        track = self.track
        if liveobj_valid(track) and track.color_index != None:
            color_to_send = track.color_index + LIVE_COLOR_TABLE_INDEX_OFFSET
            if track == self.song.view.selected_track:
                selected_color_to_send = u'DefaultButton.On'
        self.track_color_control.color = color_to_send
        self.physical_track_color_control.color = selected_color_to_send or color_to_send

    def _update_oled_display_style_control(self):
        value_to_send = OLED_DISPLAY_OFF
        track = self.track
        if liveobj_valid(track) and track.has_audio_output:
            value_to_send = OLED_DISPLAY_UNIPOLAR
        self.oled_display_style_control.value = value_to_send

    def _update_track_name_or_volume_value_display(self):
        if self._track_name_or_volume_value_display:
            self._track_name_or_volume_value_display.set_data_sources([self._oled_display_volume_value_data_source if self.volume_touch_control.is_pressed else self._oled_display_track_name_data_source])

    def _update_send_value_display(self, index):
        if index < MAX_NUM_SENDS:
            value_to_send = u''
            track = self.track
            if liveobj_valid(track):
                sends = track.mixer_device.sends
                if index < len(sends):
                    value_to_send = str(sends[index])
            self.send_value_displays[index][0] = value_to_send

    def _reset_output_meter_controls(self):
        self.output_meter_left_control.value = 0
        self.output_meter_right_control.value = 0

    def _track_has_visible_crossfade_assignment_buttons(self):
        track = self.track
        return liveobj_valid(track) and track != self.song.master_track and track.has_audio_output

    def _toggle_crossfade_assign(self, value):
        track = self.track
        if self._track_has_visible_crossfade_assignment_buttons():
            mixer_device = track.mixer_device
            mixer_device.crossfade_assign = force_to_live_crossfade_assign_value(CROSSFADE_ASSIGN_OFF) if mixer_device.crossfade_assign == value else value
