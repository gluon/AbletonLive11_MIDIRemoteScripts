<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/device_parameters.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2112 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from future.moves.itertools import zip_longest
from ableton.v2.control_surface import InternalParameterBase
from ableton.v2.control_surface.components import DisplayingDeviceParameterComponent
from ableton.v2.control_surface.control import ColorSysexControl, control_list
from .util import convert_parameter_value_to_midi_value

def is_internal_parameter(parameter):
    return isinstance(parameter, InternalParameterBase)


WIDTH = 8

class DeviceParameterComponent(DisplayingDeviceParameterComponent):
    parameter_color_fields = control_list(ColorSysexControl, WIDTH)
    encoder_color_fields = control_list(ColorSysexControl, WIDTH)

    def __init__(self, *a, **k):
        self._parameter_controls = None
<<<<<<< HEAD
        (super().__init__)(*a, **k)
=======
        (super(DeviceParameterComponent, self).__init__)(*a, **k)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def set_parameter_controls(self, encoders):
        super().set_parameter_controls(encoders)
        self._parameter_controls = encoders

    def _update_parameter_values(self):
        super()._update_parameter_values()
        for parameter, control in zip_longest(self.parameters, self._parameter_controls or []):
            if is_internal_parameter(parameter):
                if control:
                    control.send_value(convert_parameter_value_to_midi_value(parameter))

    def _update_parameters(self):
        super()._update_parameters()
        self._update_color_fields()

    def _update_color_fields(self):
        for color_field_index, parameter_info in zip_longest(range(WIDTH), self._parameter_provider.parameters[:WIDTH]):
            parameter = parameter_info.parameter if parameter_info else None
            color = 'Device.On' if parameter else 'DefaultButton.Disabled'
            self.parameter_color_fields[color_field_index].color = color
            self.encoder_color_fields[color_field_index].color = color