# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\chorus2.py
# Compiled at: 2022-12-08 12:23:09
# Size of source mod 2**32: 4303 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .device_options import DeviceOnOffOption
from .visualisation_settings import VisualisationGuides

class Chorus2DeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(Chorus2DeviceDecorator, self).__init__)(*a, **k)
        self.fb_inv_option = DeviceOnOffOption(name='FB Inv',
          property_host=(get_parameter_by_name(self, 'FB Inv')))
        self.hpf_enabled_option = DeviceOnOffOption(name='High Pass',
          property_host=(get_parameter_by_name(self, 'HPF Enabled')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.fb_inv_option, self.hpf_enabled_option)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters)


class Chorus2DeviceComponent(DeviceComponentWithTrackColorViewData):
    LFO_VISUALISATION_CONFIGURATION_IN_BANKS = {0: ButtonRange(1, 4)}

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        adjusting_lfo = adjusting_lfo_phase = False
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        for parameter in touched_parameters:
            if parameter.name == 'Offset':
                adjusting_lfo_phase = True
            if parameter.name in ('Rate', 'Amount', 'Shape'):
                adjusting_lfo = True

        return {'AdjustingLfo':adjusting_lfo,  'AdjustingLfoPhase':adjusting_lfo_phase}

    def _set_bank_index(self, bank):
        super(Chorus2DeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._configuration_view_data)
        self._update_visualisation_view_data(self._adjustment_view_data)
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @property
    def _visualisation_visible(self):
        return self._bank.index in self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS

    @property
    def _shrink_parameters(self):
        result = [
         False] * 8
        if self._visualisation_visible:
            lfo_config = self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(-1, -1))
            for x in range(lfo_config.left_index, lfo_config.right_index + 1):
                result[x] = True

        return result

    @property
    def _configuration_view_data(self):
        lfo_left, lfo_right = self._calculate_view_size(self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS)
        return {'LfoLeft':lfo_left, 
         'LfoRight':lfo_right}

    def _initial_visualisation_view_data(self):
        view_data = super(Chorus2DeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._configuration_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data

    def _calculate_view_size(self, configuration):
        if self._bank.index not in configuration:
            return (0, 0)
        config = configuration[self._bank.index]
        return (
         VisualisationGuides.light_left_x(config.left_index),
         VisualisationGuides.light_right_x(config.right_index))