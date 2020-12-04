#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/device_decorator_factory.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from .auto_filter import AutoFilterDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .device_decoration import SamplerDeviceDecorator, PedalDeviceDecorator, DrumBussDeviceDecorator, UtilityDeviceDecorator
from .hybrid_reverb import HybridReverbDeviceDecorator
from .delay import DelayDeviceDecorator
from .chorus2 import Chorus2DeviceDecorator
from .echo import EchoDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .operator import OperatorDeviceDecorator
from .redux2 import Redux2DeviceDecorator
from .transmute import TransmuteDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .spectral import SpectralDeviceDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {u'OriginalSimpler': SimplerDeviceDecorator,
     u'Operator': OperatorDeviceDecorator,
     u'MultiSampler': SamplerDeviceDecorator,
     u'AutoFilter': AutoFilterDeviceDecorator,
     u'Eq8': Eq8DeviceDecorator,
     u'Chorus2': Chorus2DeviceDecorator,
     u'Compressor2': CompressorDeviceDecorator,
     u'Pedal': PedalDeviceDecorator,
     u'DrumBuss': DrumBussDeviceDecorator,
     u'Echo': EchoDeviceDecorator,
     u'Hybrid': HybridReverbDeviceDecorator,
     u'InstrumentVector': WavetableDeviceDecorator,
     u'Spectral': SpectralDeviceDecorator,
     u'StereoGain': UtilityDeviceDecorator,
     u'Transmute': TransmuteDeviceDecorator,
     u'Delay': DelayDeviceDecorator,
     u'Redux2': Redux2DeviceDecorator}
