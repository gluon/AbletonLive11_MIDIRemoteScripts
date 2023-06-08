from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionComponent as SessionComponentBase
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