#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/mode.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.mode import Mode

class ExtendComboElementMode(Mode):

    def __init__(self, combo_pairs = None, *a, **k):
        super(ExtendComboElementMode, self).__init__(*a, **k)
        self._combo_pairs = combo_pairs

    def enter_mode(self):
        for combo, nested in self._combo_pairs:
            combo.register_control_element(nested)

    def leave_mode(self):
        for combo, nested in self._combo_pairs:
            combo.unregister_control_element(nested)
