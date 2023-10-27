# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\automation.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 5620 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter, map
from Live import DeviceParameter
from ableton.v2.base import listenable_property, listens, liveobj_valid, old_hasattr
from ableton.v2.control_surface import InternalParameterBase, ParameterInfo, PitchParameter
from pushbase.automation_component import AutomationComponent as AutomationComponentBase

class StepAutomationParameter(InternalParameterBase):

    def __init__(self, parameter=None, *a, **k):
        (super(StepAutomationParameter, self).__init__)(a, name=parameter.name, **k)
        self._parameter = parameter
        self._value = self._parameter.value

    @listenable_property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def max(self):
        return self._parameter.max

    @property
    def min(self):
        return self._parameter.min

    @property
    def display_value(self):
        return self._parameter.str_for_value(self.value)

    @property
    def canonical_parent(self):
        return self._parameter.canonical_parent

    @property
    def original_parameter(self):
        return self._parameter

    @property
    def is_quantized(self):
        return self._parameter.is_quantized

    @property
    def value_items(self):
        return self._parameter.value_items

    @property
    def short_value_items(self):
        return self.value_items

    @property
    def automation_state(self):
        return self._parameter.automation_state


def make_automation_parameter(parameter_info):
    wrapped_parameter = None
    if parameter_info:
        if liveobj_valid(parameter_info.parameter):
            parameter = parameter_info.parameter
            if isinstance(parameter, PitchParameter):
                parameter = parameter.integer_value_host
            wrapped_parameter = ParameterInfo(parameter=StepAutomationParameter(parameter=parameter),
              name=(parameter_info.name),
              default_encoder_sensitivity=(parameter_info.default_encoder_sensitivity),
              fine_grain_encoder_sensitivity=(parameter_info.fine_grain_encoder_sensitivity))
    return wrapped_parameter


class AutomationComponent(AutomationComponentBase):
    ENCODER_SENSITIVITY_FACTOR = 0.5

    def __init__(self, *a, **k):
        self._parameter_infos = []
        (super(AutomationComponent, self).__init__)(*a, **k)
        self._drum_pad_selected = False

    @staticmethod
    def parameter_is_automateable(parameter):
        return liveobj_valid(parameter) and isinstance(parameter, (DeviceParameter.DeviceParameter, PitchParameter))

    @property
    def deviceType(self):
        device_type = 'default'
        device = self.device
        if liveobj_valid(device):
            device = self.parameter_provider.device()
            device_type = device.class_name if liveobj_valid(device) else device_type
        return device_type

    @listenable_property
    def device(self):
        device = None
        if old_hasattr(self.parameter_provider, 'device'):
            device = self.parameter_provider.device()
        return device

    def _on_parameter_provider_changed(self, provider):
        self.notify_device()
        self._AutomationComponent__on_device_changed.subject = provider if getattr(self.parameter_provider, 'device', None) is not None else None

    @listenable_property
    def parameters(self):
        return [info.parameter if info else None for info in self._parameter_infos]

    @property
    def parameter_infos(self):
        return self._parameter_infos

    def set_drum_pad_selected(self, value):
        if self._drum_pad_selected != value:
            self._drum_pad_selected = value
            self.notify_can_automate_parameters()

    @listenable_property
    def can_automate_parameters(self):
        return self._can_automate_parameters() and not self._drum_pad_selected

    def update(self):
        super(AutomationComponent, self).update()
        if self.is_enabled():
            self._rebuild_parameter_list()
            self._update_parameter_values()

    def _update_parameters(self):
        self._rebuild_parameter_list()
        super(AutomationComponent, self)._update_parameters()

    def _rebuild_parameter_list(self):
        self._parameter_infos = list(map(make_automation_parameter, self._parameter_infos_to_use())) if self.is_enabled() else []

    def _update_parameter_values(self):
        for info in filter(lambda p: p is not None
, self._parameter_infos):
            if len(self._selected_time) > 0:
                wrapped_parameter = info.parameter
                wrapped_parameter.value = self.parameter_to_value(wrapped_parameter.original_parameter)

        self.notify_parameters()

    def _parameter_for_index(self, parameters, index):
        if parameters[index]:
            return parameters[index].original_parameter

    @listens('device')
    def __on_device_changed(self):
        self.notify_device()