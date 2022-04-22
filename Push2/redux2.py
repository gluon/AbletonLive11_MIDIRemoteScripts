# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/redux2.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 861 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_options import DeviceOnOffOption

class Redux2DeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(Redux2DeviceDecorator, self).__init__)(*a, **k)
        self.postFilter_on_option = DeviceOnOffOption(name='Post-Filter',
          property_host=(get_parameter_by_name(self, 'Post-Filter On')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.postFilter_on_option,)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters)