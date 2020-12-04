#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/actions.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div
from itertools import count
import Live
from ableton.v2.base import forward_property, listens, listens_group, liveobj_changed, liveobj_valid, old_hasattr
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import UndoRedoComponent as UndoRedoComponentBase
from ableton.v2.control_surface.control import control_list, ButtonControl
from ableton.v2.control_surface.elements import DisplayDataSource
from .action_with_options_component import ActionWithSettingsComponent
from .clip_control_component import convert_beat_length_to_bars_beats_sixteenths
from .consts import MessageBoxText, SIDE_BUTTON_COLORS
from .message_box_component import Messenger
AutomationState = Live.DeviceParameter.AutomationState
_Q = Live.Song.Quantization

def convert_length_to_mins_secs(length_in_secs):
    if length_in_secs is None:
        return u'-'
    mins = int(old_div(length_in_secs, 60.0))
    secs = int(length_in_secs % 60.0)
    return str(mins) + u':' + str(u'%02d' % secs)


def convert_beats_to_mins_secs(length_in_beats, tempo = 120.0):
    if length_in_beats is None:
        return u'-'
    length_in_secs = old_div(length_in_beats, tempo) * 60.0
    return convert_length_to_mins_secs(length_in_secs)


def duplicate_arrangement_clip(clip, song_view, show_notification):
    try:
        track = clip.canonical_parent
        song_view.detail_clip = track.duplicate_clip_to_arrangement(clip, clip.end_time)
        show_notification(MessageBoxText.DUPLICATE_CLIP % clip.name)
    except RuntimeError:
        show_notification(MessageBoxText.CLIP_DUPLICATION_FAILED)


class CaptureAndInsertSceneComponent(ActionWithSettingsComponent, Messenger):

    def _capture_and_insert_scene(self):
        try:
            self.song.capture_and_insert_scene()
            self.show_notification(MessageBoxText.CAPTURE_AND_INSERT_SCENE % self.song.view.selected_scene.name.strip())
        except Live.Base.LimitationError:
            self.expect_dialog(MessageBoxText.SCENE_LIMIT_REACHED)

    def post_trigger_action(self):
        view = self.song.view
        clip = view.detail_clip
        if liveobj_valid(clip) and clip.is_arrangement_clip:
            duplicate_arrangement_clip(clip, view, self.show_notification)
        else:
            self._capture_and_insert_scene()


class DuplicateDetailClipComponent(ActionWithSettingsComponent, Messenger):

    def _duplicate_session_clip(self, clip, view):
        try:
            slot = clip.canonical_parent
            track = slot.canonical_parent
            start_duplicate = clip.is_playing
            target_index = list(track.clip_slots).index(slot)
            destination_index = track.duplicate_clip_slot(target_index)
            view.highlighted_clip_slot = track.clip_slots[destination_index]
            view.detail_clip = view.highlighted_clip_slot.clip
            if start_duplicate:
                view.highlighted_clip_slot.fire(force_legato=True, launch_quantization=_Q.q_no_q)
            self.show_notification(MessageBoxText.DUPLICATE_CLIP % clip.name)
        except Live.Base.LimitationError:
            self.expect_dialog(MessageBoxText.SCENE_LIMIT_REACHED)
        except RuntimeError:
            self.show_notification(MessageBoxText.CLIP_DUPLICATION_FAILED)

    def post_trigger_action(self):
        view = self.song.view
        clip = view.detail_clip
        if liveobj_valid(clip):
            if clip.is_arrangement_clip:
                duplicate_arrangement_clip(clip, view, self.show_notification)
            else:
                self._duplicate_session_clip(clip, view)


