# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/session.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4076 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import listens_group, liveobj_valid
import ableton.v3.control_surface.components as ClipSlotComponentBase
import ableton.v3.control_surface.components as SessionComponentBase
from ableton.v3.control_surface.controls import ButtonControl, InputControl
from .control import DisplayControl

class ClipSlotComponent(ClipSlotComponentBase):

    def _feedback_value(self, track, slot_or_clip):
        is_clip = slot_or_clip is not self._clip_slot
        if slot_or_clip.is_triggered:
            if slot_or_clip.will_record_on_start:
                return 'Session.{}TriggeredRecord'.format('Clip' if is_clip else 'Slot')
            return 'Session.{}TriggeredPlay'.format('Clip' if is_clip else 'Slot')
        if slot_or_clip.is_playing:
            if slot_or_clip.is_recording:
                return 'Session.ClipRecording'
            return 'Session.ClipStarted'
        if is_clip:
            return 'Session.ClipStopped'
        if not self._clip_slot.has_stop_button:
            return 'Session.SlotLacksStop'
        if self._track_is_armed(track):
            if self._clip_slot.has_stop_button:
                return 'Session.ClipRecordButton'
        return 'Session.ClipEmpty'


class SessionComponent(SessionComponentBase):
    track_select_control = InputControl()
    scene_name_display = DisplayControl()
    stop_all_clips_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')

    def __init__(self, *a, **k):
        (super().__init__)(a, clip_slot_component_type=ClipSlotComponent, **k)

    def set_stop_all_clips_button(self, button):
        self.stop_all_clips_button.set_control_element(button)

    @track_select_control.value
    def track_select_control(self, value, _):
        if value and value <= self.stop_track_clip_buttons.control_count:
            index = value - 1
            button = self.stop_track_clip_buttons[index]._control_element
            if button:
                button.clear_send_cache()
                self._update_stop_clips_led(index)
        else:
            self._update_stop_all_clips_button()

    @stop_all_clips_button.pressed_delayed
    def stop_all_clips_button(self, _):
        self.song.stop_all_clips()

    def _reassign_scenes(self):
        super()._reassign_scenes()
        self._SessionComponent__on_scene_name_changed.replace_subjects((s.scene for s in self._scenes))
        self._update_scene_name_display()

    def _update_scene_name_display(self):
        self.scene_name_display.data = [s.scene for s in self._scenes if liveobj_valid(s.scene)]

    @listens_group('name')
    def __on_scene_name_changed(self, _):
        self._update_scene_name_display()

    def _update_stop_all_clips_button(self):
        self.stop_all_clips_button.color = 'DefaultButton.Off'