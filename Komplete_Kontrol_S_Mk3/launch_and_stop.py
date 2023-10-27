# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\launch_and_stop.py
# Compiled at: 2023-09-14 15:51:08
# Size of source mod 2**32: 2132 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import depends
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import liveobj_valid, scene_index

class LaunchAndStopComponent(Component):
    launch_button = ButtonControl(color=None)
    stop_button = ButtonControl(color=None)

    @depends(target_track=None)
    def __init__(self, target_track=None, *a, **k):
        (super().__init__)(a, name='Launch_And_Stop', **k)
        self._target_track = target_track
        self.register_slot(self.application.view, self._update_buttons, 'focused_document_view')
        self._update_buttons()

    @launch_button.pressed
    def launch_button(self, _):
        slot_or_scene = None
        if self._target_track.target_track in self.song.tracks:
            slot_or_scene = self._target_track.target_track.clip_slots[scene_index()]
        else:
            if self.song.view.selected_track == self.song.master_track:
                slot_or_scene = self.song.view.selected_scene
        if liveobj_valid(slot_or_scene):
            slot_or_scene.fire()

    @stop_button.pressed
    def stop_button(self, _):
        if self._target_track.target_track in self.song.tracks:
            self._target_track.target_track.stop_all_clips()
        else:
            if self.song.view.selected_track == self.song.master_track:
                self.song.stop_all_clips()

    def _update_buttons(self):
        in_session = self.application.view.focused_document_view == 'Session'
        self.launch_button.enabled = in_session
        self.stop_button.enabled = in_session