class DuplicateLoopComponent(ActionWithSettingsComponent, Messenger):

    def __init__(self, *a, **k):
        super(DuplicateLoopComponent, self).__init__(*a, **k)
        self._on_detail_clip_changed.subject = self.song.view
        self._on_detail_clip_changed()

    @listens(u'detail_clip')
    def _on_detail_clip_changed(self):
        self.action_button.enabled = self.can_duplicate_loop

    @property
    def can_duplicate_loop(self):
        clip = self.song.view.detail_clip
        return clip and clip.is_midi_clip

    def trigger_action(self):
        if self.can_duplicate_loop:
            clip = self.song.view.detail_clip
            if liveobj_valid(clip):
                try:
                    clip.duplicate_loop()
                    self.show_notification(MessageBoxText.DUPLICATE_LOOP % dict(length=convert_beat_length_to_bars_beats_sixteenths((clip.signature_numerator, clip.signature_denominator), clip.loop_end - clip.loop_start)))
                except RuntimeError:
                    pass


class DeleteSelectedClipComponent(ActionWithSettingsComponent, Messenger):
    u"""
    Component that deletes the selected clip when tapping
    """

    def post_trigger_action(self):
        clip = self.song.view.detail_clip
        if liveobj_valid(clip) and clip.is_arrangement_clip:
            try:
                name = clip.name
                self.song.view.selected_track.delete_clip(clip)
                self.show_notification(MessageBoxText.DELETE_CLIP % name)
            except RuntimeError:
                pass

        else:
            slot = self.song.view.highlighted_clip_slot
            if liveobj_valid(slot) and slot.has_clip:
                name = slot.clip.name
                slot.delete_clip()
                self.show_notification(MessageBoxText.DELETE_CLIP % name)


class DeleteSelectedSceneComponent(ActionWithSettingsComponent, Messenger):
    u"""
    Component for deleting the selected scene and launch the previous
    one in scene list mode
    """

    def post_trigger_action(self):
        try:
            song = self.song
            name = song.view.selected_scene.name
            selected_scene_index = list(song.scenes).index(song.view.selected_scene)
            song.delete_scene(selected_scene_index)
            self.show_notification(MessageBoxText.DELETE_SCENE % name)
            new_scene = song.scenes[max(selected_scene_index - 1, 0)]
            song.view.selected_scene = new_scene
            new_scene.fire(force_legato=True)
        except RuntimeError:
            pass


class SelectionDisplayComponent(Component):
    u"""
    This component handles display of selected objects.
    """
    num_segments = 4

    def __init__(self, *a, **k):
        super(SelectionDisplayComponent, self).__init__(*a, **k)
        self._data_sources = [ DisplayDataSource() for _ in range(self.num_segments) ]

    def set_display_line(self, display_line):
        if display_line != None:
            display_line.set_num_segments(self.num_segments)
            for idx in range(self.num_segments):
                display_line.segment(idx).set_data_source(self._data_sources[idx])

    def set_display_string(self, string, segment = 0):
        if segment < self.num_segments:
            self._data_sources[segment].set_display_string(string)

    def reset_display(self):
        for idx in range(self.num_segments):
            self._data_sources[idx].set_display_string(u' ')

    def reset_display_right(self):
        for idx in range(old_div(self.num_segments, 2), self.num_segments):
            self._data_sources[idx].set_display_string(u' ')


def select_clip_and_get_name_from_slot(clip_slot, song):
    if liveobj_valid(clip_slot):
        if song.view.highlighted_clip_slot != clip_slot:
            song.view.highlighted_clip_slot = clip_slot
        if clip_slot.has_clip and liveobj_changed(song.view.detail_clip, clip_slot.clip):
            song.view.detail_clip = clip_slot.clip
    return clip_name_from_clip_slot(clip_slot)


def get_clip_name(clip):
    if clip.name != u'':
        return clip.name
    return u'[unnamed]'


def clip_name_from_clip_slot(clip_slot):
    clip_name = u'[none]'
    if liveobj_valid(clip_slot):
        clip = clip_slot.clip
        clip_name = u'[empty slot]'
        if liveobj_valid(clip):
            clip_name = get_clip_name(clip)
    return clip_name


def select_scene_and_get_name(scene, song):
    scene_name = u'[none]'
    if liveobj_valid(scene):
        if song.view.selected_scene != scene:
            song.view.selected_scene = scene
        scene_name = scene.name if scene.name != u'' else u'[unnamed]'
    return scene_name


