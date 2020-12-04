#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/drum_pad_parameter_component.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import map
from builtins import range
from ableton.v2.base import clamp, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import Component, EnumWrappingParameter, InternalParameterBase, ParameterInfo, ParameterProvider
from ableton.v2.control_surface.control import StepEncoderControl
from .parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity
from .device_view_component import DeviceViewConnector
NO_CHOKE_GROUP = u'None'
MAX_CHOKE_GROUP = 16
NUM_CHOKE_GROUPS = MAX_CHOKE_GROUP + 1

def get_first_chain(drum_pad):
    if liveobj_valid(drum_pad) and len(drum_pad.chains) > 0:
        return drum_pad.chains[0]


class ChokeParameter(InternalParameterBase):
    is_quantized = True
    value_items = [NO_CHOKE_GROUP] + list(map(str, list(range(1, NUM_CHOKE_GROUPS))))
    min = 0
    max = MAX_CHOKE_GROUP

    def __init__(self, drum_pad = None, *a, **k):
        super(ChokeParameter, self).__init__(name=u'Choke', *a, **k)
        self.set_drum_pad(drum_pad)

    def set_drum_pad(self, drum_pad):
        self._pad = drum_pad
        self._on_choke_group_changed.subject = get_first_chain(drum_pad)
        self.notify_value()

    @listens(u'choke_group')
    def _on_choke_group_changed(self):
        self.notify_value()

    @listenable_property
    def value(self):
        first_chain = get_first_chain(self._pad)
        if liveobj_valid(first_chain):
            return first_chain.choke_group
        return 0

    @value.setter
    def value(self, value):
        value = clamp(value, 0, MAX_CHOKE_GROUP)
        get_first_chain(self._pad).choke_group = value

    @property
    def canonical_parent(self):
        return self._pad

    @property
    def display_value(self):
        return str(self.value)


DEFAULT_OUT_NOTE = 60

class DrumPadTransposeParameter(EnumWrappingParameter):

    def __init__(self, drum_pad = None, *a, **k):
        super(DrumPadTransposeParameter, self).__init__(name=u'Transpose', values_host=self, values_property=u'available_transpose_steps', index_property_host=get_first_chain(drum_pad), index_property=u'out_note', *a, **k)

    @property
    def available_transpose_steps(self, steps = list(range(128))):
        return steps

    @property
    def value_items(self):
        return []

    @property
    def min(self):
        return self.available_transpose_steps[0]

    @property
    def max(self):
        return self.available_transpose_steps[-1]

    @property
    def canonical_parent(self):
        return self._parent.drum_pad

    @property
    def display_value(self):
        difference = self.value - DEFAULT_OUT_NOTE
        sign = u'-' if difference < 0 else (u'+' if difference > 0 else u'')
        return sign + str(abs(difference)) + u' st'

    def set_drum_pad(self, drum_pad):
        self.set_property_host(get_first_chain(drum_pad))
        self.notify_value()


class DrumPadParameterComponent(Component, ParameterProvider):
    choke_encoder = StepEncoderControl(num_steps=10)
    transpose_encoder = StepEncoderControl(num_steps=10)

    def __init__(self, device_component = None, view_model = None, *a, **k):
        assert device_component is not None
        assert view_model is not None
        super(DrumPadParameterComponent, self).__init__(*a, **k)
        self._drum_pad = None
        self._parameters = []
        self.choke_param = ChokeParameter()
        self.transpose_param = DrumPadTransposeParameter(parent=self)
        self.register_disconnectables([self.choke_param, self.transpose_param])
        self._view_connector = DeviceViewConnector(parent=self, device_component=device_component, parameter_provider=self, view=view_model.deviceParameterView)

    def parameters_for_pad(self):
        if not self.has_filled_pad:
            return []
        return [ ParameterInfo(parameter=parameter, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter), fine_grain_encoder_sensitivity=fine_grain_parameter_mapping_sensitivity(parameter)) for parameter in [self.choke_param, self.transpose_param] ]

    def _get_drum_pad(self):
        return self._drum_pad

    def _set_drum_pad(self, pad):
        if pad != self._drum_pad:
            self._drum_pad = pad
            self._update_parameters()
            self._on_chains_in_pad_changed.subject = self._drum_pad

    drum_pad = property(_get_drum_pad, _set_drum_pad)

    @listens(u'chains')
    def _on_chains_in_pad_changed(self):
        self._update_parameters()

    def _update_parameters(self):
        self.transpose_param.set_drum_pad(self._drum_pad if self.has_filled_pad else None)
        self.choke_param.set_drum_pad(self._drum_pad if self.has_filled_pad else None)
        self._parameters = self.parameters_for_pad()
        self._view_connector.update()

    @property
    def has_filled_pad(self):
        return self._drum_pad and len(self._drum_pad.chains) > 0

    @property
    def parameters(self):
        return self._parameters

    @choke_encoder.value
    def choke_encoder(self, value, encoder):
        if len(self._parameters) > 0:
            self._parameters[0].parameter.value += value

    @transpose_encoder.value
    def transpose_encoder(self, value, encoder):
        if len(self._parameters) > 0:
            parameter = self._parameters[1].parameter
            if parameter.value + value in self.transpose_param.available_transpose_steps:
                parameter.value += value
