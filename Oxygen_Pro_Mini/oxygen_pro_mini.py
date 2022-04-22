# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Oxygen_Pro_Mini/oxygen_pro_mini.py
# Compiled at: 2021-11-23 12:54:43
# Size of source mod 2**32: 673 bytes
from __future__ import absolute_import, print_function, unicode_literals
from Oxygen_Pro.mode import ReenterBehaviour
from Oxygen_Pro.oxygen_pro import Oxygen_Pro
from .simple_device import SimpleDeviceParameterComponent

class Oxygen_Pro_Mini(Oxygen_Pro):
    session_width = 4
    pad_ids = ((40, 41, 42, 43), (48, 49, 50, 51))
    device_parameter_component = SimpleDeviceParameterComponent

    def _get_device_mode_behaviour(self):
        return ReenterBehaviour(on_reenter=(self._on_reenter_device_mode))

    def _on_reenter_device_mode(self):
        self._device_parameters.toggle_parameter_offset()