class SelectComponent(Component):
    u"""
    This component handles selection of objects.
    """
    select_button = ButtonControl(**SIDE_BUTTON_COLORS)

    def __init__(self, *a, **k):
        super(SelectComponent, self).__init__(*a, **k)
        self._selected_clip = None
        self._selection_display = SelectionDisplayComponent(parent=self)
        self._selection_display.set_enabled(False)

    selection_display_layer = forward_property(u'_selection_display')(u'layer')

    def set_selected_clip(self, clip):
        self._selected_clip = clip
        self._on_playing_position_changed.subject = clip

    def on_select_clip(self, clip_slot):
        clip_name = select_clip_and_get_name_from_slot(clip_slot, self.song)
        if liveobj_valid(clip_slot):
            self.set_selected_clip(clip_slot.clip)
        self._selection_display.set_display_string(u'Clip Selection:')
        self._selection_display.set_display_string(clip_name, 1)
        self._do_show_time_remaining()
        self._selection_display.set_enabled(True)

    @listens(u'playing_position')
    def _on_playing_position_changed(self):
        self._do_show_time_remaining()

    def _do_show_time_remaining(self):
        clip = self._selected_clip
        if liveobj_valid(clip) and (clip.is_triggered or clip.is_playing):
            if clip.is_recording:
                label = u'Record Count:'
                length = old_div((clip.playing_position - clip.loop_start) * clip.signature_denominator, clip.signature_numerator)
                time = convert_beat_length_to_bars_beats_sixteenths((clip.signature_numerator, clip.signature_denominator), length)
            else:
                label = u'Time Remaining:'
                length = clip.loop_end - clip.playing_position
                if clip.is_audio_clip and not clip.warping:
                    time = convert_length_to_mins_secs(length)
                else:
                    time = convert_beats_to_mins_secs(length, self.song.tempo)
        else:
            label = u' '
            time = u' '
        self._selection_display.set_display_string(label, 2)
        self._selection_display.set_display_string(time, 3)

    def on_select_scene(self, scene):
        scene_name = select_scene_and_get_name(scene, self.song)
        self._selection_display.set_display_string(u'Scene Selection:')
        self._selection_display.set_display_string(scene_name, 1)
        self._selection_display.reset_display_right()
        self._selection_display.set_enabled(True)

    def on_select_track(self, track):
        if liveobj_valid(track):
            track_name = track.name if track.name != u'' else u'[unnamed]'
        else:
            track_name = u'[none]'
        self._selection_display.set_display_string(u'Track Selection:')
        self._selection_display.set_display_string(track_name, 1)
        self._selection_display.reset_display_right()
        self._selection_display.set_enabled(True)

    def on_select_drum_pad(self, drum_pad):
        if liveobj_valid(drum_pad):
            drum_pad_name = drum_pad.name if drum_pad.name != u'' else u'[unnamed]'
        else:
            drum_pad_name = u'[none]'
        self._selection_display.set_display_string(u'Pad Selection:')
        self._selection_display.set_display_string(drum_pad_name, 1)
        self._selection_display.reset_display_right()
        self._selection_display.set_enabled(True)

    @select_button.released
    def select_button(self, control):
        self._selection_display.set_enabled(False)
        self._selection_display.reset_display()
        self.set_selected_clip(None)


class DeleteComponent(Component, Messenger):
    u"""
    Component for handling deletion of parameters
    """

    def __init__(self, *a, **k):
        super(DeleteComponent, self).__init__(*a, **k)
        self._delete_button = None

    def set_delete_button(self, button):
        self._delete_button = button

    @property
    def is_deleting(self):
        return self._delete_button and self._delete_button.is_pressed()

    def delete_clip_envelope(self, parameter):
        playing_clip = self._get_playing_clip()
        if playing_clip and parameter.automation_state != AutomationState.none:
            playing_clip.clear_envelope(parameter)
            self.show_notification(MessageBoxText.DELETE_ENVELOPE % dict(automation=parameter.name))

    def _get_playing_clip(self):
        playing_clip = None
        song = self.song
        selected_track = song.view.selected_track
        if old_hasattr(selected_track, u'playing_slot_index'):
            playing_slot_index = selected_track.playing_slot_index
            if playing_slot_index >= 0:
                playing_clip = selected_track.clip_slots[playing_slot_index].clip
        return playing_clip


