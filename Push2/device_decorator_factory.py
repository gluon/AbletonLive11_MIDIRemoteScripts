# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_decorator_factory.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 3339 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from .amp import AmpDeviceDecorator
from .analog import AnalogDeviceDecorator
from .auto_filter import AutoFilterDeviceDecorator
from .beatrepeat import BeatRepeatDeviceDecorator
from .chorus2 import Chorus2DeviceDecorator
from .collision import CollisionDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .corpus import CorpusDeviceDecorator
from .delay import DelayDeviceDecorator
from .device_decoration import DrumBussDeviceDecorator, PedalDeviceDecorator, SamplerDeviceDecorator, UtilityDeviceDecorator
from .drift import DriftDeviceDecorator
from .drumcell import DrumCellDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq3 import EqThreeDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .filterdelay import FilterDelayDeviceDecorator
from .graindelay import GrainDelayDeviceDecorator
from .hybrid_reverb import HybridReverbDeviceDecorator
from .operator import OperatorDeviceDecorator
from .phasernew import PhaserNewDeviceDecorator
from .redux2 import Redux2DeviceDecorator
from .reverb import ReverbDeviceDecorator
from .saturator import SaturatorDeviceDecorator
from .shifter import ShifterDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .spectral import SpectralDeviceDecorator
from .tension import TensionDeviceDecorator
from .transmute import TransmuteDeviceDecorator
from .vinyl import VinylDistortionDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {
      'Amp': AmpDeviceDecorator,
      'BeatRepeat': BeatRepeatDeviceDecorator,
      'OriginalSimpler': SimplerDeviceDecorator,
      'Operator': OperatorDeviceDecorator,
      'MultiSampler': SamplerDeviceDecorator,
      'AutoFilter': AutoFilterDeviceDecorator,
      'Eq8': Eq8DeviceDecorator,
      'DrumCell': DrumCellDeviceDecorator,
      'FilterDelay': FilterDelayDeviceDecorator,
      'FilterEQ3': EqThreeDeviceDecorator,
      'GrainDelay': GrainDelayDeviceDecorator,
      'Chorus2': Chorus2DeviceDecorator,
      'Collision': CollisionDeviceDecorator,
      'Compressor2': CompressorDeviceDecorator,
      'Corpus': CorpusDeviceDecorator,
      'Pedal': PedalDeviceDecorator,
      'PhaserNew': PhaserNewDeviceDecorator,
      'DrumBuss': DrumBussDeviceDecorator,
      'Echo': EchoDeviceDecorator,
      'Hybrid': HybridReverbDeviceDecorator,
      'InstrumentVector': WavetableDeviceDecorator,
      'Saturator': SaturatorDeviceDecorator,
      'Spectral': SpectralDeviceDecorator,
      'StereoGain': UtilityDeviceDecorator,
      'StringStudio': TensionDeviceDecorator,
      'Shifter': ShifterDeviceDecorator,
      'Transmute': TransmuteDeviceDecorator,
      'Delay': DelayDeviceDecorator,
      'Reverb': ReverbDeviceDecorator,
      'Drift': DriftDeviceDecorator,
      'Redux2': Redux2DeviceDecorator,
      'UltraAnalog': AnalogDeviceDecorator,
      'Vinyl': VinylDistortionDecorator}