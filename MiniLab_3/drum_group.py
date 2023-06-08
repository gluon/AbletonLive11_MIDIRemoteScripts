from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from ableton.v3.control_surface.controls import PlayableControl

class DrumGroupComponent(DrumGroupComponentBase):

    def set_matrix(self, matrix):
        super().set_matrix(matrix)
        for button in self.matrix:
            button.set_mode(PlayableControl.Mode.playable_and_listenable)
            button.pressed_color = 'DrumGroup.PadPressed'