class DeleteAndReturnToDefaultComponent(DeleteComponent):

    def delete_clip_envelope(self, parameter):
        if parameter.automation_state == AutomationState.none and not parameter.is_quantized:
            parameter.value = parameter.default_value
            self.show_notification(MessageBoxText.DEFAULT_PARAMETER_VALUE % dict(automation=parameter.name))
        super(DeleteAndReturnToDefaultComponent, self).delete_clip_envelope(parameter)


def is_clip_stop_pending(track):
    return track.fired_slot_index == -2


class StopClipComponent(Component):
    stop_all_clips_button = ButtonControl()
    stop_track_clips_buttons = control_list(ButtonControl, color=u'Session.StoppedClip')

    def __init__(self, session_ring = None, *a, **k):
        super(StopClipComponent, self).__init__(*a, **k)
        self._track_provider = session_ring
        self._on_tracks_changed.subject = self._track_provider
        self._on_track_offset_changed.subject = self._track_provider
        self._update_listeners()

    @listens(u'offset')
    def _on_track_offset_changed(self, track_offset, scene_offset):
        self._update_all_stop_buttons()

    @stop_all_clips_button.pressed
    def stop_all_clips_button(self, button):
        self.song.stop_all_clips()

    @stop_track_clips_buttons.pressed
    def stop_track_clips_buttons(self, button):
        self._stop_clips_in_track(button.track)

    def _stop_clips_in_track(self, track):
        track.stop_all_clips()

    @listens(u'tracks')
    def _on_tracks_changed(self):
        self._update_listeners()

    def _update_listeners(self):
        tracks = [ track for track in self._track_provider.controlled_tracks() if isinstance(track, Live.Track.Track) ]
        self._assign_listeners(tracks)
        self._update_all_stop_buttons()

    def _assign_listeners(self, tracks):
        self._on_fired_slot_index_changed.replace_subjects(tracks, count())
        self._on_playing_slot_index_changed.replace_subjects(tracks, count())

    @listens_group(u'fired_slot_index')
    def _on_fired_slot_index_changed(self, track_index):
        self._update_stop_button_by_index(track_index)

    @listens_group(u'playing_slot_index')
    def _on_playing_slot_index_changed(self, track_index):
        self._update_stop_button_by_index(track_index)

    def _update_all_stop_buttons(self):
        tracks = self._track_provider.controlled_tracks()
        self.stop_track_clips_buttons.control_count = len(tracks)
        for track, button in zip(tracks, self.stop_track_clips_buttons):
            self._update_stop_button(track, button)

    def _update_stop_button_by_index(self, index):
        button = self.stop_track_clips_buttons[index]
        self._update_stop_button(button.track, button)

    def _color_for_button(self, track):
        if is_clip_stop_pending(track):
            color = u'Session.StopClipTriggered'
        elif track.playing_slot_index >= 0:
            color = u'Session.StopClip'
        else:
            color = u'Session.StoppedClip'
        return color

    def _update_stop_button(self, track, button):
        has_clip_slots = liveobj_valid(track) and isinstance(track, Live.Track.Track) and bool(track.clip_slots)
        if has_clip_slots:
            button.color = self._color_for_button(track)
        button.enabled = bool(has_clip_slots)
        button.track = track


class UndoRedoComponent(UndoRedoComponentBase, Messenger):

    def _undo(self):
        super(UndoRedoComponent, self)._undo()
        if self.song.can_undo:
            self.show_notification(MessageBoxText.UNDO)

    def _redo(self):
        super(UndoRedoComponent, self)._redo()
        if self.song.can_redo:
            self.show_notification(MessageBoxText.REDO)
