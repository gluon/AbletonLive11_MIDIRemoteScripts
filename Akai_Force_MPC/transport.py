#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/transport.py
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
import Live
from ableton.v2.base import clamp, listens, sign
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, ColorSysexControl, EncoderControl, InputControl, RadioButtonControl, TextDisplayControl, ToggleButtonControl, control_list
from .control import SendReceiveValueControl
TEMPO_MIN = 20.0
TEMPO_MAX = 999.0
Quantization = Live.Song.Quantization
RADIO_BUTTON_GROUP_QUANTIZATION_VALUES = [Quantization.q_no_q,
 Quantization.q_8_bars,
 Quantization.q_4_bars,
 Quantization.q_2_bars,
 Quantization.q_bar,
 Quantization.q_quarter,
 Quantization.q_eight,
 Quantization.q_sixtenth]

def is_valid_launch_quantize_value(value):
    return Quantization.q_no_q <= value <= Quantization.q_thirtytwoth


def num_beats_in_bar(song):
    return old_div(4.0, song.signature_denominator) * song.signature_numerator


def format_beat_time(beat_time):
    return u'{}:{}:{}'.format(beat_time.bars, beat_time.beats, beat_time.sub_division)


class TransportComponent(TransportComponentBase):
    tempo_control = InputControl()
    tempo_display = TextDisplayControl()
    play_button = ButtonControl()
    stop_button = ButtonControl()
    shift_button = ButtonControl()
    tui_metronome_button = ToggleButtonControl()
    metronome_color_control = ButtonControl()
    follow_song_button = ButtonControl()
    clip_trigger_quantization_control = SendReceiveValueControl()
    clip_trigger_quantization_button_row = control_list(RadioButtonControl, len(RADIO_BUTTON_GROUP_QUANTIZATION_VALUES))
    clip_trigger_quantization_color_controls = control_list(ColorSysexControl, len(RADIO_BUTTON_GROUP_QUANTIZATION_VALUES))
    jump_backward_button = ButtonControl()
    jump_forward_button = ButtonControl()
    loop_start_display = TextDisplayControl()
    loop_length_display = TextDisplayControl()
    arrangement_position_display = TextDisplayControl()
    arrangement_position_control = EncoderControl()
    loop_start_control = EncoderControl()
    loop_length_control = EncoderControl()
    tui_arrangement_record_button = ToggleButtonControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        song = self.song
        self._cached_num_beats_in_bar = num_beats_in_bar(song)
        self.__on_song_tempo_changed.subject = song
        self.__on_song_tempo_changed()
        self.__on_metronome_changed.subject = song
        self.__on_metronome_changed()
        self.__on_clip_trigger_quantization_changed.subject = song
        self.__on_clip_trigger_quantization_changed()
        self.__on_follow_song_changed.subject = song.view
        self.__on_follow_song_changed()
        self.__on_signature_numerator_changed.subject = song
        self.__on_signature_denominator_changed.subject = song
        self.__on_loop_start_changed.subject = song
        self.__on_loop_start_changed()
        self.__on_loop_length_changed.subject = song
        self.__on_loop_length_changed()
        self.__on_arrangement_position_changed.subject = song
        self.__on_arrangement_position_changed()
        self.__on_record_mode_changed.subject = song
        self.__on_record_mode_changed()

    def set_tempo_control(self, control):
        self.tempo_control.set_control_element(control)

    @listens(u'tempo')
    def __on_song_tempo_changed(self):
        self.tempo_display[0] = u'{0:.2f}'.format(self.song.tempo)

    @tempo_control.value
    def tempo_control(self, value, _):
        self.song.tempo = clamp(float(u''.join(map(chr, value[2:]))), TEMPO_MIN, TEMPO_MAX)

    @play_button.pressed
    def play_button(self, _):
        song = self.song
        song.is_playing = not song.is_playing

    @stop_button.pressed
    def stop_button(self, _):
        self.song.stop_playing()
        if self.shift_button.is_pressed:
            self.song.current_song_time = 0.0

    @tui_metronome_button.toggled
    def tui_metronome_button(self, toggled, _):
        self.song.metronome = toggled

    @follow_song_button.pressed
    def follow_song_button(self, _):
        view = self.song.view
        view.follow_song = not view.follow_song

    @clip_trigger_quantization_control.value
    def clip_trigger_quantization_control(self, value, _):
        if is_valid_launch_quantize_value(value):
            self.song.clip_trigger_quantization = value

    @clip_trigger_quantization_button_row.checked
    def clip_trigger_quantization_button_row(self, button):
        self.song.clip_trigger_quantization = RADIO_BUTTON_GROUP_QUANTIZATION_VALUES[button.index]

    def _apply_value_to_arrangement_property(self, property_name, value):
        factor = 0.25 if self.shift_button.is_pressed else 1.0
        delta = factor * sign(value)
        old_value = getattr(self.song, property_name)
        setattr(self.song, property_name, max(0.0, old_value + delta))

    @arrangement_position_control.value
    def arrangement_position_control(self, value, _):
        self._apply_value_to_arrangement_property(u'current_song_time', value)

    @loop_start_control.value
    def loop_start_control(self, value, _):
        self._apply_value_to_arrangement_property(u'loop_start', value)

    @loop_length_control.value
    def loop_length_control(self, value, _):
        self._apply_value_to_arrangement_property(u'loop_length', value)

    @jump_backward_button.pressed
    def jump_backward_button(self, _):
        self.song.jump_by(self._cached_num_beats_in_bar * -1)

    @jump_forward_button.pressed
    def jump_forward_button(self, _):
        self.song.jump_by(self._cached_num_beats_in_bar)

    @tui_arrangement_record_button.toggled
    def tui_arrangement_record_button(self, toggled, _):
        self.song.record_mode = toggled

    def _update_button_states(self):
        self._update_play_button_color()
        self._update_continue_playing_button_color()
        self._update_stop_button_color()

    def _update_play_button_color(self):
        raise NotImplementedError

    def _update_continue_playing_button_color(self):
        self.continue_playing_button.color = u'Transport.PlayOn' if self.song.is_playing else u'Transport.PlayOff'

    def _update_stop_button_color(self):
        self.stop_button.color = u'Transport.StopOff' if self.song.is_playing else u'Transport.StopOn'

    @listens(u'metronome')
    def __on_metronome_changed(self):
        self._update_tui_metronome_button()
        self._update_metronome_color_control()

    @listens(u'follow_song')
    def __on_follow_song_changed(self):
        self.follow_song_button.color = u'DefaultButton.On' if self.song.view.follow_song else u'DefaultButton.Off'

    @listens(u'clip_trigger_quantization')
    def __on_clip_trigger_quantization_changed(self):
        self._update_clip_trigger_quantization_control()
        self._update_clip_trigger_quantization_color_controls()

    @listens(u'signature_numerator')
    def __on_signature_numerator_changed(self):
        self._cached_num_beats_in_bar = num_beats_in_bar(self.song)

    @listens(u'signature_denominator')
    def __on_signature_denominator_changed(self):
        self._cached_num_beats_in_bar = num_beats_in_bar(self.song)

    def _update_clip_trigger_quantization_control(self):
        self.clip_trigger_quantization_control.value = int(self.song.clip_trigger_quantization)

    def _update_clip_trigger_quantization_color_controls(self):
        quantization = self.song.clip_trigger_quantization
        for index, control in enumerate(self.clip_trigger_quantization_color_controls):
            control.color = u'DefaultButton.On' if RADIO_BUTTON_GROUP_QUANTIZATION_VALUES[index] == quantization else u'DefaultButton.Off'

    def _update_tui_metronome_button(self):
        self.tui_metronome_button.is_toggled = self.song.metronome

    def _update_metronome_color_control(self):
        self.metronome_color_control.color = u'Transport.MetronomeOn' if self.song.metronome else u'Transport.MetronomeOff'

    def _update_tui_arrangement_record_button(self):
        self.tui_arrangement_record_button.is_toggled = self.song.record_mode

    @listens(u'loop_start')
    def __on_loop_start_changed(self):
        loop_start_time = self.song.get_beats_loop_start()
        self.loop_start_display[0] = format_beat_time(loop_start_time)

    @listens(u'loop_length')
    def __on_loop_length_changed(self):
        loop_length_time = self.song.get_beats_loop_length()
        self.loop_length_display[0] = format_beat_time(loop_length_time)

    @listens(u'current_song_time')
    def __on_arrangement_position_changed(self):
        song_time = self.song.get_current_beats_song_time()
        self.arrangement_position_display[0] = format_beat_time(song_time)

    @listens(u'record_mode')
    def __on_record_mode_changed(self):
        self._update_tui_arrangement_record_button()


class ForceTransportComponent(TransportComponent):

    def _update_play_button_color(self):
        self.play_button.color = u'Transport.PlayOn' if self.song.is_playing else u'Transport.PlayOff'


class MPCTransportComponent(TransportComponent):

    def __init__(self, *a, **k):
        super(MPCTransportComponent, self).__init__(*a, **k)
        self.play_button.color = u'Transport.PlayOff'
        self.play_button.pressed_color = u'Transport.PlayOn'

    def _update_play_button_color(self):
        pass
