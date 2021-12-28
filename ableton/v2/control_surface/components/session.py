#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/session.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from itertools import count
from ...base import EventObject, in_range, product, listens, listens_group
from ..component import Component
from ..control import ButtonControl
from .scene import SceneComponent

class SessionComponent(Component):
    u"""
    Class encompassing several scenes to cover a defined section of
    Live's session. It handles starting and playing clips.
    """
    _session_component_ends_initialisation = True
    scene_component_type = SceneComponent
    managed_select_button = ButtonControl(color=u'Session.Select', pressed_color=u'Session.SelectPressed')
    managed_delete_button = ButtonControl(color=u'Session.Delete', pressed_color=u'Session.DeletePressed')
    managed_duplicate_button = ButtonControl(color=u'Session.Duplicate', pressed_color=u'Session.DuplicatePressed')

    def __init__(self, session_ring = None, auto_name = False, *a, **k):
        super(SessionComponent, self).__init__(*a, **k)
        assert session_ring is not None
        self._session_ring = session_ring
        self.__on_offsets_changed.subject = self._session_ring
        self._stop_all_button = None
        self._stop_track_clip_buttons = None
        self._stop_clip_triggered_value = u'Session.StopClipTriggered'
        self._stop_clip_value = u'Session.StopClip'
        self._stop_clip_disabled_value = u'Session.StopClipDisabled'
        self._track_slots = self.register_disconnectable(EventObject())
        self._selected_scene = self._create_scene()
        self._scenes = [ self._create_scene() for _ in range(self._session_ring.num_scenes) ]
        if self._session_component_ends_initialisation:
            self._end_initialisation()
        if auto_name:
            self._auto_name()
        self.__on_track_list_changed.subject = self.song
        self.__on_scene_list_changed.subject = self.song
        self.__on_selected_scene_changed.subject = self.song.view

    def _end_initialisation(self):
        self.__on_selected_scene_changed()
        self._reassign_scenes_and_tracks()

    def _create_scene(self):
        return self.scene_component_type(parent=self, session_ring=self._session_ring)

    def scene(self, index):
        assert in_range(index, 0, len(self._scenes))
        return self._scenes[index]

    def selected_scene(self):
        return self._selected_scene

    def _auto_name(self):
        self.name = u'Session_Control'
        self.selected_scene().name = u'Selected_Scene'
        for track_index in range(self._session_ring.num_tracks):
            clip_slot = self.selected_scene().clip_slot(track_index)
            clip_slot.name = u'Selected_Scene_Clip_Slot_%d' % track_index

        for scene_index in range(self._session_ring.num_scenes):
            scene = self.scene(scene_index)
            scene.name = u'Scene_%d' % scene_index
            for track_index in range(self._session_ring.num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = u'%d_Clip_Slot_%d' % (track_index, scene_index)

    def set_stop_all_clips_button(self, button):
        self._stop_all_button = button
        self.__on_stop_all_value.subject = button
        self._update_stop_all_clips_button()

    def set_stop_track_clip_buttons(self, buttons):
        self._stop_track_clip_buttons = buttons
        self.__on_stop_track_value.replace_subjects(buttons or [])
        self._update_stop_track_clip_buttons()

    def set_managed_select_button(self, button):
        self.managed_select_button.set_control_element(button)
        self.set_modifier_button(button, u'select')

    def set_managed_delete_button(self, button):
        self.managed_delete_button.set_control_element(button)
        self.set_modifier_button(button, u'delete')

    def set_managed_duplicate_button(self, button):
        self.managed_duplicate_button.set_control_element(button)
        self.set_modifier_button(button, u'duplicate')

    def set_modifier_button(self, button, name, clip_slots_only = False):
        for y in range(self._session_ring.num_scenes):
            scene = self.scene(y)
            if not clip_slots_only:
                getattr(scene, u'set_{}_button'.format(name))(button)
            for x in range(self._session_ring.num_tracks):
                getattr(scene.clip_slot(x), u'set_{}_button'.format(name))(button)

    def set_clip_launch_buttons(self, buttons):
        assert not buttons or buttons.width() == self._session_ring.num_tracks and buttons.height() == self._session_ring.num_scenes
        if buttons:
            for button, (x, y) in buttons.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(button)

        else:
            for x, y in product(range(self._session_ring.num_tracks), range(self._session_ring.num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(None)

    def set_scene_launch_buttons(self, buttons):
        num_scenes = self._session_ring.num_scenes
        assert not buttons or buttons.width() == num_scenes and buttons.height() == 1 or buttons.height() == num_scenes and buttons.width() == 1
        if buttons:
            for x, button in enumerate(buttons):
                scene = self.scene(x)
                scene.set_launch_button(button)

        else:
            for index in range(self._session_ring.num_scenes):
                scene = self.scene(index)
                scene.set_launch_button(None)

    @listens(u'offset')
    def __on_offsets_changed(self, *a):
        if self.is_enabled():
            self._reassign_scenes_and_tracks()

    def _reassign_scenes_and_tracks(self):
        self._reassign_tracks()
        self._reassign_scenes()

    def set_rgb_mode(self, color_palette, color_table, clip_slots_only = False):
        u"""
        Put the session into rgb mode by providing a color table and a color palette.
        color_palette is a dictionary, mapping custom Live colors to MIDI ids. This can be
        used to map a color directly to a CC value.
        The color_table is a list of tuples, where the first element is a MIDI CC and the
        second is the RGB color is represents. The table will be used to find the nearest
        matching color for a custom color. The table is used if there is no entry in the
        palette.
        """
        for y in range(self._session_ring.num_scenes):
            scene = self.scene(y)
            if not clip_slots_only:
                scene.set_color_palette(color_palette)
                scene.set_color_table(color_table)
            for x in range(self._session_ring.num_tracks):
                slot = scene.clip_slot(x)
                slot.set_clip_palette(color_palette)
                slot.set_clip_rgb_table(color_table)

    def update(self):
        super(SessionComponent, self).update()
        if self.is_enabled():
            self._update_stop_track_clip_buttons()
            self._update_stop_all_clips_button()
            self._reassign_scenes_and_tracks()

    def _update_stop_track_clip_buttons(self):
        if self.is_enabled():
            for index in range(self._session_ring.num_tracks):
                self._update_stop_clips_led(index)

    @listens(u'scenes')
    def __on_scene_list_changed(self):
        self._reassign_scenes()

    @listens(u'visible_tracks')
    def __on_track_list_changed(self):
        self._reassign_tracks()

    @listens(u'selected_scene')
    def __on_selected_scene_changed(self):
        if self._selected_scene != None:
            self._selected_scene.set_scene(self.song.view.selected_scene)

    def _update_stop_all_clips_button(self):
        if self.is_enabled():
            button = self._stop_all_button
            if button:
                button.set_light(button.is_pressed())

    def _reassign_scenes(self):
        scenes = self.song.scenes
        for index, scene in enumerate(self._scenes):
            scene_index = self._session_ring.scene_offset + index
            scene.set_scene(scenes[scene_index] if len(scenes) > scene_index else None)
            scene.set_track_offset(self._session_ring.track_offset)

        if self._selected_scene != None:
            self._selected_scene.set_track_offset(self._session_ring.track_offset)

    def _reassign_tracks(self):
        tracks_to_use = self._session_ring.tracks_to_use()
        tracks = list(map(lambda t: (t if isinstance(t, Live.Track.Track) else None), tracks_to_use))
        self.__on_fired_slot_index_changed.replace_subjects(tracks, count())
        self.__on_playing_slot_index_changed.replace_subjects(tracks, count())
        self._update_stop_all_clips_button()
        self._update_stop_track_clip_buttons()

    @listens(u'value')
    def __on_stop_all_value(self, value):
        self._stop_all_value(value)

    def _stop_all_value(self, value):
        if self.is_enabled():
            if value is not 0 or not self._stop_all_button.is_momentary():
                self.song.stop_all_clips()
            self._update_stop_all_clips_button()

    @listens_group(u'value')
    def __on_stop_track_value(self, value, button):
        if self.is_enabled():
            if value is not 0 or not button.is_momentary():
                tracks = self._session_ring.tracks_to_use()
                track_index = list(self._stop_track_clip_buttons).index(button) + self._session_ring.track_offset
                if in_range(track_index, 0, len(tracks)) and tracks[track_index] in self.song.tracks:
                    tracks[track_index].stop_all_clips()

    @listens_group(u'fired_slot_index')
    def __on_fired_slot_index_changed(self, track_index):
        self._on_fired_slot_index_changed(track_index)

    def _on_fired_slot_index_changed(self, track_index):
        session_ring = self._session_ring
        button_index = track_index - session_ring.track_offset
        if in_range(button_index, 0, session_ring.num_tracks):
            self._update_stop_clips_led(button_index)

    @listens_group(u'playing_slot_index')
    def __on_playing_slot_index_changed(self, track_index):
        self._on_playing_slot_index_changed(track_index)

    def _on_playing_slot_index_changed(self, track_index):
        session_ring = self._session_ring
        button_index = track_index - session_ring.track_offset
        if in_range(button_index, 0, session_ring.num_tracks):
            self._update_stop_clips_led(button_index)

    def _update_stop_clips_led(self, index):
        tracks_to_use = self._session_ring.tracks_to_use()
        track_index = index + self._session_ring.track_offset
        if self.is_enabled() and self._stop_track_clip_buttons != None and index < len(self._stop_track_clip_buttons):
            button = self._stop_track_clip_buttons[index]
            if button != None:
                value_to_send = None
                if track_index < len(tracks_to_use) and tracks_to_use[track_index].clip_slots:
                    track = tracks_to_use[track_index]
                    if track.fired_slot_index == -2:
                        value_to_send = self._stop_clip_triggered_value
                    elif track.playing_slot_index >= 0:
                        value_to_send = self._stop_clip_value
                    else:
                        value_to_send = self._stop_clip_disabled_value
                if value_to_send == None:
                    button.set_light(False)
                elif in_range(value_to_send, 0, 128):
                    button.send_value(value_to_send)
                else:
                    button.set_light(value_to_send)
