# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\drum_pad_parameter_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6302 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, range, str
from ableton.v2.base import clamp, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import Component, EnumWrappingParameter, InternalParameterBase, ParameterInfo, ParameterProvider
from ableton.v2.control_surface.control import StepEncoderControl
from .device_view_component import DeviceViewConnector
from .parameter_mapping_sensitivities import fine_grain_parameter_mapping_sensitivity, parameter_mapping_sensitivity
NO_CHOKE_GROUP = 'None'
MAX_CHOKE_GROUP = 16
NUM_CHOKE_GROUPS = MAX_CHOKE_GROUP + 1

def get_first_chain(drum_pad):
    if liveobj_valid(drum_pad):
        if len(drum_pad.chains) > 0:
            return drum_pad.chains[0]


class ChokeParameter(InternalParameterBase):
    is_quantized = True
    value_items = [
     NO_CHOKE_GROUP] + list(map(str, list(range(1, NUM_CHOKE_GROUPS))))
    min = 0
    max = MAX_CHOKE_GROUP

    def __init__(self, drum_pad=None, *a, **k):
        (super(ChokeParameter, self).__init__)(a, name='Choke', **k)
        self.set_drum_pad(drum_pad)

    def set_drum_pad(self, drum_pad):
        self._pad = drum_pad
        self._on_choke_group_changed.subject = get_first_chain(drum_pad)
        self.notify_value()

    @listens('choke_group')
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

    @property
    def short_value_items(self):
        return self.value_items


DEFAULT_OUT_NOTE = 60

class DrumPadTransposeParameter(EnumWrappingParameter):

    def __init__(self, drum_pad=None, *a, **k):
        (super(DrumPadTransposeParameter, self).__init__)(a, name='Transpose', values_host=self, values_property='available_transpose_steps', index_property_host=get_first_chain(drum_pad), index_property='out_note', **k)

    @property
    def available_transpose_steps(self, steps=list(range(128))):
        return steps

    @property
    def value_items(self):
        return []

    @property
    def short_value_items(self):
        return self.value_items

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
        sign = '-' if difference < 0 else '+' if difference > 0 else ''
        return sign + str(abs(difference)) + ' st'

    def set_drum_pad(self, drum_pad):
        self.set_property_host(get_first_chain(drum_pad))
        self.notify_value()


class DrumPadParameterComponent(Component, ParameterProvider):
    choke_encoder = StepEncoderControl(num_steps=10)
    transpose_encoder = StepEncoderControl(num_steps=10)

    def __init__(self, device_component=None, view_model=None, *a, **k):
        (super(DrumPadParameterComponent, self).__init__)(*a, **k)
        self._drum_pad = None
        self._parameters = []
        self.choke_param = ChokeParameter()
        self.transpose_param = DrumPadTransposeParameter(parent=self)
        self.register_disconnectables([self.choke_param, self.transpose_param])
        self._view_connector = DeviceViewConnector(parent=self,
          device_component=device_component,
          parameter_provider=self,
          view=(view_model.deviceParameterView))

    def parameters_for_pad(self):
        if not self.has_filled_pad:
            return []
        return [ParameterInfo(parameter=parameter, default_encoder_sensitivity=(parameter_mapping_sensitivity(parameter)), fine_grain_encoder_sensitivity=(fine_grain_parameter_mapping_sensitivity(parameter))) for parameter in [self.choke_param, self.transpose_param]]

    def _get_drum_pad(self):
        return self._drum_pad

    def _set_drum_pad(self, pad):
        if pad != self._drum_pad:
            self._drum_pad = pad
            self._update_parameters()
            self._on_chains_in_pad_changed.subject = self._drum_pad

    drum_pad = property(_get_drum_pad, _set_drum_pad)

    @listens('chains')
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