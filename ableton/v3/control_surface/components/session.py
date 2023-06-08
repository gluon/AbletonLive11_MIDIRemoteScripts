<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from itertools import count, zip_longest
from ...base import clip_slot_display_name, const, depends, inject, listens, listens_group, liveobj_valid
from .. import Component
from ..controls import ButtonControl, control_list
from . import SceneComponent
COPY_FROM_GROUP_SLOT_ERROR = 'Cannot copy from Group Slot'
COPY_FROM_EMPTY_SLOT_ERROR = 'Cannot copy from empty Clip Slot'
COPY_RECORDING_CLIP_ERROR = 'Cannot copy recording Clip'
COPY_SUCCESS = '{} copied. Press destination Clip Slot to paste'
PASTE_TO_GROUP_SLOT_ERROR = 'Cannot paste into Group Slot'
PASTE_AUDIO_TO_MIDI_ERROR = 'Cannot paste an audio Clip into a MIDI Track'
PASTE_MIDI_TO_AUDIO_ERROR = 'Cannot paste a MIDI Clip into an audio Track'
PASTE_SUCCESS = '{} copied to: {}'

class SessionComponent(Component):
    copy_button = ButtonControl(color=None)
    stop_all_clips_button = ButtonControl(color='Session.StopAllClips',
      pressed_color='Session.StopAllClipsPressed')
    stop_track_clip_buttons = control_list(ButtonControl)
    _session_component_ends_initialisation = True

    @depends(session_ring=None)
    def __init__(self, name='Session', session_ring=None, scene_component_type=None, clip_slot_component_type=None, clip_slot_copy_handler_type=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._session_ring = session_ring
        scene_component_type = scene_component_type or SceneComponent
        create_scene = lambda: scene_component_type(parent=self,
          session_ring=(self._session_ring),
          clip_slot_component_type=clip_slot_component_type)
        clip_slot_copy_handler_type = clip_slot_copy_handler_type or ClipSlotCopyHandler
        self._clip_slot_copy_handler = clip_slot_copy_handler_type()
        with inject(copy_handler=(const(self._clip_slot_copy_handler))).everywhere():
            self._selected_scene = create_scene()
            self._scenes = [create_scene() for _ in range(self._session_ring.num_scenes)]
        self.register_slot(self._session_ring, self._reassign_scenes, 'scenes')
        self.register_slot(self._session_ring, self._reassign_tracks, 'tracks')
        self._SessionComponent__on_offsets_changed.subject = self._session_ring
        self._SessionComponent__on_selected_scene_changed.subject = self.song.view
        self.stop_track_clip_buttons.control_count = session_ring.num_tracks
        if self._session_component_ends_initialisation:
            self._end_initialisation()

    @property
    def clip_slot_copy_handler(self):
        return self._clip_slot_copy_handler

    def scene(self, index):
        return self._scenes[index]

    def selected_scene(self):
        return self._selected_scene

    def set_clip_launch_buttons(self, buttons):
        for y, scene in enumerate(self._scenes):
            for x in range(self._session_ring.num_tracks):
                button = buttons.get_button(y, x) if buttons else None
                scene.clip_slot(x).set_launch_button(button)

    def set_scene_launch_buttons(self, buttons):
        num_scenes = self._session_ring.num_scenes
        for scene, button in zip_longest(self._scenes, buttons or []):
            scene.set_launch_button(button)
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/session.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 4573 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as ClipSlotComponentBase
import ableton.v2.control_surface.components as SceneComponentBase
import ableton.v2.control_surface.components as SessionComponentBase
from ...base import depends, liveobj_valid
from ..controls import ButtonControl, control_list

class ClipSlotComponent(ClipSlotComponentBase):

    def __init__(self, color_for_obj_function=None, *a, **k):
        self._color_for_obj_function = color_for_obj_function
        (super().__init__)(*a, **k)
        self._record_button_color = 'Session.ClipRecordButton'

    @property
    def clip_slot(self):
        return self._clip_slot

    def _color_value(self, slot_or_clip):
        if self._color_for_obj_function:
            if liveobj_valid(slot_or_clip):
                return self._color_for_obj_function(slot_or_clip)
        return super()._color_value(slot_or_clip)


class SceneComponent(SceneComponentBase):

    def __init__(self, clip_slot_component_type=None, color_for_obj_function=None, *a, **k):
        self._color_for_obj_function = color_for_obj_function
        clip_slot_component_type = clip_slot_component_type or ClipSlotComponent
        self._create_clip_slot = lambda: clip_slot_component_type(parent=self,
          color_for_obj_function=color_for_obj_function)
        (super().__init__)(*a, **k)
        self._no_scene_color = 'Session.SceneEmpty'

    @property
    def scene(self):
        return self._scene

    def _color_value(self, color):
        if self._color_for_obj_function:
            if liveobj_valid(self._scene):
                return self._color_for_obj_function(self._scene)
        return super()._color_value(color)


class SessionComponent(SessionComponentBase):
    stop_all_clips_button = ButtonControl(color='Session.StopAllClips',
      pressed_color='Session.StopAllClipsPressed')
    stop_track_clip_buttons = control_list(ButtonControl)

    @depends(session_ring=None)
    def __init__(self, name='Session', session_ring=None, scene_component_type=None, clip_slot_component_type=None, color_for_obj_function=None, *a, **k):
        scene_component_type = scene_component_type or SceneComponent
        self._create_scene = lambda: scene_component_type(parent=self,
          session_ring=(self._session_ring),
          clip_slot_component_type=clip_slot_component_type,
          color_for_obj_function=color_for_obj_function)
        (super().__init__)(a, name=name, session_ring=session_ring, **k)
        self.stop_track_clip_buttons.control_count = session_ring.num_tracks

    def set_stop_all_clips_button(self, button):
        self.stop_all_clips_button.set_control_element(button)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def set_stop_track_clip_buttons(self, buttons):
        self.stop_track_clip_buttons.set_control_element(buttons)
        self._update_stop_track_clip_buttons()

<<<<<<< HEAD
    def set_clip_slot_select_button(self, button):
        self.set_modifier_button(button, 'select_button', clip_slots_only=True)

    def set_select_button(self, button):
        self.set_modifier_button(button, 'select_button')

    def set_delete_button(self, button):
        self.set_modifier_button(button, 'delete_button')

    def set_duplicate_button(self, button):
        self.set_modifier_button(button, 'duplicate_button')

    def set_copy_button(self, button):
        self.copy_button.set_control_element(button)
        self.set_modifier_button(button, 'copy_button', clip_slots_only=True)

    def set_modifier_button(self, button, name, clip_slots_only=False):
        for y in range(self._session_ring.num_scenes):
            scene = self.scene(y)
            if not clip_slots_only:
                getattr(scene, name).set_control_element(button)
            else:
                for x in range(self._session_ring.num_tracks):
                    getattr(scene.clip_slot(x), name).set_control_element(button)

    def __getattr__(self, name):
        if name.startswith('set_selected_scene_launch_button'):
            return self.selected_scene().set_launch_button
        if name.startswith('set_scene_'):
            if name.endswith('_launch_button'):
                return self.scene(int(name.split('_')[-3])).set_launch_button
        raise AttributeError

    @copy_button.released
    def copy_button(self, _):
        self._clip_slot_copy_handler.stop_copying()

=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    @stop_all_clips_button.pressed
    def stop_all_clips_button(self, _):
        self.song.stop_all_clips()

    @stop_track_clip_buttons.pressed
    def stop_track_clip_buttons(self, button):
<<<<<<< HEAD
        self._session_ring.tracks[button.index].stop_all_clips()

    def _end_initialisation(self):
        self._SessionComponent__on_selected_scene_changed()
        self._reassign_tracks_and_scenes()

    def update(self):
        super().update()
        if self.is_enabled():
            self._update_stop_track_clip_buttons()
            self._reassign_tracks_and_scenes()

    def _reassign_tracks_and_scenes(self):
        self._reassign_tracks()
        self._reassign_scenes()

    def _reassign_scenes(self):
        scenes = self.song.scenes
        for index, scene in enumerate(self._scenes):
            scene_index = self._session_ring.scene_offset + index
            scene.set_scene(scenes[scene_index] if len(scenes) > scene_index else None)

    def _reassign_tracks(self):
        tracks = self._session_ring.tracks
        self._SessionComponent__on_fired_slot_index_changed.replace_subjects(tracks, count())
        self._SessionComponent__on_playing_slot_index_changed.replace_subjects(tracks, count())
        self._update_stop_track_clip_buttons()

    def _update_stop_track_clip_buttons(self):
        if self.is_enabled():
            for index in range(self._session_ring.num_tracks):
                self._update_stop_clips_led(index)

    def _update_stop_clips_led(self, index):
        if index < self.stop_track_clip_buttons.control_count:
            tracks = self._session_ring.tracks
            track = tracks[index] if index < len(tracks) else None
            button = self.stop_track_clip_buttons[index]
            if liveobj_valid(track) and track.clip_slots:
                button.enabled = True
                if track.fired_slot_index == -2:
                    button.color = 'Session.StopClipTriggered'
                else:
                    if track.playing_slot_index >= 0:
                        button.color = 'Session.StopClip'
                    else:
                        button.color = 'Session.StopClipDisabled'
            else:
                button.enabled = False

    @listens('offset')
    def __on_offsets_changed(self, *_):
        if self.is_enabled():
            self._reassign_tracks_and_scenes()

    @listens('selected_scene')
    def __on_selected_scene_changed(self):
        if self._selected_scene is not None:
            self._selected_scene.set_scene(self.song.view.selected_scene)

    @listens_group('fired_slot_index')
    def __on_fired_slot_index_changed(self, track_index):
        self._update_stop_clips_led(track_index)

    @listens_group('playing_slot_index')
    def __on_playing_slot_index_changed(self, track_index):
        self._update_stop_clips_led(track_index)


class ClipSlotCopyHandler:

    @depends(show_message=None)
    def __init__(self, show_message=None, *a, **k):
        (super().__init__)(*a, **k)
        self._show_message = show_message
        self._is_copying = False
        self._source_clip_slot = None

    @property
    def is_copying(self):
        return self._is_copying

    def copy_or_paste(self, slot):
        status_msg = None
        if self._is_copying:
            status_msg = self._paste_clip_slot(slot)
        else:
            status_msg = self._copy_clip_slot(slot)
        if status_msg:
            self._show_message(status_msg)

    def stop_copying(self):
        self._reset_copying_state()

    def _copy_clip_slot(self, source_slot):
        if not liveobj_valid(source_slot):
            return
        if source_slot.is_group_slot:
            return COPY_FROM_GROUP_SLOT_ERROR
        if not liveobj_valid(source_slot.clip):
            return COPY_FROM_EMPTY_SLOT_ERROR
        if source_slot.clip.is_recording:
            return COPY_RECORDING_CLIP_ERROR
        return self._perform_copy(source_slot)

    def _perform_copy(self, source_slot):
        self._is_copying = True
        self._source_clip_slot = source_slot
        clip_name = clip_slot_display_name(source_slot)
        return COPY_SUCCESS.format(clip_name)

    def _paste_clip_slot(self, destination_slot):
        if not liveobj_valid(destination_slot):
            return
        if destination_slot.is_group_slot:
            return PASTE_TO_GROUP_SLOT_ERROR
        source_is_audio = self._source_clip_slot.clip.is_audio_clip
        destination_track = destination_slot.canonical_parent
        if source_is_audio:
            if not destination_track.has_audio_input:
                return PASTE_AUDIO_TO_MIDI_ERROR
            if not source_is_audio:
                if destination_track.has_audio_input:
                    return PASTE_MIDI_TO_AUDIO_ERROR
            return self._perform_paste(destination_track, destination_slot)

    def _perform_paste(self, destination_track, destination_slot):
        self._source_clip_slot.duplicate_clip_to(destination_slot)
        clip_name = clip_slot_display_name(self._source_clip_slot)
        self._reset_copying_state()
        return PASTE_SUCCESS.format(clip_name, destination_track.name)

    def _reset_copying_state(self):
        self._source_clip_slot = None
        self._is_copying = False
=======
        tracks_to_use = self._session_ring.tracks_to_use()
        track_index = self._session_ring.track_offset + button.index
        if track_index < len(tracks_to_use):
            tracks_to_use[track_index].stop_all_clips()

    def _update_stop_clips_led(self, index):
        if index < self.stop_track_clip_buttons.control_count:
            tracks_to_use = self._session_ring.tracks_to_use()
            track_index = self._session_ring.track_offset + index
            button = self.stop_track_clip_buttons[index]
            if track_index < len(tracks_to_use) and tracks_to_use[track_index].clip_slots:
                button.enabled = True
                track = tracks_to_use[track_index]
                if track.fired_slot_index == -2:
                    button.color = 'Session.StopClipTriggered'
                elif track.playing_slot_index >= 0:
                    button.color = 'Session.StopClip'
                else:
                    button.color = 'Session.StopClipDisabled'
            else:
                button.enabled = False
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
