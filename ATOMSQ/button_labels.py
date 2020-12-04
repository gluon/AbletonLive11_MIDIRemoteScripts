#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/button_labels.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import control_list
from .control import DisplayControl
BUTTON_LABELS_MAP = {u'song': (u'Solo', u'Mute', u'Arm', u'Clip', u'Scene', u'Stop'),
 u'instrument': (u'-', u'-', u'-', u'-', u'-', u'-'),
 u'editor': (u'Lock', u'< Device', u'Device >', u'On/Off', u'< Bank', u'Bank >'),
 u'user': (u'User 1', u'User 2', u'User 3', u'User 4', u'User 5', u'User 6')}

class ButtonLabelsComponent(Component):
    display_lines = control_list(DisplayControl, control_count=6)

    def show_button_labels_for_mode(self, mode_name):
        if mode_name in BUTTON_LABELS_MAP:
            for display, text in zip(self.display_lines, BUTTON_LABELS_MAP[mode_name]):
                display.message = text
