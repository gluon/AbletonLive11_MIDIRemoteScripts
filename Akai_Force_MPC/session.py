#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/session.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import range
from future.moves.itertools import zip_longest
from past.utils import old_div
from itertools import count, product
import Live
from ableton.v2.base import clamp, find_if, in_range, index_if, listens_group, liveobj_valid
from ableton.v2.control_surface.components import SessionComponent as SessionComponentBase
from ableton.v2.control_surface.control import ButtonControl, SendValueControl, control_list
from .elements import NUM_TRACK_CONTROLS
from .scene import SceneComponent

def _set_method(component, control_name):
    set_method = getattr(component, u'set_{}'.format(control_name), None)
    if not set_method:
        set_method = getattr(component, control_name, None).set_control_element
    return set_method


def find_first_playing_grouped_track(group_track, all_tracks):

    def is_playing_and_grouped(track):
        return is_child_of_group_track(group_track, track) and not track.is_foldable and track.playing_slot_index >= 0

    return find_if(is_playing_and_grouped, all_tracks[index_if(lambda t: t == group_track, all_tracks):])


def is_child_of_group_track(group_track, track):
    group_track_of_track = track.group_track
    return liveobj_valid(group_track_of_track) and (group_track_of_track == group_track or is_child_of_group_track(group_track, group_track_of_track))


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent
    stop_clip_color_controls = control_list(ButtonControl, NUM_TRACK_CONTROLS)
    playing_position_controls = control_list(SendValueControl, NUM_TRACK_CONTROLS)
    insert_scene_button = ButtonControl()

    def __init__(self, *a, **k):
        self._playing_position_subjects = [None] * NUM_TRACK_CONTROLS
        super(SessionComponent, self).__init__(*a, **k)
        self._update_playing_position_subjects()

    @insert_scene_button.pressed
    def insert_scene_button(self, _):
        try:
            song = self.song
            scenes = song.scenes
            song.create_scene(clamp(index_if(lambda s: s == song.view.selected_scene, scenes) + 1, 0, len(scenes)))
        except Live.Base.LimitationError:
            pass

    def set_clip_color_controls(self, controls):
        self._set_clip_controls(u'clip_color_control', controls)

    def set_clip_name_displays(self, displays):
        self._set_clip_controls(u'clip_name_display', displays)

    def set_scene_name_displays(self, displays):
        self._set_scene_controls(u'scene_name_display', displays)

    def set_scene_color_controls(self, controls):
        self._set_scene_controls(u'scene_color_control', controls)

    def set_scene_selection_controls(self, controls):
        self._set_scene_controls(u'scene_selection_control', controls)

    def set_force_scene_launch_buttons(self, buttons):
        self._set_scene_controls(u'force_launch_button', buttons)

    def set_select_button(self, button):
        for scene_index, slot_index in product(range(self._session_ring.num_scenes), range(self._session_ring.num_tracks)):
            self.scene(scene_index).clip_slot(slot_index).set_select_button(button)

    def _reassign_tracks(self):
        super(SessionComponent, self)._reassign_tracks()
        self._update_playing_position_subjects()

    def _on_fired_slot_index_changed(self, track_index):
        super(SessionComponent, self)._on_fired_slot_index_changed(track_index)
        self._update_playing_position_subject(track_index)

    def _on_playing_slot_index_changed(self, track_index):
        super(SessionComponent, self)._on_playing_slot_index_changed(track_index)
        self._update_playing_position_subject(track_index)

    def _update_playing_position_subject(self, track_index):
        session_ring = self._session_ring
        track_offset = session_ring.track_offset
        if in_range(track_index, track_offset, track_offset + session_ring.num_tracks):
            self._do_update_playing_position_subject(track_index - track_offset)

    def _update_playing_position_subjects(self):
        for index in range(NUM_TRACK_CONTROLS):
            self._do_update_playing_position_subject(index)

    def _do_update_playing_position_subject(self, index):
        session_ring = self._session_ring
        tracks = session_ring.tracks_to_use()
        track_index = session_ring.track_offset + index
        new_subject = None
        if track_index < len(tracks):
            track = tracks[track_index]
            if self._can_have_playing_slots(track):
                if liveobj_valid(track.group_track):
                    group_track_index = index_if(lambda t: t == track.group_track, tracks)
                    if group_track_index < len(tracks):
                        subject_index = index - track_index + group_track_index
                        if in_range(subject_index, 0, session_ring.num_tracks):
                            self._do_update_playing_position_subject(subject_index)
                if track.is_foldable:
                    track = find_first_playing_grouped_track(track, self.song.tracks)
                if liveobj_valid(track):
                    playing_slot_index = track.playing_slot_index
                    if playing_slot_index >= 0:
                        clip_slot = track.clip_slots[playing_slot_index]
                        if clip_slot.has_clip:
                            new_subject = clip_slot.clip
        self._playing_position_subjects[index] = new_subject
        self.__on_playing_position_changed.replace_subjects(self._playing_position_subjects, identifiers=count())
        self.__on_playing_position_changed(index)

    @listens_group(u'playing_position')
    def __on_playing_position_changed(self, index):
        clip = self._playing_position_subjects[index]
        normalized_value = 0.0
        if liveobj_valid(clip):
            playing_position = clip.playing_position
            loop_start = clip.loop_start
            start_marker = clip.start_marker
            if not clip.looping:
                normalized_value = old_div(playing_position - clip.start_marker, clip.length)
            elif start_marker < loop_start and playing_position < loop_start:
                normalized_value = old_div(playing_position - clip.start_marker, loop_start - start_marker)
            else:
                length = clip.length
                position_in_loop = playing_position - loop_start - max(0, clip.start_marker - loop_start)
                if position_in_loop < 0:
                    position_in_loop += length
                normalized_value = old_div(position_in_loop, length)
        self.playing_position_controls[index].value = clamp(int(normalized_value * 127), 0, 127)

    def _update_stop_clips_led(self, index):
        super(SessionComponent, self)._update_stop_clips_led(index)
        if index < self.stop_clip_color_controls.control_count:
            color = u'DefaultButton.Off'
            tracks_to_use = self._session_ring.tracks_to_use()
            track_index = index + self._session_ring.track_offset
            if track_index < len(tracks_to_use) and tracks_to_use[track_index].clip_slots:
                color = u'Session.StopClip'
            self.stop_clip_color_controls[index].color = color

    def _set_clip_controls(self, name, controls):
        assert not controls or controls.width() == self._session_ring.num_tracks and controls.height() == self._session_ring.num_scenes
        for x, y in product(range(self._session_ring.num_tracks), range(self._session_ring.num_scenes)):
            scene = self.scene(y)
            slot = scene.clip_slot(x)
            _set_method(slot, name)(controls.get_button(x, y) if controls else None)

    def _set_scene_controls(self, name, controls):
        assert not controls or controls.width() == self._session_ring.num_scenes and controls.height() == 1
        for x in range(self._session_ring.num_scenes):
            scene = self.scene(x)

        for scene, control in zip_longest(self._scenes, controls or []):
            _set_method(scene, name)(control)

    def _can_have_playing_slots(self, track):
        return liveobj_valid(track) and not (track == self.song.master_track or track in self.song.return_tracks)
