# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\device_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1785 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import ParameterInfo
from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v2.control_surface.control import ButtonControl
from .parameter_mapping_sensitivities import fine_grain_parameter_mapping_sensitivity, parameter_mapping_sensitivity

def is_wavetable(device):
    return liveobj_valid(device) and device.class_name == 'InstrumentVector'


class DeviceComponent(DeviceComponentBase):
    shift_button = ButtonControl()

    @shift_button.pressed
    def shift_button(self, button):
        decorated_device = self.device()
        if is_wavetable(decorated_device):
            decorated_device.osc_1_pitch.adjust_finegrain = True
            decorated_device.osc_2_pitch.adjust_finegrain = True

    @shift_button.released
    def shift_button(self, button):
        decorated_device = self.device()
        if is_wavetable(decorated_device):
            decorated_device.osc_1_pitch.adjust_finegrain = False
            decorated_device.osc_2_pitch.adjust_finegrain = False

    def _create_parameter_info(self, parameter, name):
        device_class_name = self.device().class_name
        return ParameterInfo(parameter=parameter,
          name=name,
          default_encoder_sensitivity=(parameter_mapping_sensitivity(parameter, device_class_name)),
          fine_grain_encoder_sensitivity=(fine_grain_parameter_mapping_sensitivity(parameter, device_class_name)))