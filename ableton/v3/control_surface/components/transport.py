<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import clamp, listens, move_current_song_time, sign, task
from .. import Component
from ..controls import ButtonControl, EncoderControl, ToggleButtonControl

class TransportComponent(Component):
    arrangement_position_encoder = EncoderControl()
    tempo_coarse_encoder = EncoderControl()
    tempo_fine_encoder = EncoderControl()
    play_button = ButtonControl(color='Transport.PlayOff', on_color='Transport.PlayOn')
    play_toggle_button = ToggleButtonControl(color='Transport.PlayOff',
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/transport.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 8793 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import listens, task
from .. import Component
from ..controls import ButtonControl, ToggleButtonControl

class TransportComponent(Component):
    play_button = ButtonControl(color='Transport.PlayOff', on_color='Transport.PlayOn')
    play_toggle_button = ButtonControl(color='Transport.PlayOff',
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
      on_color='Transport.PlayOn')
    continue_button = ButtonControl(color='Transport.ContinueOff',
      on_color='Transport.ContinueOn')
    stop_button = ButtonControl(color='Transport.StopOff', on_color='Transport.StopOn')
<<<<<<< HEAD
    session_record_button = ButtonControl()
    arrangement_record_button = ToggleButtonControl(color='Transport.ArrangementRecordingOff',
      on_color='Transport.ArrangementRecordingOn')
    arrangement_overdub_button = ToggleButtonControl(color='Transport.OverdubOff',
      on_color='Transport.OverdubOn')
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
=======
    arrangement_record_button = ToggleButtonControl(untoggled_color='Transport.ArrangementRecordingOff',
      toggled_color='Transport.ArrangementRecordingOn')
    session_record_button = ButtonControl()
    arrangement_overdub_button = ToggleButtonControl(untoggled_color='Transport.OverdubOff',
      toggled_color='Transport.OverdubOn')
    capture_midi_button = ButtonControl(color='Transport.CaptureOff',
      on_color='Transport.CaptureOn')
    loop_button = ToggleButtonControl(untoggled_color='Transport.LoopOff',
      toggled_color='Transport.LoopOn')
    metronome_button = ToggleButtonControl(untoggled_color='Transport.MetronomeOff',
      toggled_color='Transport.MetronomeOn')
    punch_in_button = ToggleButtonControl(untoggled_color='Transport.PunchOff',
      toggled_color='Transport.PunchOn')
    punch_out_button = ToggleButtonControl(untoggled_color='Transport.PunchOff',
      toggled_color='Transport.PunchOn')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    tap_tempo_button = ButtonControl(color='Transport.TapTempo',
      pressed_color='Transport.TapTempoPressed')
    nudge_down_button = ButtonControl(color='Transport.Nudge',
      pressed_color='Transport.NudgePressed')
    nudge_up_button = ButtonControl(color='Transport.Nudge',
      pressed_color='Transport.NudgePressed')
<<<<<<< HEAD
    seek_dict = {
      'color': 'Transport.Seek',
      'pressed_color': 'Transport.SeekPressed',
      'repeat': True,
      'delay_time': 0}
=======
    seek_dict = {'color':'Transport.Seek', 
     'pressed_color':'Transport.SeekPressed', 
     'repeat':True, 
     'delay_time':0}
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    rewind_button = ButtonControl(**seek_dict)
    fastforward_button = ButtonControl(**seek_dict)
    prev_cue_button = ButtonControl(color='Transport.CannotJumpToCue',
      on_color='Transport.CanJumpToCue')
    next_cue_button = ButtonControl(color='Transport.CannotJumpToCue',
      on_color='Transport.CanJumpToCue')
    set_cue_button = ButtonControl(color='Transport.SetCue',
      pressed_color='Transport.SetCuePressed')

    def __init__(self, name='Transport', *a, **k):
        (super().__init__)(a, name=name, **k)
        self._view_based_record_button = None
        self._end_undo_step_task = self._tasks.add(task.sequence(task.wait(1.5), task.run(self.song.end_undo_step)))
        self._end_undo_step_task.kill()
        song = self.song
<<<<<<< HEAD
        self.tempo_coarse_encoder.connect_property(song,
          'tempo', transform=(lambda x: clamp(song.tempo + sign(x), 20, 999)
))
        self.tempo_fine_encoder.connect_property(song,
          'tempo', transform=(lambda x: clamp(song.tempo + sign(x) / 10, 20, 999)
))
        self.play_toggle_button.connect_property(song, 'is_playing')
        self.arrangement_record_button.connect_property(song, 'record_mode')
        self.arrangement_overdub_button.connect_property(song, 'arrangement_overdub')
        self.automation_arm_button.connect_property(song, 'session_automation_record')
=======
        self.arrangement_record_button.connect_property(song, 'record_mode')
        self.arrangement_overdub_button.connect_property(song, 'arrangement_overdub')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self.loop_button.connect_property(song, 'loop')
        self.metronome_button.connect_property(song, 'metronome')
        self.punch_in_button.connect_property(song, 'punch_in')
        self.punch_out_button.connect_property(song, 'punch_out')
        self._TransportComponent__on_is_playing_changed.subject = song
        self._TransportComponent__on_is_playing_changed()
        self.register_slot(song, self._update_session_record_button, 'session_record_status')
        self.register_slot(song, self._update_session_record_button, 'session_record')
<<<<<<< HEAD
        self._TransportComponent__on_re_enable_automation_enabled_changed.subject = song
        self._TransportComponent__on_re_enable_automation_enabled_changed()
        self._TransportComponent__on_can_capture_midi_changed.subject = song
=======
        self._TransportComponent__on_can_capture_midi_changed.subject = self.song
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self._TransportComponent__on_can_capture_midi_changed()
        self._TransportComponent__on_can_jump_to_prev_cue_changed.subject = song
        self._TransportComponent__on_can_jump_to_prev_cue_changed()
        self._TransportComponent__on_can_jump_to_next_cue_changed.subject = song
        self._TransportComponent__on_can_jump_to_next_cue_changed()
        self._TransportComponent__on_main_view_changed.subject = self.application.view

    def disconnect(self):
        super().disconnect()
        self._view_based_record_button = None

    def set_view_based_record_button(self, button):
        self._view_based_record_button = button
        if button:
            self.update()
        else:
            self.arrangement_record_button.set_control_element(None)
            self.session_record_button.set_control_element(None)

<<<<<<< HEAD
    @arrangement_position_encoder.value
    def arrangement_position_encoder(self, value, _):
        move_current_song_time(self.song, sign(value))

=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    @play_button.pressed
    def play_button(self, _):
        self.song.start_playing()

<<<<<<< HEAD
=======
    @play_toggle_button.pressed
    def play_toggle_button(self, _):
        self.song.is_playing = not self.song.is_playing

>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    @continue_button.pressed
    def continue_button(self, _):
        self.song.continue_playing()

    @stop_button.pressed
    def stop_button(self, _):
        self.song.stop_playing()

    @session_record_button.pressed
    def session_record_button(self, _):
        self.song.session_record = not self.song.session_record

<<<<<<< HEAD
    @re_enable_automation_button.pressed
    def re_enable_automation_button(self, _):
        if self.song.re_enable_automation_enabled:
            self.song.re_enable_automation()

=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
        except RuntimeError:
            pass

    @tap_tempo_button.pressed
    def tap_tempo_button(self, _):
        if not self._end_undo_step_task.is_running:
            self.song.begin_undo_step()
        self._end_undo_step_task.restart()
        self.song.tap_tempo()

    @nudge_down_button.value
    def nudge_down_button(self, value, _):
        self.song.nudge_down = bool(value)

    @nudge_up_button.value
    def nudge_up_button(self, value, _):
        self.song.nudge_up = bool(value)

    @rewind_button.pressed
    def rewind_button(self, _):
<<<<<<< HEAD
        move_current_song_time(self.song, -1)

    @fastforward_button.pressed
    def fastforward_button(self, _):
        move_current_song_time(self.song, 1)
=======
        if self.rewind_button.is_momentary:
            self._move_current_song_time(-1)
        else:
            self.song.current_song_time = max(0.0, self.song.current_song_time - 1)

    @fastforward_button.pressed
    def fastforward_button(self, _):
        if self.fastforward_button.is_momentary:
            self._move_current_song_time(1)
        else:
            self.song.current_song_time += 1

    def _move_current_song_time(self, delta):
        song = self.song
        song.current_song_time = max(0.0, song.current_song_time + delta)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

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

    @listens('is_playing')
    def __on_is_playing_changed(self):
        is_playing = self.song.is_playing
        self.play_button.is_on = is_playing
<<<<<<< HEAD
        self.continue_button.is_on = not is_playing
        self.stop_button.is_on = is_playing

    @listens('focused_document_view')
    def __on_main_view_changed(self):
        if self._view_based_record_button:
            if self.application.view.focused_document_view == 'Session':
=======
        self.play_toggle_button.is_on = is_playing
        self.continue_button.is_on = not is_playing
        self.stop_button.is_on = is_playing

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        if self._view_based_record_button:
            if self.application.view.is_view_visible('Session'):
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                self.arrangement_record_button.set_control_element(None)
                self.session_record_button.set_control_element(self._view_based_record_button)
                self._update_session_record_button()
            else:
                self.session_record_button.set_control_element(None)
                self.arrangement_record_button.set_control_element(self._view_based_record_button)

<<<<<<< HEAD
    @listens('re_enable_automation_enabled')
    def __on_re_enable_automation_enabled_changed(self):
        self.re_enable_automation_button.enabled = self.song.re_enable_automation_enabled

    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.enabled = self.song.can_capture_midi
=======
    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.is_on = self.song.can_capture_midi
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    @listens('can_jump_to_prev_cue')
    def __on_can_jump_to_prev_cue_changed(self):
        self.prev_cue_button.is_on = self.song.can_jump_to_prev_cue

    @listens('can_jump_to_next_cue')
    def __on_can_jump_to_next_cue_changed(self):
        self.next_cue_button.is_on = self.song.can_jump_to_next_cue

    def update(self):
        super().update()
        self._TransportComponent__on_main_view_changed()
        self._update_session_record_button()

    def _update_session_record_button(self):
        song = self.song
        status = song.session_record_status
        if status == Live.Song.SessionRecordStatus.transition:
<<<<<<< HEAD
            self.session_record_button.color = 'Transport.SessionRecordingTransition'
        else:
            if status == Live.Song.SessionRecordStatus.on or song.session_record:
                self.session_record_button.color = 'Transport.SessionRecordingOn'
            else:
                self.session_record_button.color = 'Transport.SessionRecordingOff'
=======
            self.session_record_button.color = 'Recording.Transition'
        elif status == Live.Song.SessionRecordStatus.on or song.session_record:
            self.session_record_button.color = 'Recording.On'
        else:
            self.session_record_button.color = 'Recording.Off'
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
