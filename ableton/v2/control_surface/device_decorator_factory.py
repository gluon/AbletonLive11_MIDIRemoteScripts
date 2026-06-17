# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\device_decorator_factory.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 1427 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import DecoratorFactory
from .delay_decoration import DelayDeviceDecorator
from .drift_decoration import DriftDeviceDecorator
from .simpler_decoration import SimplerDeviceDecorator
from .wavetable_decoration import WavetableDeviceDecorator

class DeviceDecoratorFactory(DecoratorFactory):
    DECORATOR_CLASSES = {
      'Delay': DelayDeviceDecorator,
      'Drift': DriftDeviceDecorator,
      'OriginalSimpler': SimplerDeviceDecorator,
      'InstrumentVector': WavetableDeviceDecorator}

    @classmethod
    def generate_decorated_device(cls, device, additional_properties={}, song=None, *a, **k):
        decorated = (cls.DECORATOR_CLASSES[device.class_name])(a, live_object=device, additional_properties=additional_properties, **k)
        return decorated

    @classmethod
    def _should_be_decorated(cls, device):
        return liveobj_valid(device) and device.class_name in cls.DECORATOR_CLASSES

    def _get_decorated_object(self, device, additional_properties, song=None, *a, **k):
        return (self.generate_decorated_device)(
 device, *a, additional_properties=additional_properties, **k)