# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\recording.py
# Compiled at: 2023-09-13 04:24:51
# Size of source mod 2**32: 9180 bytes
from __future__ import absolute_import, print_function, unicode_literals
from abc import ABC, abstractmethod
from Live.Song import SessionRecordStatus
from ...base import depends
from ...live import is_track_armed, is_track_recording, liveobj_valid, playing_clip_slot, prepare_new_clip_slot
from .. import Component
from ..controls import ButtonControl, ToggleButtonControl
from ..display import Renderable

class RecordingMethod(ABC):

    @depends(song=None, target_track=None)
    def __init__(self, song=None, target_track=None, *a, **k):
        (super().__init__)(*a, **k)
        self.song = song
        self.target_track = target_track

    @abstractmethod
    def trigger_recording(self):
        pass

    def start_recording(self, *_):
        self.song.session_record = True

    def stop_recording(self):
        status = self.song.session_record_status
        was_recording = status != SessionRecordStatus.off or self.song.session_record
        if was_recording:
            self.song.session_record = False
        return was_recording

    @staticmethod
    def can_record_into_clip_slot(clip_slot):
        return liveobj_valid(clip_slot) and is_track_armed(clip_slot.canonical_parent)


class BasicRecordingMethod(RecordingMethod):

    def trigger_recording(self):
        if not self.stop_recording():
            self.start_recording()


class NextSlotRecordingMethod(RecordingMethod):

    def trigger_recording(self):
        if not self.stop_recording():
            slot = prepare_new_clip_slot(self.target_track.target_track)
            if self.can_record_into_clip_slot(slot):
                slot.fire()
            else:
                self.start_recording()


class NextSlotWithOverdubRecordingMethod(NextSlotRecordingMethod):

    def trigger_recording(self):
        track = self.target_track.target_track
        playing_slot = playing_clip_slot(track)
        if not is_track_recording(track) or playing_slot is not None:
            self.song.overdub = not self.song.overdub
            self.song.is_playing = self.song.is_playing or True
        else:
            super().trigger_recording()


class RecordingComponent(Component, Renderable):
    session_record_button = ButtonControl()
    session_overdub_button = ToggleButtonControl(color='Recording.SessionOverdubOff',
      on_color='Recording.SessionOverdubOn')
    arrangement_record_button = ToggleButtonControl(color='Recording.ArrangementRecordOff',
      on_color='Recording.ArrangementRecordOn')
    arrangement_overdub_button = ToggleButtonControl(color='Recording.ArrangementOverdubOff',
      on_color='Recording.ArrangementOverdubOn')
    new_button = ButtonControl(color='Recording.New',
      pressed_color='Recording.NewPressed')

    @depends(target_track=None)
    def __init__(self, target_track=None, recording_method_type=None, name='Recording', *a, **k):
        (super().__init__)(a, name=name, **k)
        recording_method_type = recording_method_type or BasicRecordingMethod
        self._recording_method = recording_method_type()
        song = self.song
        self.session_overdub_button.connect_property(song, 'overdub')
        self.arrangement_record_button.connect_property(song, 'record_mode')
        self.arrangement_overdub_button.connect_property(song, 'arrangement_overdub')
        self.register_slot(song, self._update_session_record_button, 'session_record_status')
        self.register_slot(song, self._update_session_record_button, 'session_record')
        self._update_session_record_button()
        self._target_track = target_track
        self.register_slot(target_track, self._update_new_button, 'target_clip')
        self._update_new_button()

    @session_record_button.pressed
    def session_record_button(self, _):
        self._recording_method.trigger_recording()

    @new_button.pressed
    def new_button(self, _):
        if prepare_new_clip_slot((self._target_track.target_track), stop=True):
            self.notify(self.notifications.Recording.new)

    def _update_session_record_button(self):
        song = self.song
        status = song.session_record_status
        if status == SessionRecordStatus.transition:
            self.session_record_button.color = 'Recording.SessionRecordTransition'
        else:
            if status == SessionRecordStatus.on or song.session_record:
                self.session_record_button.color = 'Recording.SessionRecordOn'
            else:
                self.session_record_button.color = 'Recording.SessionRecordOff'

    def _update_new_button(self):
        self.new_button.enabled = liveobj_valid(self._target_track.target_clip)


class ViewBasedRecordingComponent(RecordingComponent):

    def __init__(self, name='View_Based_Recording', *a, **k):
        (super().__init__)(a, name=name, **k)
        self._record_button = None
        self._overdub_button = None
        self.register_slot(self.application.view, self.update, 'focused_document_view')

    def disconnect(self):
        super().disconnect()
        self._record_button = None
        self._overdub_button = None

    def set_record_button(self, button):
        self._record_button = button
        self._update_record_button_assignments()

    def set_overdub_button(self, button):
        self._overdub_button = button
        self._update_overdub_button_assignments()

    def update(self):
        super().update()
        self._update_record_button_assignments()
        self._update_overdub_button_assignments()

    def _update_record_button_assignments(self):
        self.arrangement_record_button.set_control_element(None)
        self.session_record_button.set_control_element(None)
        if self.application.view.focused_document_view == 'Session':
            self.session_record_button.set_control_element(self._record_button)
        else:
            self.arrangement_record_button.set_control_element(self._record_button)

    def _update_overdub_button_assignments(self):
        self.arrangement_overdub_button.set_control_element(None)
        self.session_overdub_button.set_control_element(None)
        if self.application.view.focused_document_view == 'Session':
            self.session_overdub_button.set_control_element(self._overdub_button)
        else:
            self.arrangement_overdub_button.set_control_element(self._overdub_button)