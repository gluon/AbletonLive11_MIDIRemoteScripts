from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import control_list
from .control import DisplayControl
BUTTON_LABELS_MAP = {
  'song': ('Solo', 'Mute', 'Arm', 'Clip', 'Scene', 'Stop'),
  'instrument': ('-', '-', '-', '-', '-', '-'),
  'editor': ('Lock', '< Device', 'Device >', 'On/Off', '< Bank', 'Bank >'),
  'user': ('User 1', 'User 2', 'User 3', 'User 4', 'User 5', 'User 6')}

class ButtonLabelsComponent(Component):
    display_lines = control_list(DisplayControl, control_count=6)

    def show_button_labels_for_mode(self, mode_name):
        if mode_name in BUTTON_LABELS_MAP:
            for display, text in zip(self.display_lines, BUTTON_LABELS_MAP[mode_name]):
                display.message = text