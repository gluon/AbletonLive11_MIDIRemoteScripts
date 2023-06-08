from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import DecoratorFactory
from .delay_decoration import DelayDeviceDecorator
from .simpler_decoration import SimplerDeviceDecorator
from .wavetable_decoration import WavetableDeviceDecorator

class DeviceDecoratorFactory(DecoratorFactory):
    DECORATOR_CLASSES = {'Delay':DelayDeviceDecorator, 
     'OriginalSimpler':SimplerDeviceDecorator, 
     'InstrumentVector':WavetableDeviceDecorator}

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