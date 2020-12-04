#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/clip_slot.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase
from ableton.v2.control_surface.control import ButtonControl, TextDisplayControl
from .skin import LIVE_COLOR_TABLE_INDEX_OFFSET

class ClipSlotComponent(ClipSlotComponentBase):
    clip_name_display = TextDisplayControl(segments=(u'',))
    clip_color_control = ButtonControl()

    def __init__(self, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._empty_slot_with_stop_button_color = u'Session.ClipEmptyWithStopButton'
        view = self.song.view
        self.__on_selected_scene_changed.subject = view
        self.__on_selected_track_changed.subject = view
        self.__on_selected_track_changed()

    @property
    def select_button_is_pressed(self):
        return self._select_button is not None and self._select_button.is_pressed()

    def set_select_button(self, button):
        super(ClipSlotComponent, self).set_select_button(button)
        self.__on_select_button_value.subject = button

    @listens(u'value')
    def __on_select_button_value(self, value):
        self._update_clip_color_control()

    def _update_clip_property_slots(self):
        super(ClipSlotComponent, self)._update_clip_property_slots()
        clip = self._clip_slot.clip if liveobj_valid(self._clip_slot) else None
        self.__on_clip_name_changed.subject = clip
        self.__on_clip_name_changed()

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
        if slot_or_clip.color != None or getattr(slot_or_clip, u'controls_other_clips', True):
            return self._stopped_value
        if self._track_is_armed(track) and self._clip_slot.has_stop_button:
            return self._record_button_color
        if self._clip_slot.has_stop_button:
            return self._empty_slot_with_stop_button_color
        return self._empty_slot_color

    @listens(u'name')
    def __on_clip_name_changed(self):
        self._update_clip_name_display()

    @listens(u'selected_scene')
    def __on_selected_scene_changed(self):
        self._update_clip_color_control()

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._update_clip_color_control()

    def _update_clip_name_display(self):
        clip_slot = self._clip_slot
        self.clip_name_display[0] = clip_slot.clip.name if liveobj_valid(clip_slot) and self.has_clip() else u''

    def _update_clip_color_control(self):
        color_to_send = u'DefaultButton.Off'
        clip_slot = self._clip_slot
        if liveobj_valid(clip_slot):
            if self.has_clip():
                color_to_send = u'Session.ClipSelected' if self.select_button_is_pressed and clip_slot == self.song.view.highlighted_clip_slot else clip_slot.clip.color_index + LIVE_COLOR_TABLE_INDEX_OFFSET
            elif clip_slot.color != None:
                color_to_send = clip_slot.color_index + LIVE_COLOR_TABLE_INDEX_OFFSET
        self.clip_color_control.color = color_to_send
