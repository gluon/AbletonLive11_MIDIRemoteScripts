<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/parameter_provider.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 1756 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, NamedTuple, liveobj_valid
DISCRETE_PARAMETERS_DICT = {'GlueCompressor': ('Ratio', 'Attack', 'Release', 'Peak Clip In')}

def is_parameter_quantized(parameter, parent_device):
    is_quantized = False
    if liveobj_valid(parameter):
        device_class = getattr(parent_device, 'class_name', None)
        is_quantized = (parameter.is_quantized) or ((device_class in DISCRETE_PARAMETERS_DICT) and (parameter.name in DISCRETE_PARAMETERS_DICT[device_class]))
    return is_quantized


class ParameterInfo(NamedTuple):
    parameter = None
    default_encoder_sensitivity = None
    fine_grain_encoder_sensitivity = None

    def __init__(self, name=None, *a, **k):
<<<<<<< HEAD
        (super(ParameterInfo, self).__init__)(a, _overridden_name=name, **k)
=======
        (super(ParameterInfo, self).__init__)(a, _overriden_name=name, **k)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    @property
    def name(self):
        actual_name = self.parameter.name if liveobj_valid(self.parameter) else ''
<<<<<<< HEAD
        return self._overridden_name or actual_name
=======
        return self._overriden_name or actual_name
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def __eq__(self, other_info):
        if not isinstance(other_info, ParameterInfo):
            return NotImplemented
        return super(ParameterInfo, self).__eq__(other_info) and self.name == other_info.name

    def __hash__(self):
        return hash((
         self._overridden_name,
         self.parameter,
         self.default_encoder_sensitivity,
         self.fine_grain_encoder_sensitivity))


class ParameterProvider(EventObject):
    __events__ = ('parameters', )

    @property
    def parameters(self):
        return []