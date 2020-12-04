#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/parameter_provider.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid, NamedTuple, EventObject
DISCRETE_PARAMETERS_DICT = {u'GlueCompressor': (u'Ratio', u'Attack', u'Release', u'Peak Clip In')}

def is_parameter_quantized(parameter, parent_device):
    is_quantized = False
    if liveobj_valid(parameter):
        device_class = getattr(parent_device, u'class_name', None)
        is_quantized = parameter.is_quantized or device_class in DISCRETE_PARAMETERS_DICT and parameter.name in DISCRETE_PARAMETERS_DICT[device_class]
    return is_quantized


class ParameterInfo(NamedTuple):
    parameter = None
    default_encoder_sensitivity = None
    fine_grain_encoder_sensitivity = None

    def __init__(self, name = None, *a, **k):
        super(ParameterInfo, self).__init__(_overriden_name=name, *a, **k)

    @property
    def name(self):
        actual_name = self.parameter.name if liveobj_valid(self.parameter) else u''
        return self._overriden_name or actual_name

    def __eq__(self, other_info):
        if not isinstance(other_info, ParameterInfo):
            return NotImplemented
        return super(ParameterInfo, self).__eq__(other_info) and self.name == other_info.name

    def __hash__(self):
        return hash((self._overridden_name,
         self.parameter,
         self.default_encoder_sensitivity,
         self.fine_grain_encoder_sensitivity))


class ParameterProvider(EventObject):
    __events__ = (u'parameters',)

    @property
    def parameters(self):
        return []
