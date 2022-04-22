# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/OpenLabs/SpecialDeviceComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1055 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
import _Framework.DeviceComponent as DeviceComponent

class SpecialDeviceComponent(DeviceComponent):

    def __init__(self):
        DeviceComponent.__init__(self)

    def _device_parameters_to_map(self):
        return self._device.parameters[1:]