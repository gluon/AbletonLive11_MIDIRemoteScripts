# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\shifter.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6748 bytes
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import unicode
import Live
from ableton.v2.base import EventObject, listens
from ableton.v2.control_surface import EnumWrappingParameter, IntegerParameter, LiveObjectDecorator, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .device_options import DeviceOnOffOption
from .visualisation_settings import VisualisationGuides
ParameterState = Live.DeviceParameter.ParameterState

class ShifterDeviceDecorator(LiveObjectDecorator, EventObject):
    MIN_PITCH_BEND_RANGE = 0
    MAX_PITCH_BEND_RANGE = 24

    def __init__(self, *a, **k):
        (super(ShifterDeviceDecorator, self).__init__)(*a, **k)
        self._pitch_mode_parameter = EnumWrappingParameter(name='Pitch Mode',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='pitch_mode_list',
          index_property='pitch_mode_index')
        self._pitch_bend_range_parameter = IntegerParameter(name='Pitch Bend Range',
          parent=self,
          integer_value_host=(self._live_object),
          integer_value_property_name='pitch_bend_range',
          min_value=(self.MIN_PITCH_BEND_RANGE),
          max_value=(self.MAX_PITCH_BEND_RANGE),
          show_as_quantized=False,
          display_value_conversion=(lambda x: unicode(x) + ' st'
))
        self._additional_parameters = (
         self._pitch_mode_parameter,
         self._pitch_bend_range_parameter)
        self.on_pitch_mode_change.subject = self._pitch_mode_parameter
        self.on_pitch_mode_change()
        self._options = tuple([DeviceOnOffOption(name=n, property_host=(get_parameter_by_name(self, p))) for n, p in (('Delay', 'Delay On'),
                                                                                                                      ('Delay Sync', 'Delay Sync'),
                                                                                                                      ('Lfo Sync', 'Lfo Sync'),
                                                                                                                      ('Lfo Spin', 'Lfo Spin'),
                                                                                                                      ('Wide', 'Wide'),
                                                                                                                      ('RM Drive', 'RM Drive'),
                                                                                                                      ('Env. Follow', 'Env On'))])
        self.register_disconnectables(self.options)
        self.register_disconnectables(self._additional_parameters)

    @property
    def options(self):
        return self._options

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @listens('value')
    def on_pitch_mode_change(self):
        pitch_bend_state = ParameterState.enabled if self._pitch_mode_parameter.value == 1 else ParameterState.disabled
        self._pitch_bend_range_parameter.state = pitch_bend_state


class ShifterDeviceComponent(DeviceComponentWithTrackColorViewData):
    LFO_VISUALISATION_CONFIGURATION_IN_BANKS = {1: ButtonRange(1, 4)}
    _PRIMARY_LFO_PARAMETERS = frozenset(('Amount', 'Duty Cycle', 'Offset', 'Rate',
                                         'S. Rate', 'Waveform'))
    _SECONDARY_LFO_PARAMETERS = frozenset(('Amount', 'Duty Cycle', 'Offset', 'Phase',
                                           'Rate', 'S. Rate', 'S&H Width', 'Spin',
                                           'Waveform'))

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        adjusting_lfo = adjusting_secondary_lfo = False
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed if self.parameters[button.index].parameter.state == ParameterState.enabled]
        adjusting_lfo = any((p.name in self._PRIMARY_LFO_PARAMETERS for p in touched_parameters))
        adjusting_secondary_lfo = any((p.name in self._SECONDARY_LFO_PARAMETERS for p in touched_parameters))
        return {'AdjustingLfo':adjusting_lfo, 
         'AdjustingSecondaryLfo':adjusting_secondary_lfo}

    def _set_bank_index(self, bank):
        super(ShifterDeviceComponent, self)._set_bank_index(bank)
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

    def _basic_visualisation_view_data(self):
        view_data = super()._basic_visualisation_view_data()
        view_data.update(self._configuration_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data

    def _initial_visualisation_view_data(self):
        view_data = super(ShifterDeviceComponent, self)._initial_visualisation_view_data()
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