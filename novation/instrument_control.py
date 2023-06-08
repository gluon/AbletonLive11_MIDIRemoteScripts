from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.base import listens
from ableton.v2.control_surface import PercussionInstrumentFinder
from ableton.v2.control_surface.components import TargetTrackComponent
from .colors import Rgb
from .util import is_song_recording

def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


class InstrumentControlMixin(object):
    target_track_class = TargetTrackComponent

    def _create_components(self):
        super(InstrumentControlMixin, self)._create_components()
        self._target_track = self.target_track_class(name='Target_Track')
        self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=(self._target_track.target_track)))
        self._InstrumentControlMixin__on_drum_group_changed.subject = self._drum_group_finder
        self._InstrumentControlMixin__on_target_track_changed.subject = self._target_track
        self._InstrumentControlMixin__on_session_record_changed.subject = self.song
        self._InstrumentControlMixin__on_record_mode_changed.subject = self.song
        self._set_feedback_velocity()

    @listens('target_track')
    def __on_target_track_changed(self):
        self._target_track_changed()

    def _target_track_changed(self):
        track = self._target_track.target_track
        self._drum_group_finder.device_parent = track
        self._drum_group.set_parent_track(track)
        self._InstrumentControlMixin__on_target_track_arm_changed.subject = track
        self._InstrumentControlMixin__on_target_track_implicit_arm_changed.subject = track
        self._update_controlled_track()

    @listens('instrument')
    def __on_drum_group_changed(self):
        self._drum_group_changed()

    def _drum_group_changed(self):
        raise NotImplementedError

    @listens('session_record')
    def __on_session_record_changed(self):
        self._set_feedback_velocity()

    @listens('record_mode')
    def __on_record_mode_changed(self):
        self._set_feedback_velocity()

    @listens('arm')
    def __on_target_track_arm_changed(self):
        self._set_feedback_velocity()

    @listens('implicit_arm')
    def __on_target_track_implicit_arm_changed(self):
        self._set_feedback_velocity()

    def _update_controlled_track(self):
        if self._is_instrument_mode():
            self.set_controlled_track(self._target_track.target_track)
        else:
            self.release_controlled_track()

    def _is_instrument_mode(self):
        raise NotImplementedError

    def _set_feedback_velocity(self):
        track = self._target_track.target_track
        if is_song_recording(self.song) and track_can_record(track):
            feedback_velocity = Rgb.RED.midi_value
        else:
            feedback_velocity = Rgb.GREEN.midi_value
        self._c_instance.set_feedback_velocity(int(feedback_velocity))
        self._feedback_velocity_changed(feedback_velocity)

    def _feedback_velocity_changed(self, feedback_velocity):
        pass