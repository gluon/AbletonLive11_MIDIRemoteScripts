# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Oxygen_Pro/session.py
# Compiled at: 2021-11-23 12:54:43
# Size of source mod 2**32: 948 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class SessionComponent(SessionComponentBase):
    selected_scene_launch_button = ButtonControl()
    scene_encoder = EncoderControl()

    @scene_encoder.value
    def scene_encoder(self, value, _):
        factor = 1 if value < 0 else -1
        new_scene_index = factor + list(self.song.scenes).index(self.song.view.selected_scene)
        if new_scene_index in range(len(self.song.scenes)):
            self.song.view.selected_scene = self.song.scenes[new_scene_index]

    @selected_scene_launch_button.released_immediately
    def selected_scene_launch_button(self, _):
        self.song.view.selected_scene.fire()