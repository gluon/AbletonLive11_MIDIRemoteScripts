# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/controls/toggle_button.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 470 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.control as ToggleButtonControlBase

class ToggleButtonControl(ToggleButtonControlBase):

    class State(ToggleButtonControlBase.State):

        def on_connected_property_changed(self, value=None):
            self.is_toggled = value or self.connected_property_value