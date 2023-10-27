# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\device_parameters.py
# Compiled at: 2023-03-08 07:29:56
# Size of source mod 2**32: 2399 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import zip_longest
from ...base import listens
from .. import Component, ParameterProvider
from ..controls import MappedSensitivitySettingControl, control_list

class DeviceParametersComponent(Component):
    controls = control_list(MappedSensitivitySettingControl, 8)

    def __init__(self, parameter_provider=None, name='Device_Parameters', *a, **k):
        (super().__init__)(a, name=name, **k)
        self.parameter_provider = parameter_provider

    @property
    def parameter_provider(self):
        return self._parameter_provider

    @parameter_provider.setter
    def parameter_provider(self, provider):
        self._parameter_provider = provider or ParameterProvider()
        self._DeviceParametersComponent__on_parameters_changed.subject = self._parameter_provider
        self._update_parameters()

    def set_parameter_controls(self, encoders):
        if encoders:
            if len(encoders) > self.controls.control_count:
                self.controls.control_count = len(encoders)
        self.controls.set_control_element(encoders)
        self._connect_parameters()

    def _connect_parameters(self):
        parameters = self._parameter_provider.parameters[:self.controls.control_count]
        for control, parameter_info in zip_longest(self.controls, parameters):
            parameter = parameter_info.parameter if parameter_info else None
            control.mapped_parameter = parameter
            if parameter:
                control.update_sensitivities(parameter_info.default_encoder_sensitivity, parameter_info.fine_grain_encoder_sensitivity)

    def update(self):
        super().update()
        self._update_parameters()

    def _update_parameters(self):
        if self.is_enabled():
            self._connect_parameters()

    @listens('parameters')
    def __on_parameters_changed(self):
        self._update_parameters()