# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\clip_slot.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 4033 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase
from ableton.v2.control_surface.control import ButtonControl, TextDisplayControl
from .skin import LIVE_COLOR_TABLE_INDEX_OFFSET

class ClipSlotComponent(ClipSlotComponentBase):
    clip_name_display = TextDisplayControl(segments=('', ))
    clip_color_control = ButtonControl()

    def __init__(self, *a, **k):
        (super(ClipSlotComponent, self).__init__)(*a, **k)
        self._empty_slot_with_stop_button_color = 'Session.ClipEmptyWithStopButton'
        view = self.song.view
        self._ClipSlotComponent__on_selected_scene_changed.subject = view
        self._ClipSlotComponent__on_selected_track_changed.subject = view
        self._ClipSlotComponent__on_selected_track_changed()

    @property
    def select_button_is_pressed(self):
        return self._select_button is not None and self._select_button.is_pressed()

    def set_select_button(self, button):
        super(ClipSlotComponent, self).set_select_button(button)
        self._ClipSlotComponent__on_select_button_value.subject = button

    @listens('value')
    def __on_select_button_value(self, value):
        self._update_clip_color_control()

    def _update_clip_property_slots(self):
        super(ClipSlotComponent, self)._update_clip_property_slots()
        clip = self._clip_slot.clip if liveobj_valid(self._clip_slot) else None
        self._ClipSlotComponent__on_clip_name_changed.subject = clip
        self._ClipSlotComponent__on_clip_name_changed()

    def _update_launch_button_color(self):
        super(ClipSlotComponent, self)._update_launch_button_color()
        self._update_clip_color_control()

    def _feedback_value(self, track, slot_or_clip):
        if slot_or_clip.is_triggered:
            if slot_or_clip.will_record_on_start:
                return self._triggered_to_record_color
            return self._triggered_to_play_color
        if slot_or_clip.is_playing:
            if slot_or_clip.is_recording:
                return self._recording_color
            return self._started_value
        if slot_or_clip.color != None or getattr(slot_or_clip, 'controls_other_clips', True):
            return self._stopped_value
        if self._track_is_armed(track):
            if self._clip_slot.has_stop_button:
                return self._record_button_color
        if self._clip_slot.has_stop_button:
            return self._empty_slot_with_stop_button_color
        return self._empty_slot_color

    @listens('name')
    def __on_clip_name_changed(self):
        self._update_clip_name_display()

    @listens('selected_scene')
    def __on_selected_scene_changed(self):
        self._update_clip_color_control()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_clip_color_control()

    def _update_clip_name_display(self):
        clip_slot = self._clip_slot
        self.clip_name_display[0] = clip_slot.clip.name if (liveobj_valid(clip_slot)) and (self.has_clip()) else ''

    def _update_clip_color_control(self):
        color_to_send = 'DefaultButton.Off'
        clip_slot = self._clip_slot
        if liveobj_valid(clip_slot):
            if self.has_clip():
                color_to_send = 'Session.ClipSelected' if (self.select_button_is_pressed) and (clip_slot == self.song.view.highlighted_clip_slot) else (clip_slot.clip.color_index + LIVE_COLOR_TABLE_INDEX_OFFSET)
            else:
                if clip_slot.color != None:
                    color_to_send = clip_slot.color_index + LIVE_COLOR_TABLE_INDEX_OFFSET
        self.clip_color_control.color = color_to_send