from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase

class DrumGroupComponent(DrumGroupComponentBase):

    def set_matrix(self, matrix):
        if matrix is None:
            if self.matrix.control_elements is not None:
                for button in self.matrix.control_elements:
                    button.clear_send_cache()
                    button.reset()

        super().set_matrix(matrix)