<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import EncoderControl
from _Framework.SessionComponent import SessionComponent as SessionComponentBase
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Arturia/SessionComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2022 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import EncoderControl
import _Framework.SessionComponent as SessionComponentBase
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

class SessionComponent(SessionComponentBase):
    scene_select_encoder = EncoderControl()
    _session_component_ends_initialisation = False

    def __init__(self, *a, **k):
        (super(SessionComponent, self).__init__)(*a, **k)
        self.set_offsets(0, 0)
        self.on_selected_scene_changed()
        self.on_selected_track_changed()

    def set_scene_select_control(self, control):
        self.scene_select_encoder.set_control_element(control)

    @scene_select_encoder.value
    def scene_select_encoder(self, value, encoder):
        selected_scene = self.song().view.selected_scene
        all_scenes = self.song().scenes
        current_index = list(all_scenes).index(selected_scene)
<<<<<<< HEAD
        if value > 0 and selected_scene != all_scenes[-1]:
            self.song().view.selected_scene = all_scenes[current_index + 1]
        else:
            if value < 0:
                if selected_scene != all_scenes[0]:
                    self.song().view.selected_scene = all_scenes[current_index - 1]
=======
        if value > 0 and selected_scene != all_scenes[(-1)]:
            self.song().view.selected_scene = all_scenes[(current_index + 1)]
        elif value < 0:
            if selected_scene != all_scenes[0]:
                self.song().view.selected_scene = all_scenes[(current_index - 1)]
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def on_selected_scene_changed(self):
        super(SessionComponent, self).on_selected_scene_changed()
        all_scenes = list(self.song().scenes)
        selected_scene = self.song().view.selected_scene
        new_scene_offset = all_scenes.index(selected_scene)
        self.set_offsets(self.track_offset(), new_scene_offset)

    def on_selected_track_changed(self):
        super(SessionComponent, self).on_selected_track_changed()
        tracks = list(self.song().tracks)
        selected_track = self.song().view.selected_track
        if selected_track in tracks:
            track_index = tracks.index(selected_track)
            new_track_offset = track_index - track_index % self.width()
            self.set_offsets(new_track_offset, self.scene_offset())