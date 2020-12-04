#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/session_recording_component.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter
import Live
from ableton.v2.base import listens, liveobj_valid, EventObject
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.components import SessionRecordingComponent
from .consts import MessageBoxText
from .message_box_component import Messenger
Quantization = Live.Song.Quantization

def track_can_overdub(track):
    return not track.has_audio_input


def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


def get_clip_slot_from_index(song, track, clip_slot_index):
    clip_slots = track.clip_slots
    if clip_slot_index < len(clip_slots):
        return clip_slots[clip_slot_index]


def have_other_recording_clips(tracks, recording_clip):
    for track in filter(lambda t: t.can_be_armed and (t.arm or t.implicit_arm), tracks):
        index = track.playing_slot_index
        slot = track.clip_slots[index] if 0 <= index < len(track.clip_slots) else None
        clip = getattr(slot, u'clip', None)
        if getattr(clip, u'is_recording', False) and clip is not recording_clip:
            return True

    return False


class FixedLengthRecording(EventObject):

    def __init__(self, song = None, clip_creator = None, fixed_length_setting = None, *a, **k):
        assert song is not None
        assert clip_creator is not None
        assert fixed_length_setting is not None
        super(FixedLengthRecording, self).__init__(*a, **k)
        self._song = song
        self._clip_creator = clip_creator
        self._fixed_length_setting = fixed_length_setting
        self._clip_creator.legato_launch = self._fixed_length_setting.legato_launch
        self.__on_setting_selected_index_changes.subject = self._fixed_length_setting
        self.__on_setting_legato_launch_changes.subject = self._fixed_length_setting

    def should_start_fixed_length_recording(self, clip_slot):
        return track_can_record(clip_slot.canonical_parent) and not clip_slot.is_recording and not clip_slot.has_clip and self._fixed_length_setting.enabled

    def start_recording_in_slot(self, track, clip_slot_index):
        song = self._song
        song.overdub = True
        if track_can_record(track):
            self._record_in_slot(track, track.clip_slots[clip_slot_index])
        if not song.is_playing:
            song.is_playing = True

    def _is_infinite_recording(self, clip):
        return not clip.is_overdubbing

    def stop_recording(self, clip):
        if have_other_recording_clips(self._song.tracks, clip):
            clip.fire()
        elif self._is_infinite_recording(clip):
            self._song.session_record = False
        else:
            self._song.overdub = False

    def _record_in_slot(self, track, clip_slot):
        if self.should_start_fixed_length_recording(clip_slot):
            length, quant = self._fixed_length_setting.get_selected_length(self._song)
            if self._song.is_playing:
                quant = self._song.clip_trigger_quantization
            if track_can_overdub(track):
                self._clip_creator.create(clip_slot, length=length, launch_quantization=self._song.clip_trigger_quantization)
            else:
                clip_slot.fire(record_length=length, launch_quantization=quant)
        elif not clip_slot.is_playing or not self._song.is_playing:
            if clip_slot.has_clip:
                clip_slot.stop()
                clip_slot.fire(force_legato=True, launch_quantization=Quantization.q_no_q)
            else:
                clip_slot.fire()

    @listens(u'selected_index')
    def __on_setting_selected_index_changes(self, _):
        length, _ = self._fixed_length_setting.get_selected_length(self._song)
        self._clip_creator.fixed_length = length

    @listens(u'legato_launch')
    def __on_setting_legato_launch_changes(self, value):
        self._clip_creator.legato_launch = value


class FixedLengthSessionRecordingComponent(SessionRecordingComponent, Messenger):
    foot_switch_button = ButtonControl()
    arrangement_record_button = ButtonControl()
    capture_midi_button = ButtonControl()

    def __init__(self, clip_creator = None, fixed_length_setting = None, *a, **k):
        assert clip_creator is not None
        assert fixed_length_setting is not None
        super(FixedLengthSessionRecordingComponent, self).__init__(*a, **k)
        self._fixed_length_recording = self.register_disconnectable(FixedLengthRecording(song=self.song, clip_creator=clip_creator, fixed_length_setting=fixed_length_setting))
        self.footswitch_toggles_arrangement_recording = False
        self.__on_record_mode_changed.subject = self.song
        self.__on_record_mode_changed()
        self.set_trigger_recording_on_release(not any((self.record_button.is_pressed, self.arrangement_record_button.is_pressed)))

    def set_trigger_recording_on_release(self, trigger_recording):
        self._should_trigger_recording = trigger_recording

    @foot_switch_button.pressed
    def foot_switch_button(self, button):
        if self.footswitch_toggles_arrangement_recording:
            self._toggle_arrangement_recording()
        else:
            self._trigger_recording()

    @capture_midi_button.pressed
    def capture_midi_button(self, button):
        try:
            self.song.capture_midi()
            self.set_trigger_recording_on_release(not any((self.record_button.is_pressed, self.arrangement_record_button.is_pressed)))
        except RuntimeError:
            pass

    @arrangement_record_button.pressed
    def arrangement_record_button(self, _):
        self._on_arrangement_record_button_pressed()

    @arrangement_record_button.released
    def arrangement_record_button(self, _):
        self._on_arrangement_record_button_released()

    def _toggle_arrangement_recording(self):
        self.song.record_mode = not self.song.record_mode

    def _on_record_button_pressed(self):
        pass

    def _on_record_button_released(self):
        self._trigger_recording_action(self._trigger_recording)

    def _on_arrangement_record_button_pressed(self):
        pass

    def _on_arrangement_record_button_released(self):
        self._trigger_recording_action(self._toggle_arrangement_recording)

    def _trigger_recording_action(self, recording_action):
        if self._should_trigger_recording:
            recording_action()
        self._should_trigger_recording = True

    def _clip_slot_index_to_record_into(self):
        song = self.song
        selected_scene = song.view.selected_scene
        return list(song.scenes).index(selected_scene)

    def _update_record_button(self):
        if self.is_enabled():
            song = self.song
            clip_slot = get_clip_slot_from_index(song, song.view.selected_track, self._clip_slot_index_to_record_into())
            if liveobj_valid(clip_slot) and clip_slot.is_triggered and song.overdub and not clip_slot.is_recording:
                self.record_button.color = u'Recording.Transition'
            elif song.record_mode:
                self.record_button.color = u'Recording.ArrangementRecordingOn'
            else:
                super(FixedLengthSessionRecordingComponent, self)._update_record_button()
            self.arrangement_record_button.color = self.record_button.color

    @listens(u'record_mode')
    def __on_record_mode_changed(self):
        self._update_record_button()

    def _start_recording(self):
        track = self.song.view.selected_track
        clip_slot_index = self._clip_slot_index_to_record_into()
        self._fixed_length_recording.start_recording_in_slot(track, clip_slot_index)
        if track_can_record(track):
            self._ensure_slot_is_visible(self.song.view.selected_track, clip_slot_index)

    def _ensure_slot_is_visible(self, track, scene_index):
        song = self.song
        if song.view.selected_track == track:
            song.view.selected_scene = song.scenes[scene_index]
        self._view_selected_clip_detail()

    def _handle_limitation_error_on_scene_creation(self):
        self.expect_dialog(MessageBoxText.SCENE_LIMIT_REACHED)
