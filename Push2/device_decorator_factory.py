from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from .auto_filter import AutoFilterDeviceDecorator
from .chorus2 import Chorus2DeviceDecorator
from .compressor import CompressorDeviceDecorator
from .corpus import CorpusDeviceDecorator
from .delay import DelayDeviceDecorator
from .device_decoration import DrumBussDeviceDecorator, PedalDeviceDecorator, SamplerDeviceDecorator, UtilityDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .hybrid_reverb import HybridReverbDeviceDecorator
from .operator import OperatorDeviceDecorator
from .phasernew import PhaserNewDeviceDecorator
from .redux2 import Redux2DeviceDecorator
from .reverb import ReverbDeviceDecorator
from .shifter import ShifterDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .spectral import SpectralDeviceDecorator
from .subzero import SubZeroDeviceDecorator
from .transmute import TransmuteDeviceDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {
      'OriginalSimpler': SimplerDeviceDecorator,
      'Operator': OperatorDeviceDecorator,
      'MultiSampler': SamplerDeviceDecorator,
      'AutoFilter': AutoFilterDeviceDecorator,
      'Eq8': Eq8DeviceDecorator,
      'Chorus2': Chorus2DeviceDecorator,
      'Compressor2': CompressorDeviceDecorator,
      'Corpus': CorpusDeviceDecorator,
      'Pedal': PedalDeviceDecorator,
      'PhaserNew': PhaserNewDeviceDecorator,
      'DrumBuss': DrumBussDeviceDecorator,
      'Echo': EchoDeviceDecorator,
      'Hybrid': HybridReverbDeviceDecorator,
      'InstrumentVector': WavetableDeviceDecorator,
      'Spectral': SpectralDeviceDecorator,
      'StereoGain': UtilityDeviceDecorator,
      'Shifter': ShifterDeviceDecorator,
      'Transmute': TransmuteDeviceDecorator,
      'Delay': DelayDeviceDecorator,
      'Reverb': ReverbDeviceDecorator,
      'SubZero': SubZeroDeviceDecorator,
      'Redux2': Redux2DeviceDecorator}