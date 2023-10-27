# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\session.py
# Compiled at: 2023-09-22 14:37:57
# Size of source mod 2**32: 12242 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import count, zip_longest
from ...base import const, depends, inject, listenable_property, listens, listens_group
from ...live import liveobj_valid
from .. import Component
from ..controls import ButtonControl, control_list
from ..display import Renderable
from . import ClipboardComponent, SceneComponent

class SessionComponent(Component, Renderable):
    stop_all_clips_button = ButtonControl(color='Session.StopAllClips',
      pressed_color='Session.StopAllClipsPressed')
    stop_track_clip_buttons = control_list(ButtonControl)
    _session_component_ends_initialisation = True

    @depends(session_ring=None)
    def __init__(self, name='Session', session_ring=None, scene_component_type=None, clip_slot_component_type=None, clipboard_component_type=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._session_ring = session_ring
        scene_component_type = scene_component_type or SceneComponent
        create_scene = lambda: scene_component_type(parent=self,
          session_ring=(self._session_ring),
          clip_slot_component_type=clip_slot_component_type)
        clipboard_component_type = clipboard_component_type or ClipSlotClipboardComponent
        self._clipboard = clipboard_component_type(parent=self)
        with inject(clipboard=(const(self._clipboard))).everywhere():
            self._selected_scene = create_scene()
            self._scenes = [create_scene() for _ in range(self._session_ring.num_scenes)]
        self.register_slot(self._session_ring, self._reassign_scenes, 'scenes')
        self.register_slot(self._session_ring, self._reassign_tracks, 'tracks')
        self._SessionComponent__on_offsets_changed.subject = self._session_ring
        self._SessionComponent__on_selected_scene_changed.subject = self.song.view
        self.stop_track_clip_buttons.control_count = session_ring.num_tracks
        if self._session_component_ends_initialisation:
            self._end_initialisation()

    @listenable_property
    def clipboard(self):
        return self._clipboard

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

    def set_stop_track_clip_buttons(self, buttons):
        self.stop_track_clip_buttons.set_control_element(buttons)
        self._update_stop_track_clip_buttons()

    def set_clip_slot_select_button(self, button):
        self.set_modifier_button(button, 'select_button', clip_slots_only=True)

    def set_select_button(self, button):
        self.set_modifier_button(button, 'select_button')

    def set_delete_button(self, button):
        self.set_modifier_button(button, 'delete_button')

    def set_duplicate_button(self, button):
        self.set_modifier_button(button, 'duplicate_button')

    def set_copy_button(self, button):
        self._clipboard.set_copy_button(button)
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

    @stop_all_clips_button.pressed
    def stop_all_clips_button(self, _):
        self.song.stop_all_clips()

    @stop_track_clip_buttons.pressed
    def stop_track_clip_buttons(self, button):
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


class ClipSlotClipboardComponent(ClipboardComponent):

    def _do_copy(self, obj):
        if not liveobj_valid(obj):
            return
        if obj.is_group_slot:
            self.notify(self.notifications.Clip.CopyPaste.error_copy_from_group_slot)
        else:
            if not liveobj_valid(obj.clip):
                self.notify(self.notifications.Clip.CopyPaste.error_copy_from_empty_slot)
            else:
                if obj.clip.is_recording:
                    self.notify(self.notifications.Clip.CopyPaste.error_copy_recording_clip)
                else:
                    self.notify(self.notifications.Clip.CopyPaste.copy, obj)
                    return obj

    def _do_paste(self, obj):
        if not liveobj_valid(obj):
            return False
        if obj.is_group_slot:
            self.notify(self.notifications.Clip.CopyPaste.error_paste_to_group_slot)
            return False
        source_is_audio = self._source_obj.clip.is_audio_clip
        destination_track = obj.canonical_parent
        if source_is_audio and not destination_track.has_audio_input:
            self.notify(self.notifications.Clip.CopyPaste.error_paste_audio_to_midi)
        else:
            if not source_is_audio or destination_track.has_audio_input:
                self.notify(self.notifications.Clip.CopyPaste.error_paste_midi_to_audio)
            else:
                self._source_obj.duplicate_clip_to(obj)
                self.notify(self.notifications.Clip.CopyPaste.paste, self._source_obj)
                return True
        return False

    def _is_source_valid(self):
        return liveobj_valid(self._source_obj) and self._source_obj.has_clip