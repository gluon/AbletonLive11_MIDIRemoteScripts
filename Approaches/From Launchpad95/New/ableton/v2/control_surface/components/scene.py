#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/scene.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from builtins import zip
from ...base import listens, liveobj_valid, liveobj_changed
from ..component import Component
from ..control import ButtonControl
from .clip_slot import ClipSlotComponent, is_button_pressed, find_nearest_color

class SceneComponent(Component):
    u"""
    Class representing a scene in Live
    """
    clip_slot_component_type = ClipSlotComponent
    launch_button = ButtonControl()

    def __init__(self, session_ring = None, *a, **k):
        assert session_ring is not None
        assert session_ring.num_tracks >= 0
        self._controlled_tracks = []
        super(SceneComponent, self).__init__(*a, **k)
        self._session_ring = session_ring
        self._scene = None
        self._clip_slots = []
        self._color_palette = None
        self._color_table = None
        for _ in range(session_ring.num_tracks):
            new_slot = self._create_clip_slot()
            self._clip_slots.append(new_slot)

        self._triggered_color = u'Session.SceneTriggered'
        self._scene_color = u'Session.Scene'
        self._no_scene_color = u'Session.NoScene'
        self._track_offset = 0
        self._select_button = None
        self._delete_button = None
        self._duplicate_button = None
        self.__on_track_list_changed.subject = session_ring

    @listens(u'tracks')
    def __on_track_list_changed(self):
        self._update_controlled_tracks()

    def set_scene(self, scene):
        if liveobj_changed(scene, self._scene):
            self._scene = scene
            self.__on_is_triggered_changed.subject = scene
            self.__on_scene_color_changed.subject = scene
            self.update()

    def set_launch_button(self, button):
        self.launch_button.set_control_element(button)
        self.update()

    def set_select_button(self, button):
        self._select_button = button

    def set_delete_button(self, button):
        self._delete_button = button

    def set_duplicate_button(self, button):
        self._duplicate_button = button

    def set_track_offset(self, offset):
        assert offset >= 0
        if offset != self._track_offset:
            self._track_offset = offset
            self._update_controlled_tracks()

    def set_color_palette(self, palette):
        self._color_palette = palette

    def set_color_table(self, table):
        self._color_table = table

    def clip_slot(self, index):
        return self._clip_slots[index]

    def update(self):
        super(SceneComponent, self).update()
        if liveobj_valid(self._scene) and self.is_enabled():
            clip_slots_to_use = self.build_clip_slot_list()
            for slot_wrapper, clip_slot in zip(self._clip_slots, clip_slots_to_use):
                slot_wrapper.set_clip_slot(clip_slot)

        else:
            for slot in self._clip_slots:
                slot.set_clip_slot(None)

        self._update_launch_button()

    def _update_controlled_tracks(self):
        controlled_tracks = self._session_ring.controlled_tracks()
        if controlled_tracks != self._controlled_tracks:
            self.update()
            self._controlled_tracks = controlled_tracks

    def _determine_actual_track_offset(self, tracks):
        actual_track_offset = self._track_offset
        if self._track_offset > 0:
            real_offset = 0
            visible_tracks = 0
            while visible_tracks < self._track_offset and len(tracks) > real_offset:
                if tracks[real_offset].is_visible:
                    visible_tracks += 1
                real_offset += 1

            actual_track_offset = real_offset
        return actual_track_offset

    def build_clip_slot_list(self):
        slots_to_use = []
        tracks = self.song.tracks
        track_offset = self._determine_actual_track_offset(tracks)
        clip_slots = self._scene.clip_slots
        for _ in self._clip_slots:
            while len(tracks) > track_offset and not tracks[track_offset].is_visible:
                track_offset += 1

            if len(clip_slots) > track_offset:
                slots_to_use.append(clip_slots[track_offset])
            else:
                slots_to_use.append(None)
            track_offset += 1

        return slots_to_use

    @launch_button.pressed
    def launch_button(self, value):
        self._on_launch_button_pressed()

    def _on_launch_button_pressed(self):
        if is_button_pressed(self._select_button):
            self._do_select_scene(self._scene)
        elif liveobj_valid(self._scene):
            if is_button_pressed(self._duplicate_button):
                self._do_duplicate_scene(self._scene)
            elif is_button_pressed(self._delete_button):
                self._do_delete_scene(self._scene)
            else:
                self._do_launch_scene(True)

    @launch_button.released
    def launch_button(self, value):
        self._on_launch_button_released()

    def _on_launch_button_released(self):
        if not is_button_pressed(self._select_button) and liveobj_valid(self._scene) and not is_button_pressed(self._duplicate_button) and not is_button_pressed(self._delete_button):
            self._do_launch_scene(False)

    def _do_select_scene(self, scene_for_overrides):
        if liveobj_valid(self._scene):
            view = self.song.view
            if view.selected_scene != self._scene:
                view.selected_scene = self._scene
                self._on_scene_selected()

    def _on_scene_selected(self):
        pass

    def _do_delete_scene(self, scene_for_overrides):
        try:
            if liveobj_valid(self._scene):
                song = self.song
                song.delete_scene(list(song.scenes).index(self._scene))
                self._on_scene_deleted()
        except RuntimeError:
            pass

    def _on_scene_deleted(self):
        pass

    def _do_duplicate_scene(self, scene_for_overrides):
        try:
            song = self.song
            song.duplicate_scene(list(song.scenes).index(self._scene))
            self._on_scene_duplicated()
        except (Live.Base.LimitationError, IndexError, RuntimeError):
            pass

    def _on_scene_duplicated(self):
        pass

    def _do_launch_scene(self, value):
        launched = False
        if self.launch_button.is_momentary:
            self._scene.set_fire_button_state(value != 0)
            launched = value != 0
        elif value != 0:
            self._scene.fire()
            launched = True
        if launched and self.song.select_on_launch:
            self.song.view.selected_scene = self._scene

    @listens(u'is_triggered')
    def __on_is_triggered_changed(self):
        assert liveobj_valid(self._scene)
        self._update_launch_button()

    @listens(u'color')
    def __on_scene_color_changed(self):
        assert liveobj_valid(self._scene)
        self._update_launch_button()

    def _color_value(self, color):
        value = None
        if self._color_palette:
            value = self._color_palette.get(color, None)
        if value is None and self._color_table:
            value = find_nearest_color(self._color_table, color)
        return value

    def _update_launch_button(self):
        if self.is_enabled():
            value_to_send = self._no_scene_color
            if liveobj_valid(self._scene):
                value_to_send = self._scene_color
                if self._scene.is_triggered:
                    value_to_send = self._triggered_color
                else:
                    possible_color = self._color_value(self._scene.color)
                    if possible_color:
                        value_to_send = possible_color
            self.launch_button.color = value_to_send

    def _create_clip_slot(self):
        return self.clip_slot_component_type(parent=self)
