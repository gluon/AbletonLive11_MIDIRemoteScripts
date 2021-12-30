#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/SessionComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from itertools import count
import Live
from .CompoundComponent import CompoundComponent
from .SceneComponent import SceneComponent
from .ScrollComponent import ScrollComponent
from .SubjectSlot import subject_slot, subject_slot_group
from .Util import in_range, product

class SessionComponent(CompoundComponent):
    u"""
    Class encompassing several scene to cover a defined section of
    Live's session.  It controls the session ring and the set of tracks
    controlled by a given mixer.
    """
    __subject_events__ = (u'offset',)
    _linked_session_instances = []
    _minimal_track_offset = -1
    _minimal_scene_offset = -1
    _highlighting_callback = None
    _session_component_ends_initialisation = True
    scene_component_type = SceneComponent

    def __init__(self, num_tracks = 0, num_scenes = 0, auto_name = False, enable_skinning = False, *a, **k):
        super(SessionComponent, self).__init__(*a, **k)
        assert num_tracks >= 0
        assert num_scenes >= 0
        self._track_offset = -1
        self._scene_offset = -1
        self._num_tracks = num_tracks
        self._num_scenes = num_scenes
        self._vertical_banking, self._horizontal_banking, self._vertical_paginator, self._horizontal_paginator = self.register_components(ScrollComponent(), ScrollComponent(), ScrollComponent(), ScrollComponent())
        self._vertical_banking.can_scroll_up = self._can_bank_up
        self._vertical_banking.can_scroll_down = self._can_bank_down
        self._vertical_banking.scroll_up = self._bank_up
        self._vertical_banking.scroll_down = self._bank_down
        self._horizontal_banking.can_scroll_up = self._can_bank_left
        self._horizontal_banking.can_scroll_down = self._can_bank_right
        self._horizontal_banking.scroll_up = self._bank_left
        self._horizontal_banking.scroll_down = self._bank_right
        self._vertical_paginator.can_scroll_up = self._can_scroll_page_up
        self._vertical_paginator.can_scroll_down = self._can_scroll_page_down
        self._vertical_paginator.scroll_up = self._scroll_page_up
        self._vertical_paginator.scroll_down = self._scroll_page_down
        self._horizontal_paginator.can_scroll_up = self._can_scroll_page_left
        self._horizontal_paginator.can_scroll_down = self._can_scroll_page_right
        self._horizontal_paginator.scroll_up = self._scroll_page_left
        self._horizontal_paginator.scroll_down = self._scroll_page_right
        self._page_left_button = None
        self._page_right_button = None
        self._stop_all_button = None
        self._next_scene_button = None
        self._prev_scene_button = None
        self._stop_track_clip_buttons = None
        self._stop_clip_triggered_value = 127
        self._stop_clip_value = None
        self._highlighting_callback = None
        self._show_highlight = num_tracks > 0 and num_scenes > 0
        self._mixer = None
        self._track_slots = self.register_slot_manager()
        self._selected_scene = self.register_component(self._create_scene())
        self._scenes = self.register_components(*[ self._create_scene() for _ in range(num_scenes) ])
        if self._session_component_ends_initialisation:
            self._end_initialisation()
        if auto_name:
            self._auto_name()
        if enable_skinning:
            self._enable_skinning()

    def _end_initialisation(self):
        self.on_selected_scene_changed()
        self.set_offsets(0, 0)

    def _create_scene(self):
        return self.scene_component_type(num_slots=self._num_tracks, tracks_to_use_callback=self.tracks_to_use)

    def disconnect(self):
        if self._is_linked():
            self._unlink()
        super(CompoundComponent, self).disconnect()

    def set_highlighting_callback(self, callback):
        assert not callback or callable(callback)
        if self._highlighting_callback != callback:
            self._highlighting_callback = callback
            self._do_show_highlight()

    def scene(self, index):
        assert in_range(index, 0, len(self._scenes))
        return self._scenes[index]

    def selected_scene(self):
        return self._selected_scene

    def _enable_skinning(self):
        self.set_stop_clip_triggered_value(u'Session.StopClipTriggered')
        self.set_stop_clip_value(u'Session.StopClip')
        for scene_index in range(self._num_scenes):
            scene = self.scene(scene_index)
            scene.set_scene_value(u'Session.Scene')
            scene.set_no_scene_value(u'Session.NoScene')
            scene.set_triggered_value(u'Session.SceneTriggered')
            for track_index in range(self._num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_triggered_to_play_value(u'Session.ClipTriggeredPlay')
                clip_slot.set_triggered_to_record_value(u'Session.ClipTriggeredRecord')
                clip_slot.set_record_button_value(u'Session.RecordButton')
                clip_slot.set_stopped_value(u'Session.ClipStopped')
                clip_slot.set_started_value(u'Session.ClipStarted')
                clip_slot.set_recording_value(u'Session.ClipRecording')

    def _auto_name(self):
        self.name = u'Session_Control'
        self.selected_scene().name = u'Selected_Scene'
        for track_index in range(self._num_tracks):
            clip_slot = self.selected_scene().clip_slot(track_index)
            clip_slot.name = u'Selected_Scene_Clip_Slot_%d' % track_index

        for scene_index in range(self._num_scenes):
            scene = self.scene(scene_index)
            scene.name = u'Scene_%d' % scene_index
            for track_index in range(self._num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = u'%d_Clip_Slot_%d' % (track_index, scene_index)

    def set_scene_bank_buttons(self, down_button, up_button):
        self.set_scene_bank_up_button(up_button)
        self.set_scene_bank_down_button(down_button)

    def set_scene_bank_up_button(self, button):
        self._bank_up_button = button
        self._vertical_banking.set_scroll_up_button(button)

    def set_scene_bank_down_button(self, button):
        self._bank_down_button = button
        self._vertical_banking.set_scroll_down_button(button)

    def set_track_bank_buttons(self, right_button, left_button):
        self.set_track_bank_left_button(left_button)
        self.set_track_bank_right_button(right_button)

    def set_track_bank_left_button(self, button):
        self._bank_left_button = button
        self._horizontal_banking.set_scroll_up_button(button)

    def set_track_bank_right_button(self, button):
        self._bank_right_button = button
        self._horizontal_banking.set_scroll_down_button(button)

    def set_page_up_button(self, page_up_button):
        self._vertical_paginator.set_scroll_up_button(page_up_button)

    def set_page_down_button(self, page_down_button):
        self._vertical_paginator.set_scroll_down_button(page_down_button)

    def set_page_left_button(self, page_left_button):
        self._page_left_button = page_left_button
        self._horizontal_paginator.set_scroll_up_button(page_left_button)

    def set_page_right_button(self, page_right_button):
        self._page_right_button = page_right_button
        self._horizontal_paginator.set_scroll_down_button(page_right_button)

    def _can_scroll_page_up(self):
        return self.scene_offset() > 0

    def _can_scroll_page_down(self):
        return self.scene_offset() < len(self.song().scenes) - self.height()

    def _scroll_page_up(self):
        height = self.height()
        track_offset = self.track_offset()
        scene_offset = self.scene_offset()
        if scene_offset > 0:
            new_scene_offset = scene_offset
            if scene_offset % height > 0:
                new_scene_offset -= scene_offset % height
            else:
                new_scene_offset = max(0, scene_offset - height)
            self.set_offsets(track_offset, new_scene_offset)

    def _scroll_page_down(self):
        height = self.height()
        track_offset = self.track_offset()
        scene_offset = self.scene_offset()
        new_scene_offset = scene_offset + height - scene_offset % height
        self.set_offsets(track_offset, new_scene_offset)

    def _can_scroll_page_left(self):
        return self.track_offset() > 0

    def _can_scroll_page_right(self):
        return self.track_offset() < len(self.tracks_to_use()) - self.width()

    def _scroll_page_left(self):
        width = self.width()
        track_offset = self.track_offset()
        scene_offset = self.scene_offset()
        if track_offset > 0:
            new_track_offset = track_offset
            if track_offset % width > 0:
                new_track_offset -= track_offset % width
            else:
                new_track_offset = max(0, track_offset - width)
            self.set_offsets(new_track_offset, scene_offset)

    def _scroll_page_right(self):
        width = self.width()
        track_offset = self.track_offset()
        scene_offset = self.scene_offset()
        new_track_offset = track_offset + width - track_offset % width
        self.set_offsets(new_track_offset, scene_offset)

    def set_stop_all_clips_button(self, button):
        self._stop_all_button = button
        self._on_stop_all_value.subject = button
        self._update_stop_all_clips_button()

    def set_stop_track_clip_buttons(self, buttons):
        self._stop_track_clip_buttons = buttons
        self._on_stop_track_value.replace_subjects(buttons or [])
        self._update_stop_track_clip_buttons()

    def set_stop_clip_triggered_value(self, value):
        self._stop_clip_triggered_value = value

    def set_stop_clip_value(self, value):
        self._stop_clip_value = value

    def set_select_buttons(self, next_button, prev_button):
        self.set_select_next_button(next_button)
        self.set_select_prev_button(prev_button)

    def set_select_next_button(self, next_button):
        self._next_scene_button = next_button
        self._on_next_scene_value.subject = next_button
        self._update_select_buttons()

    def set_select_prev_button(self, prev_button):
        self._prev_scene_button = prev_button
        self._on_prev_scene_value.subject = prev_button
        self._update_select_buttons()

    def set_clip_launch_buttons(self, buttons):
        assert not buttons or buttons.width() == self._num_tracks and buttons.height() == self._num_scenes
        if buttons:
            for button, (x, y) in buttons.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(button)

        else:
            for x, y in product(range(self._num_tracks), range(self._num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(None)

    def set_scene_launch_buttons(self, buttons):
        assert not buttons or buttons.width() == self._num_scenes and buttons.height() == 1
        if buttons:
            for button, (x, _) in buttons.iterbuttons():
                scene = self.scene(x)
                scene.set_launch_button(button)

        else:
            for x in range(self._num_scenes):
                scene = self.scene(x)
                scene.set_launch_button(None)

    def set_mixer(self, mixer):
        u""" Sets the MixerComponent to be controlled by this session """
        self._mixer = mixer
        if self._mixer != None:
            self._mixer.set_track_offset(self.track_offset())

    def set_offsets(self, track_offset, scene_offset):
        assert track_offset >= 0
        assert scene_offset >= 0
        track_increment = 0
        scene_increment = 0
        if self._is_linked():
            SessionComponent._perform_offset_change(track_offset - self._track_offset, scene_offset - self._scene_offset)
        else:
            if len(self.tracks_to_use()) > track_offset:
                track_increment = track_offset - self._track_offset
            if len(self.song().scenes) > scene_offset:
                scene_increment = scene_offset - self._scene_offset
            self._change_offsets(track_increment, scene_increment)

    def set_show_highlight(self, show_highlight):
        if self._show_highlight != show_highlight:
            self._show_highlight = show_highlight
            self._do_show_highlight()

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
        for y in range(self._num_scenes):
            scene = self.scene(y)
            if not clip_slots_only:
                scene.set_color_palette(color_palette)
                scene.set_color_table(color_table)
            for x in range(self._num_tracks):
                slot = scene.clip_slot(x)
                slot.set_clip_palette(color_palette)
                slot.set_clip_rgb_table(color_table)

    def on_enabled_changed(self):
        self.update()
        self._do_show_highlight()

    def update(self):
        super(SessionComponent, self).update()
        if self._allow_updates:
            self._update_select_buttons()
            self._update_stop_track_clip_buttons()
            self._update_stop_all_clips_button()
        else:
            self._update_requests += 1

    def _update_stop_track_clip_buttons(self):
        if self.is_enabled():
            for index in range(self._num_tracks):
                self._update_stop_clips_led(index)

    def on_scene_list_changed(self):
        if not self._update_scene_offset():
            self._reassign_scenes()

    def _snap_track_offset(self):
        return self._page_left_button or self._page_right_button

    def on_track_list_changed(self):
        num_tracks = len(self.tracks_to_use())
        new_track_offset = self.track_offset()
        if new_track_offset >= num_tracks:
            new_track_offset = num_tracks - 1
            new_track_offset -= new_track_offset % (self.width() if self._snap_track_offset() else 1)
        self._reassign_tracks()
        self.set_offsets(new_track_offset, self.scene_offset())

    def on_selected_scene_changed(self):
        self._update_scene_offset()
        if self._selected_scene != None:
            self._selected_scene.set_scene(self.song().view.selected_scene)

    def width(self):
        return self._num_tracks

    def height(self):
        return len(self._scenes)

    def track_offset(self):
        return self._track_offset

    def scene_offset(self):
        return self._scene_offset

    def tracks_to_use(self):
        list_of_tracks = None
        if self._mixer != None:
            list_of_tracks = self._mixer.tracks_to_use()
        else:
            list_of_tracks = self.song().visible_tracks
        return list_of_tracks

    @property
    def current_tracks(self):
        tracks_to_use = self.tracks_to_use()
        offset = self.track_offset()
        return tracks_to_use[offset:offset + self.width()]

    def _get_minimal_track_offset(self):
        if self._is_linked():
            return SessionComponent._minimal_track_offset
        return self.track_offset()

    def _get_minimal_scene_offset(self):
        if self._is_linked():
            return SessionComponent._minimal_scene_offset
        return self.scene_offset()

    def _can_bank_down(self):
        return len(self.song().scenes) > self._get_minimal_scene_offset() + 1

    def _can_bank_up(self):
        return self._get_minimal_scene_offset() > 0

    def _can_bank_right(self):
        return len(self.tracks_to_use()) > self._get_minimal_track_offset() + 1

    def _can_bank_left(self):
        return self._get_minimal_track_offset() > 0

    def _bank_up(self):
        return self.set_offsets(self.track_offset(), max(0, self.scene_offset() - 1))

    def _bank_down(self):
        return self.set_offsets(self.track_offset(), self.scene_offset() + 1)

    def _bank_right(self):
        return self.set_offsets(self.track_offset() + 1, self.scene_offset())

    def _bank_left(self):
        return self.set_offsets(max(self.track_offset() - 1, 0), self.scene_offset())

    def _update_stop_all_clips_button(self):
        button = self._stop_all_button
        if button:
            button.set_light(button.is_pressed())

    def _update_select_buttons(self):
        selected_scene = self.song().view.selected_scene
        if self._next_scene_button != None:
            self._next_scene_button.set_light(selected_scene != self.song().scenes[-1])
        if self._prev_scene_button != None:
            self._prev_scene_button.set_light(selected_scene != self.song().scenes[0])

    def _update_scene_offset(self):
        offset_corrected = False
        num_scenes = len(self.song().scenes)
        if self.scene_offset() >= num_scenes:
            self.set_offsets(self.track_offset(), num_scenes - 1)
            offset_corrected = True
        return offset_corrected

    def _change_offsets(self, track_increment, scene_increment):
        offsets_changed = track_increment != 0 or scene_increment != 0
        if offsets_changed:
            self._track_offset += track_increment
            self._scene_offset += scene_increment
            assert self._track_offset >= 0
            assert self._scene_offset >= 0
            if self._mixer != None:
                self._mixer.set_track_offset(self.track_offset())
            self._reassign_tracks()
            self._reassign_scenes()
            self.notify_offset()
            if self.width() > 0 and self.height() > 0:
                self._do_show_highlight()

    def _reassign_scenes(self):
        scenes = self.song().scenes
        for index, scene in enumerate(self._scenes):
            scene_index = self._scene_offset + index
            if len(scenes) > scene_index:
                scene.set_scene(scenes[scene_index])
                scene.set_track_offset(self._track_offset)
            else:
                self._scenes[index].set_scene(None)

        if self._selected_scene != None:
            self._selected_scene.set_track_offset(self._track_offset)
        self._vertical_banking.update()
        self._vertical_paginator.update()

    def _reassign_tracks(self):
        current_tracks = self.current_tracks
        self._on_fired_slot_index_changed.replace_subjects(current_tracks, count())
        self._on_playing_slot_index_changed.replace_subjects(current_tracks, count())
        self._horizontal_banking.update()
        self._horizontal_paginator.update()
        self._update_stop_all_clips_button()
        self._update_stop_track_clip_buttons()

    @subject_slot(u'value')
    def _on_stop_all_value(self, value):
        self._stop_all_value(value)

    def _stop_all_value(self, value):
        if self.is_enabled():
            if value is not 0 or not self._stop_all_button.is_momentary():
                self.song().stop_all_clips()
            self._update_stop_all_clips_button()

    @subject_slot(u'value')
    def _on_next_scene_value(self, value):
        if self.is_enabled():
            if value is not 0 or not self._next_scene_button.is_momentary():
                selected_scene = self.song().view.selected_scene
                all_scenes = self.song().scenes
                if selected_scene != all_scenes[-1]:
                    index = list(all_scenes).index(selected_scene)
                    self.song().view.selected_scene = all_scenes[index + 1]

    @subject_slot(u'value')
    def _on_prev_scene_value(self, value):
        if self.is_enabled():
            if value is not 0 or not self._prev_scene_button.is_momentary():
                selected_scene = self.song().view.selected_scene
                all_scenes = self.song().scenes
                if selected_scene != all_scenes[0]:
                    index = list(all_scenes).index(selected_scene)
                    self.song().view.selected_scene = all_scenes[index - 1]

    @subject_slot_group(u'value')
    def _on_stop_track_value(self, value, button):
        if self.is_enabled():
            if value is not 0 or not button.is_momentary():
                tracks = self.tracks_to_use()
                track_index = list(self._stop_track_clip_buttons).index(button) + self.track_offset()
                if in_range(track_index, 0, len(tracks)) and tracks[track_index] in self.song().tracks:
                    tracks[track_index].stop_all_clips()

    def _do_show_highlight(self):
        if self._highlighting_callback != None:
            return_tracks = self.song().return_tracks
            include_returns = len(return_tracks) > 0 and return_tracks[0] in self.tracks_to_use()
            if self._show_highlight:
                self._highlighting_callback(self._track_offset, self._scene_offset, self.width(), self.height(), include_returns)
            else:
                self._highlighting_callback(-1, -1, -1, -1, include_returns)

    @subject_slot_group(u'fired_slot_index')
    def _on_fired_slot_index_changed(self, controlled_track_index):
        self._update_stop_clips_led(controlled_track_index)

    @subject_slot_group(u'playing_slot_index')
    def _on_playing_slot_index_changed(self, controlled_track_index):
        self._update_stop_clips_led(controlled_track_index)

    def _update_stop_clips_led(self, index):
        tracks_to_use = self.tracks_to_use()
        track_index = index + self.track_offset()
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
                if value_to_send == None:
                    button.turn_off()
                elif in_range(value_to_send, 0, 128):
                    button.send_value(value_to_send)
                else:
                    button.set_light(value_to_send)

    def _is_linked(self):
        return self in SessionComponent._linked_session_instances

    def _link(self):
        assert not self._is_linked()
        SessionComponent._linked_session_instances.append(self)

    def _unlink(self):
        assert self._is_linked()
        SessionComponent._linked_session_instances.remove(self)

    @staticmethod
    def _perform_offset_change(track_increment, scene_increment):
        u""" Performs the given offset changes on all linked instances """
        assert len(SessionComponent._linked_session_instances) > 0
        scenes = Live.Application.get_application().get_document().scenes
        instances_covering_session = 0
        found_negative_offset = False
        minimal_track_offset = -1
        minimal_scene_offset = -1
        for instance in SessionComponent._linked_session_instances:
            new_track_offset = instance.track_offset() + track_increment
            new_scene_offset = instance.scene_offset() + scene_increment
            if new_track_offset >= 0 and new_scene_offset >= 0:
                if new_track_offset < len(instance.tracks_to_use()) and new_scene_offset < len(scenes):
                    instances_covering_session += 1
                    if minimal_track_offset < 0:
                        minimal_track_offset = new_track_offset
                    else:
                        minimal_track_offset = min(minimal_track_offset, new_track_offset)
                    if minimal_scene_offset < 0:
                        minimal_scene_offset = new_scene_offset
                    else:
                        minimal_scene_offset = min(minimal_scene_offset, new_scene_offset)
            else:
                found_negative_offset = True
                break

        if not found_negative_offset and instances_covering_session > 0:
            SessionComponent._minimal_track_offset = minimal_track_offset
            SessionComponent._minimal_scene_offset = minimal_scene_offset
            for instance in SessionComponent._linked_session_instances:
                instance._change_offsets(track_increment, scene_increment)
