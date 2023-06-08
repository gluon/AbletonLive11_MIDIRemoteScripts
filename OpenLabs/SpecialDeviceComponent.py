from __future__ import absolute_import, print_function, unicode_literals
import Live
import _Framework.DeviceComponent as DeviceComponent

class SpecialDeviceComponent(DeviceComponent):

    def __init__(self):
        DeviceComponent.__init__(self)

    def _device_parameters_to_map(self):
        return self._device.parameters[1:]