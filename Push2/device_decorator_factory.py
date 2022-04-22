# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/device_decorator_factory.py
# Compiled at: 2022-01-28 05:06:23
# Size of source mod 2**32: 2090 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface as DeviceDecoratorFactoryBase
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
from .shifter import ShifterDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .spectral import SpectralDeviceDecorator
from .transmute import TransmuteDeviceDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {'OriginalSimpler':SimplerDeviceDecorator, 
     'Operator':OperatorDeviceDecorator, 
     'MultiSampler':SamplerDeviceDecorator, 
     'AutoFilter':AutoFilterDeviceDecorator, 
     'Eq8':Eq8DeviceDecorator, 
     'Chorus2':Chorus2DeviceDecorator, 
     'Compressor2':CompressorDeviceDecorator, 
     'Corpus':CorpusDeviceDecorator, 
     'Pedal':PedalDeviceDecorator, 
     'PhaserNew':PhaserNewDeviceDecorator, 
     'DrumBuss':DrumBussDeviceDecorator, 
     'Echo':EchoDeviceDecorator, 
     'Hybrid':HybridReverbDeviceDecorator, 
     'InstrumentVector':WavetableDeviceDecorator, 
     'Spectral':SpectralDeviceDecorator, 
     'StereoGain':UtilityDeviceDecorator, 
     'Shifter':ShifterDeviceDecorator, 
     'Transmute':TransmuteDeviceDecorator, 
     'Delay':DelayDeviceDecorator, 
     'Redux2':Redux2DeviceDecorator}