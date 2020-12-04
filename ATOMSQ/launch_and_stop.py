#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/launch_and_stop.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import ClipSlotComponent
from ableton.v2.control_surface.control import ButtonControl, ToggleButtonControl

class LaunchAndStopComponent(Component):
    scene_launch_button = ButtonControl(color=u'DefaultButton.Off', pressed_color=u'DefaultButton.On')
    track_stop_button = ButtonControl()

    def __init__(self, *a, **k):
        super(LaunchAndStopComponent, self).__init__(*a, **k)
        self._clip_slot = ClipSlotComponent()
        self.register_slot(self.song.view, self.__on_track_or_scene_changed, u'selected_track')
        self.register_slot(self.song.view, self.__on_track_or_scene_changed, u'selected_scene')
        self.__on_playing_status_changed.subject = self.song.view
        self.__on_track_or_scene_changed()
        self.__on_playing_status_changed()

    def set_clip_launch_button(self, button):
        self._clip_slot.set_launch_button(button)

    @scene_launch_button.pressed
    def scene_launch_button(self, _):
        self.song.view.selected_scene.fire()

    @track_stop_button.pressed
    def track_stop_button(self, _):
        self.song.view.selected_track.stop_all_clips()

    def __on_track_or_scene_changed(self):
        slot = self.song.view.highlighted_clip_slot
        self._clip_slot.set_clip_slot(slot if liveobj_valid(slot) else None)

    @listens(u'selected_track.playing_slot_index')
    def __on_playing_status_changed(self):
        track = self.song.view.selected_track
        self.track_stop_button.enabled = track in self.song.tracks and track.playing_slot_index >= 0
