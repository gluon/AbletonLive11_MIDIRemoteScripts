# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/session.py
# Compiled at: 2021-08-06 01:27:35
# Size of source mod 2**32: 4152 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens_group, liveobj_valid
import ableton.v2.control_surface.components as ClipSlotComponentBase
import ableton.v2.control_surface.components as SceneComponentBase
import ableton.v2.control_surface.components as SessionComponentBase
from ableton.v2.control_surface.control import ButtonControl, InputControl
from .control import DisplayControl

class ClipSlotComponent(ClipSlotComponentBase):

    def _feedback_value(self, track, slot_or_clip):
        is_clip = slot_or_clip is not self._clip_slot
        if slot_or_clip.is_triggered:
            if slot_or_clip.will_record_on_start:
                return 'Session.{}TriggeredRecord'.format('Clip' if is_clip else 'Slot')
        else:
            return 'Session.{}TriggeredPlay'.format('Clip' if is_clip else 'Slot')
            if slot_or_clip.is_playing:
                if slot_or_clip.is_recording:
                    return 'Session.ClipRecording'
                return 'Session.ClipStarted'
            if is_clip:
                return 'Session.ClipStopped'
            return self._clip_slot.has_stop_button or 'Session.SlotLacksStop'
        if self._track_is_armed(track):
            if self._clip_slot.has_stop_button:
                return 'Session.RecordButton'
        return 'Session.ClipEmpty'


class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent

    @property
    def scene(self):
        return self._scene


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent
    track_select_control = InputControl()
    scene_name_display = DisplayControl()
    stop_all_clips_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')

    def set_stop_all_clips_button(self, button):
        self.stop_all_clips_button.set_control_element(button)

    @track_select_control.value
    def track_select_control(self, value, _):
        if value and value <= len(self._stop_track_clip_buttons):
            index = value - 1
            button = self._stop_track_clip_buttons[index]
            if button:
                button.clear_send_cache()
                self._update_stop_clips_led(index)
        else:
            self._update_stop_all_clips_button()

    @stop_all_clips_button.pressed_delayed
    def stop_all_clips_button(self, _):
        self.song.stop_all_clips()

    def _reassign_scenes(self):
        super(SessionComponent, self)._reassign_scenes()
        self._SessionComponent__on_scene_name_changed.replace_subjects((s.scene for s in self._scenes))
        self._update_scene_name_display()

    def _update_scene_name_display(self):
        self.scene_name_display.data = [s.scene for s in self._scenes if liveobj_valid(s._scene)]

    @listens_group('name')
    def __on_scene_name_changed(self, _):
        self._update_scene_name_display()

    def _update_stop_all_clips_button(self):
        self.stop_all_clips_button.color = 'DefaultButton.Off'