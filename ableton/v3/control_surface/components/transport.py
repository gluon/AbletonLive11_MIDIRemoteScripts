# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\transport.py
# Compiled at: 2023-09-14 15:51:08
# Size of source mod 2**32: 11639 bytes
from __future__ import absolute_import, print_function, unicode_literals
from Live.Song import RecordingQuantization
from ...base import clamp, listens, sign, task
from ...live import get_bar_length, move_current_song_time
from .. import Component
from ..controls import ButtonControl, StepEncoderControl, ToggleButtonControl
from ..display import Renderable
from ..skin import OptionalSkinEntry

class TransportComponent(Component, Renderable):
    arrangement_position_encoder = StepEncoderControl(num_steps=64)
    loop_start_encoder = StepEncoderControl(num_steps=64)
    tempo_coarse_encoder = StepEncoderControl(num_steps=64)
    tempo_fine_encoder = StepEncoderControl(num_steps=64)
    play_button = ButtonControl(color='Transport.PlayOff', on_color='Transport.PlayOn')
    play_toggle_button = ToggleButtonControl(color='Transport.PlayOff',
      on_color='Transport.PlayOn')
    play_pause_button = ButtonControl(color='Transport.PlayOff',
      on_color='Transport.PlayOn')
    stop_button = ButtonControl(color='Transport.StopOff',
      on_color='Transport.StopOn',
      pressed_color=(OptionalSkinEntry('Transport.StopPressed')))
    automation_arm_button = ToggleButtonControl(color='Transport.AutomationArmOff',
      on_color='Transport.AutomationArmOn')
    re_enable_automation_button = ButtonControl(color='Transport.CanReEnableAutomation')
    capture_midi_button = ButtonControl(color='Transport.CanCaptureMidi')
    loop_button = ToggleButtonControl(color='Transport.LoopOff',
      on_color='Transport.LoopOn')
    metronome_button = ToggleButtonControl(color='Transport.MetronomeOff',
      on_color='Transport.MetronomeOn')
    punch_in_button = ToggleButtonControl(color='Transport.PunchOff',
      on_color='Transport.PunchOn')
    punch_out_button = ToggleButtonControl(color='Transport.PunchOff',
      on_color='Transport.PunchOn')
    tap_tempo_button = ButtonControl(color='Transport.TapTempo',
      pressed_color='Transport.TapTempoPressed')
    nudge_down_button = ButtonControl(color='Transport.Nudge',
      pressed_color='Transport.NudgePressed')
    nudge_up_button = ButtonControl(color='Transport.Nudge',
      pressed_color='Transport.NudgePressed')
    seek_dict = {
      'color': 'Transport.Seek',
      'pressed_color': 'Transport.SeekPressed',
      'repeat': True,
      'delay_time': 0}
    rewind_button = ButtonControl(**seek_dict)
    fastforward_button = ButtonControl(**seek_dict)
    prev_cue_button = ButtonControl(color='Transport.CannotJumpToCue',
      on_color='Transport.CanJumpToCue')
    next_cue_button = ButtonControl(color='Transport.CannotJumpToCue',
      on_color='Transport.CanJumpToCue')
    set_cue_button = ButtonControl(color='Transport.SetCue',
      pressed_color='Transport.SetCuePressed')
    record_quantize_button = ButtonControl(color='Transport.RecordQuantizeOff',
      on_color='Transport.RecordQuantizeOn')

    def __init__(self, name='Transport', *a, **k):
        (super().__init__)(a, name=name, **k)
        self._end_undo_step_task = self._tasks.add(task.sequence(task.wait(1.5), task.run(self.song.end_undo_step)))
        self._end_undo_step_task.kill()
        song = self.song
        self.loop_start_encoder.connect_property(song,
          'loop_start',
          transform=(lambda x: max(0.0, song.loop_start + get_bar_length() * sign(x))
))
        self.tempo_coarse_encoder.connect_property(song,
          'tempo', transform=(lambda x: clamp(song.tempo + sign(x), 20, 999)
))
        self.tempo_fine_encoder.connect_property(song,
          'tempo', transform=(lambda x: clamp(song.tempo + sign(x) / 10, 20, 999)
))
        self.play_toggle_button.connect_property(song, 'is_playing')
        self.automation_arm_button.connect_property(song, 'session_automation_record')
        self.loop_button.connect_property(song, 'loop')
        self.metronome_button.connect_property(song, 'metronome')
        self.punch_in_button.connect_property(song, 'punch_in')
        self.punch_out_button.connect_property(song, 'punch_out')
        self._TransportComponent__on_is_playing_changed.subject = song
        self._TransportComponent__on_is_playing_changed()
        self._TransportComponent__on_re_enable_automation_enabled_changed.subject = song
        self._TransportComponent__on_re_enable_automation_enabled_changed()
        self._TransportComponent__on_can_capture_midi_changed.subject = song
        self._TransportComponent__on_can_capture_midi_changed()
        self._TransportComponent__on_can_jump_to_prev_cue_changed.subject = song
        self._TransportComponent__on_can_jump_to_prev_cue_changed()
        self._TransportComponent__on_can_jump_to_next_cue_changed.subject = song
        self._TransportComponent__on_can_jump_to_next_cue_changed()
        self._last_record_quantization_value = RecordingQuantization.rec_q_sixtenth
        self._TransportComponent__on_record_quantization_changed.subject = song
        self._TransportComponent__on_record_quantization_changed()

    @arrangement_position_encoder.value
    def arrangement_position_encoder(self, value, _):
        move_current_song_time(self.song, sign(value))

    @metronome_button.pressed
    def metronome_button(self, button):
        self.notify(self.notifications.Transport.metronome, not button.is_on)

    @loop_button.pressed
    def loop_button(self, button):
        self.notify(self.notifications.Transport.loop, not button.is_on)

    @play_button.pressed
    def play_button(self, _):
        self.song.start_playing()

    @play_pause_button.pressed
    def play_pause_button(self, _):
        if self.song.is_playing:
            self.song.stop_playing()
        else:
            self.song.continue_playing()

    @stop_button.pressed
    def stop_button(self, _):
        self.song.stop_playing()

    @re_enable_automation_button.pressed
    def re_enable_automation_button(self, _):
        if self.song.re_enable_automation_enabled:
            self.song.re_enable_automation()

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            initial_tempo = self.song.tempo
            if self.song.can_capture_midi:
                self.song.capture_midi()
                tempo_set_by_capture = self.song.tempo != initial_tempo
                self.notify(self.notifications.Transport.midi_capture, tempo_set_by_capture, self.song.tempo)
        except RuntimeError:
            pass

    @tap_tempo_button.pressed
    def tap_tempo_button(self, _):
        self._trigger_tap_tempo()

    def _trigger_tap_tempo(self):
        if not self._end_undo_step_task.is_running:
            self.song.begin_undo_step()
        self._end_undo_step_task.restart()
        self.song.tap_tempo()

    @tap_tempo_button.released
    def tap_tempo_button(self, _):
        self.notify(self.notifications.Transport.tap_tempo, self.song.tempo)

    @nudge_down_button.value
    def nudge_down_button(self, value, _):
        self.song.nudge_down = bool(value)

    @nudge_up_button.value
    def nudge_up_button(self, value, _):
        self.song.nudge_up = bool(value)

    @rewind_button.pressed
    def rewind_button(self, _):
        move_current_song_time(self.song, -1)

    @fastforward_button.pressed
    def fastforward_button(self, _):
        move_current_song_time(self.song, 1)

    @prev_cue_button.pressed
    def prev_cue_button(self, _):
        if self.song.can_jump_to_prev_cue:
            self.song.jump_to_prev_cue()

    @next_cue_button.pressed
    def next_cue_button(self, _):
        if self.song.can_jump_to_next_cue:
            self.song.jump_to_next_cue()

    @set_cue_button.pressed
    def set_cue_button(self, _):
        self.song.set_or_delete_cue()

    @record_quantize_button.pressed
    def record_quantize_button(self, _):
        self._toggle_record_quantize()

    def _toggle_record_quantize(self):
        self.notify(self.notifications.Transport.record_quantize, not self.record_quantize_button.is_on)
        if self.song.midi_recording_quantization == RecordingQuantization.rec_q_no_q:
            self.song.midi_recording_quantization = self._last_record_quantization_value
        else:
            self.song.midi_recording_quantization = RecordingQuantization.rec_q_no_q

    @listens('is_playing')
    def __on_is_playing_changed(self):
        is_playing = self.song.is_playing
        self.play_button.is_on = is_playing
        self.play_pause_button.is_on = is_playing
        self.stop_button.is_on = is_playing

    @listens('re_enable_automation_enabled')
    def __on_re_enable_automation_enabled_changed(self):
        self.re_enable_automation_button.enabled = self.song.re_enable_automation_enabled

    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.enabled = self.song.can_capture_midi

    @listens('can_jump_to_prev_cue')
    def __on_can_jump_to_prev_cue_changed(self):
        self.prev_cue_button.is_on = self.song.can_jump_to_prev_cue

    @listens('can_jump_to_next_cue')
    def __on_can_jump_to_next_cue_changed(self):
        self.next_cue_button.is_on = self.song.can_jump_to_next_cue

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        quantization_value = self.song.midi_recording_quantization
        quantization_on = quantization_value != RecordingQuantization.rec_q_no_q
        if quantization_on:
            self._last_record_quantization_value = quantization_value
        self.record_quantize_button.is_on = quantization_on